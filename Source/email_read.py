import imap_tools
from imap_tools import MailBox,AND,A
import getpass
import json 
import os 
from gtts import gTTS
import playsound
import pygame
from dotenv import load_dotenv
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


def read_email_from_email(username,configdata):
    ORG_EMAIL=configdata['mail']['ORG_EMAIL']
    SMTP_SERVER=configdata['mail']['SMTP_SERVER']
    FROM_EMAIL=EMAIL
    FROM_PWD=PASSWORD

    storage_dir=os.path.join(PROJECT_HOME_PATH,'Data','Extract_data')

    mail=MailBox(SMTP_SERVER).login(FROM_EMAIL,FROM_PWD)

    print("email account accesss success !!")
    messages=mail.fetch(A(seen=False),mark_seen=True)
    # messages=mail.fetch(criteria=all(),mark_seen=True,bulk=False)
    print("messages are fetch successfully !!0")
    # print(messages)
    msg=list(messages)

    print(msg)
    
    count=len(msg)
    print(count)

    if count>0:
        for email in msg:
            #Get senders email address or name 
            email_holder=email.from_
            #Get the subject
            email_subject=email.subject
            #Get the email date
            ("%Y-%m-%d_%H-%M-%S")  # Format: 2024-12-07_14-30-00
            email_date=email.date.strftime("%Y-%m-%d_%H-%M-%S")
            #Get the email body
            email_body=email.text 
            #Define unique folder name to store attachments
            folder_name = f"{email_holder.replace(' ', '_').replace('@', '_').replace('.', '_')}_{email_date}"
            folder_path=os.path.join(storage_dir,folder_name)

            #create folder if it does not exit 
            os.makedirs(folder_path,exist_ok=True)

            text=f"{username} You have an Email From {email_holder} with a Subject Saying {email_subject}"

            # Loop through attachments and save them
            for att in email.attachments:
                # Get the file extension of the attachment
                file_extension = att.filename.split('.')[-1].lower()

                # Check if the attachment is a PDF, JPG, DOCX, or other allowed types
                allowed_extensions = ['pdf', 'jpg', 'jpeg', 'docx', 'png', 'xls', 'xlsx']
                if file_extension in allowed_extensions:
                    # Define the file path to save the attachment
                    file_path = os.path.join(folder_path, att.filename)

                    # Save the attachment
                    with open(file_path, 'wb') as f:
                        f.write(att.payload)
                    print(f"Attachment {att.filename} saved to {file_path}")

            speak(text)
            print(text)

    else:
        print("You Dont have any new emails !!")
        speak("You dont have nay new emails")


if __name__=='__main__':
    read_email_from_email('Shubham',config)
    # speak("heelo i am shubham")
