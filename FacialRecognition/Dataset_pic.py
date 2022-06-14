''''
Capture multiple Faces from multiple users to be stored on a DataBase (dataset directory)
	==> Faces will be stored on a directory: dataset/ (if does not exist, pls create one)
	==> Each face will have a unique numeric integer ID as 1, 2, 3, etc                       

Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18    

'''

import cv2
import os

#path name for list of user
listOfUser_path = "Face-Regconittion\listOfUser.txt"
listNameOfImage_path ="Face-Regconittion\listOfPic.txt"


face_detector = cv2.CascadeClassifier('Face-Regconittion\FacialRecognition\haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id
def loadId_from_file(pathName):
    with open(pathName,'r') as file:
        for line in file:
            pass
        face_id= line.split(",")[0]
    return face_id
face_id = loadId_from_file(listOfUser_path)

#load file Pic_name
def load_ChoosedPic(fileName):
    try:
        listOfPic = list()
        with open(fileName,'r') as reader:
            for line in reader:
                listOfPic.append(line.rstrip())
        return listOfPic
    except:
        print("File name wasn't found!")

list_Pic = load_ChoosedPic(listNameOfImage_path) 

        

# Initialize individual sampling face count
count = 0

while(True):
    pic_name = list_Pic[count]
    img = cv2.imread(pic_name,cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(100, 100)
    )
    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1

        # Save the captured image into the datasets folder
        # need direct link path
        cv2.imwrite("Face-Regconittion\FacialRecognition\dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    print(count)
    if k == 27:
        break
    elif count >= len(list_Pic): # Take 30 face sample and stop video
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cv2.destroyAllWindows()


