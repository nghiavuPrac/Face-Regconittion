import os.path
import os
pathName="Face-Regconittion\listOfUser.txt"
tempName= "Face-Regconittion\Temp.txt"
with open(pathName,'r') as reader:
    with open(tempName,'w') as writer:    
        for line in reader:
            info = line.rstrip().split(",")
            fileName = "Face-Regconittion\\FacialRecognition\\dataset\\User."+ str(info[0]) +".1.jpg"
            if(os.path.exists(fileName)):#write back to file if id have picture
                writer.write(line)

os.replace(tempName,pathName)
