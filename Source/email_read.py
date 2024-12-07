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
        #gtts API to convert text to speech 
        tts=gTTS(text,lang='en',slow=False) 
        tts.save('output2.mp3')
        # Initialize the mixer module
        pygame.mixer.init()
        # Load the mp3 file
        pygame.mixer.music.load("output2.mp3")
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
    FROM_EMAIL=EMAIL
    # FROM_EMAIL=configdata['mail']['FROM_EMAIL']+ORG_EMAIL
    FROM_PWD=PASSWORD
    # FROM_PWD=configdata['mail']['FROM_PWD']
    SMTP_SERVER=configdata['mail']['SMTP_SERVER']
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
        text=username+", You have an Email From "+msg[0].from_+" ,with a Subject Saying "+msg[0].subject

        print(text)

        speak(text)

    else:
        print("You Dont have any new emails !!")
        speak("You dont have nay new emails")


if __name__=='__main__':
    read_email_from_email('Shubham',config)
    # speak("heelo i am shubham")
