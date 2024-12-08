import imap_tools
from imap_tools import MailBox,AND,A
import getpass
import json 
import os 
from gtts import gTTS
import playsound
import pygame


import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from classification import classify_email

from dotenv import load_dotenv

from classification import classify_email
from parse import parsed_pdf_data,parsed_excel_data

load_dotenv()

#Load env variables
PROJECT_HOME_PATH=os.getenv('PROJECT_HOME_PATH')
EMAIL=os.getenv('EMAIL')
PASSWORD=os.getenv('PASSWORD')

#load mail config
config_path=os.path.join(PROJECT_HOME_PATH,'Config','mailconfig.json')
with open(config_path) as file:
    config=json.load(file)
    # print(config)
    file.close()


def speak(text):
    try:
        audio_file_path=os.path.join(PROJECT_HOME_PATH,'Data','Sound_mp3','output_mp3')
        #gtts API to convert text to speech 
        tts=gTTS(text,lang='en',slow=False) 
        tts.save(audio_file_path)
        # Initialize the mixer module
        pygame.mixer.init()
        # Load the mp3 file
        pygame.mixer.music.load(audio_file_path)
        # Play the loaded mp3 file
        pygame.mixer.music.play()
        # Wait until the music finishes playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Small delay to wait for playback
    
    except Exception as e:
        print(f"Exception :{e}")

    finally:
        # os.remove('output2.mp3')
        print("file temporary remove successfuly1!!!")


def read_email_from_email(username="shubham", configdata=config):
    ORG_EMAIL = configdata['mail']['ORG_EMAIL']
    SMTP_SERVER = configdata['mail']['SMTP_SERVER']
    FROM_EMAIL = EMAIL
    FROM_PWD = PASSWORD

    storage_dir = os.path.join(PROJECT_HOME_PATH, 'Data', 'Extract_data')

    mail = MailBox(SMTP_SERVER).login(FROM_EMAIL, FROM_PWD)

    print("Email account access success!")
    messages = mail.fetch(A(seen=False), mark_seen=False)
    print("Messages fetched successfully!")
    msg_list = list(messages)

    email_data_list = []  # List to store parsed email data

    if len(msg_list) > 0:
        for email in msg_list:
            print(email)
            email_data = {}  # Initialize a dictionary to store email data
            
            # Get sender email address
            email_holder = email.from_
            email_data['sender'] = email_holder
            
            # Get email subject
            email_subject = email.subject
            email_data['subject'] = email_subject
            
            # Get email date
            email_date = email.date.strftime("%Y-%m-%d_%H-%M-%S")
            email_data['date'] = email_date
            
            # Get email body
            email_body = email.text
            email_data['body'] = email_body

            # Classify the email
            email_check = json.loads(classify_email(email_subject, email_body))

            # Add 'po_detected' field to indicate whether the email is classified as 'Yes'
            email_data['po_detected'] = 'Yes' if email_check["classification"] == 'Yes' else 'No'

            if email_check["classification"] == 'Yes':
            
                # Define unique folder name to store attachments
                folder_name = f"{email_holder.replace(' ', '_').replace('@', '_').replace('.', '_')}_{email_date}"
                folder_path = os.path.join(storage_dir, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                
                # Get thread-related information
                in_reply_to = email.headers.get('In-Reply-To', '')
                references = email.headers.get('References', '')
                thread_link = ""
                if in_reply_to:
                    thread_link = f"https://mail.google.com/mail/u/0/#inbox/{in_reply_to}"
                elif references:
                    thread_link = f"https://mail.google.com/mail/u/0/#inbox/{references.split()[0]}"
                email_data['thread_link'] = thread_link if thread_link else None

                parsed_files_data = {}  # Dictionary to store parsed file data

                # Process attachments
                for att in email.attachments:
                    file_extension = att.filename.split('.')[-1].lower()
                    allowed_extensions = ['pdf', 'jpg', 'jpeg', 'docx', 'png', 'xls', 'xlsx']
                    if file_extension in allowed_extensions:
                        file_path = os.path.join(folder_path, att.filename)
                        with open(file_path, 'wb') as f:
                            f.write(att.payload)
                        print(f"Attachment {att.filename} saved to {file_path}")

                        # Parse the file if it is PDF or Excel
                        if file_extension == 'pdf':
                            parsed_files_data[att.filename] = parsed_pdf_data(file_path)
                        elif file_extension in ['xls', 'xlsx']:
                            parsed_files_data[att.filename] = parsed_excel_data(file_path)
                
                email_data['attachments'] = list(parsed_files_data.keys())
                email_data['parsed_files_data'] = parsed_files_data

                # Speak email summary
                text = f"{username}, You have an email from {email_holder} with a subject saying {email_subject}"
                speak(text)
                print(text)
                
                # Add email data to the list
                email_data_list.append(email_data)
            
            else:
                email_data_list.append(email_data)
                email_data_list.append(email_check)

    else:
        print("You don't have any new emails!")
        speak("You don't have any new emails!")

    return email_data_list  # Return the list of dictionaries for all emails


if __name__=='__main__':
    data=read_email_from_email('Shubham',config)

    print(data)
    # speak("heelo i am shubham")
