''''
Real Time Face Recogition
	==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc                       
	==> LBPH computed model (trained faces) should be on trainer/ dir
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18  

'''

import cv2
import numpy as np
import os 

pathName = "Face-Regconittion\listOfUser.txt"


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('Face-Regconittion\FacialRecognition\Trainer\Trainer.yml')
cascadePath = "Face-Regconittion\FacialRecognition\haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX
id = 0

def load_from_file(pathName):
    users = dict()
    with open(pathName,'r') as file:
        for line in file:
            user = line.rstrip().split(",")
            users[user[0]] = user[1]
    return users
names= load_from_file(pathName)

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 1080) # set video widht
cam.set(4, 720) # set video height

# Define min window size to be recognized as a face


while True:

    ret, img =cam.read()
    img = cv2.flip(img, 1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
    )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 65 ==> "0" is perfect match 
        if (confidence < 100):
            id = names[str(id)]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img)

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k==27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
