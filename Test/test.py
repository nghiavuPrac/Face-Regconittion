
userinfo = input("User Info: ")
id = userinfo.split(",")[0]
name = userinfo.split(",")[1]

checkId = []
checkName =[]
with open("E:\Project Face regconition\Face-Regconittion\listOfUser.txt") as reader:
    for line in reader:
        info = line.rstrip().split(",")
        checkId.append(info[0])
        checkName.append(info[1].lower())
if(id in checkId and name.lower() in checkName):
    print (3)
elif(id in checkId):
    print(2)
else:
    print(1)
