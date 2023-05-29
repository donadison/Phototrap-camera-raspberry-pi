import os
import RPi.GPIO as GPIO
from gpiozero import MotionSensor
import time
import picamera
from gpiozero import MotionSensor
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from time import sleep
import smtplib
import ssl
from email.message import EmailMessage


#to sending email we must define few things. It is very intuitive
sender_email="PHOTOTRAP@gmail.com"
rec_email="YOOURMAIL@gmail.com"

#THIS ISINT PASSWOR TO YOUR EMAIL!!!! This is specific password for "apps". We can get this if we have 2step verification on google account
#link to make this password is in readme!!!
password="16CHARPASSWORDFROMGOOGLE"
message="Zarejestrowano ruch"
#time for email
timer = time.strftime("%Y %m %d - %H %M %S")


#body of our email message
body= timer + """

Nowe nagranie z fotopulapki jest zarejestrowane i przeslane na dysk google

"""


#forming of email
em= EmailMessage()
em['From']=sender_email
em['To']=rec_email
em['Subject']=message
em.set_content(body)

#ssl security
context= ssl.create_default_context()


#gauth is for sending files to our google drive. Congiguration of this file will be add in readme. You must have few files which are
#generating after making project on google account with their api
settings='/home/pi/Desktop/settings.yaml'
gauth = GoogleAuth(settings)
gauth.LocalWebserverAuth()
#this will add necesary .json file
#gauth.SaveCredentialsFile('./cred.json')
drive = GoogleDrive(gauth)
#link to folder of my google account
folder ='GDRIVEFOLDERLINK'


#INITIALIZAITON OF MOTION SENSOR ON GPIO21
pir = MotionSensor(21)

# path to records
folder_path = os.path.expanduser("~/Desktop/records")

# cheking of folder with records
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

#picamera initialization
camera = picamera.PiCamera()
camera.rotation = 180

# function of motion detectior
def motion_detected(channel):
    print("wykryto ruch")
    #timestamp for filename
    timestamp = time.strftime("%Y_%m_%d-%H.%M.%S")
    filename = "motion_{}.h264".format(timestamp)
    
    # path to our folder and filename for new record
    file_path = os.path.join(folder_path, filename)
    
    # picamera 15 seconds record
    camera.start_recording(file_path)
    time.sleep(15)
    camera.stop_recording()
    

    
    #gdrive sending files
    file_drive = drive.CreateFile({'title': filename, 'parents': [{'id': folder}]})
    file_drive.SetContentFile(file_path)
    file_drive.Upload()
    

    #email sending
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, password)
        smtp.sendmail(sender_email, rec_email, em.as_string())

#if we have motion it starts recording
pir.when_motion=motion_detected


try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Manualnie przerwano program.")

finally:
    camera.close()