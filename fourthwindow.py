# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fourthwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.



from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import os
import os.path
import os
from PIL import Image
import numpy as np
import cv2
from sympy import true
  


class Ui_fourthWindow(object):
    setPath="E:\Project Face regconition\Face-Regconittion\FacialRecognition\extra_source"
    listOfUser_path = "E:\Project Face regconition\Face-Regconittion\listOfUser.txt"
    listNameOfImage_path = "E:\Project Face regconition\Face-Regconittion\listOfPic.txt"
    images = list()

    def selectAll(self):
        self.listWidget.selectAll()
        self.item_clicked()


    def item_clicked(self):
        clicked = self.listWidget.selectedItems()
        items = []
        for i in range(len(clicked)):
            items.append(str(self.listWidget.selectedItems()[i].text()))
        self.label_2.setText("Selected: "+ str(len(items)))
        return items

    def load_ImageToListwidget(self):
        self.listWidget.clear()
        for i in range(len(self.images)):
            self.display_Items(self.images[i])

    def display_Items(self, imgPath):
        icon = QtGui.QIcon(imgPath)
        item = QtWidgets.QListWidgetItem(icon,imgPath)
        size = QtCore.QSize()
        size.setHeight(100)
        size.setWidth(400)
        item.setSizeHint(size)
        self.listWidget.setIconSize(size)
        self.listWidget.addItem(item)
    
    def get_Image(self):
        fname = QtWidgets.QFileDialog.getOpenFileNames(self.listWidget, 'Open file',self.setPath,"All Files (*);;Jpg Files (*.jpg);; PNG Files (*.png)")
        self.images.extend(fname[0])
        self.load_ImageToListwidget()
    
    def remove_Image(self):
        items = self.item_clicked()
        if len(items)>0:
            for i in items:
                self.images.remove(i)
            #reload list of images
            self.load_ImageToListwidget()

        else:
            self.infrom_message("No image was picked!")

    def infrom_message(self,message):
        imsg = QMessageBox()
        imsg.setIcon(QMessageBox.Information)
        imsg.setText(message)
        imsg.setWindowTitle("Information")
        imsg.setEscapeButton(QMessageBox.Ok)
        imsg.exec_()
    
    def warning_message(self,message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.setEscapeButton(QMessageBox.Ok)
        msg.exec_()   
    
    def remove_unused(self):
        tempName= os.getcwd()+"\Face-Regconittion\Temp.txt"
        with open(self.listOfUser_path,'r') as reader:
            with open(tempName,'w') as writer:    
                for line in reader:
                    info = line.rstrip().split(",")
                    fileName = os.getcwd()+ "\\Face-Regconittion\\FacialRecognition\\dataset\\User." + str(info[0]) +".1.jpg"
                    if(os.path.exists(fileName)):#write back to file if id have picture
                        writer.write(line)
        os.replace(tempName, self.listOfUser_path)
        

    #Check Valid(co 3 truong hop):
    #1:File khong ton tai
    #2:Trung id
    #3:Chua co ten
    #4:Chua co hinh
    def check_valid(self,id,name):
        checkId = []
        checkName =[]
        with open(self.listOfUser_path) as reader:
            for line in reader:
                info = line.rstrip().split(",")
                checkId.append(info[0])
                checkName.append(info[1].lower())
        if(id in checkId and name.lower() in checkName):
            self.warning_message("Tai khoan da duoc dang ky!\n Nhan nut 'Remove user' va quay lai de cap nhat tai khoan")
            return False
        elif(id in checkId):
            self.warning_message("Trùng id rồi kìa!\n Những id đã bị chiếm: " + str(checkId))
            return False
        else:
            return True
    
    def write_imgPathToFile(self, imgPath):
        with open(self.listNameOfImage_path,'w') as writer:
            for img in imgPath:
                writer.write(img+"\n")


        
    def train(self):
        #input
        id = self.spinBox.text()
        name = self.lineEdit.text()
        images = self.item_clicked()
        userinfo = id +","+name
        #3:Chua co ten
        if(len(name)==0):
            self.warning_message("chua nhap ten kia!")
            return 1
        
        #4:Chua chon hinh
        if(len(images)==0):
            self.warning_message("chua chon hinh kia!")
            return 1
        
        if(os.path.exists(self.listOfUser_path)):
            #remove false user id
            self.remove_unused()
            if(self.check_valid(id,name)):
                with open(self.listOfUser_path,'a') as writer:
                    writer.write(userinfo + "\n")
                self.write_imgPathToFile(images)
            else:
                return 1                

        else: #1:File khong ton tai    
            with open(self.listOfUser_path,'w') as writer:
                writer.write(userinfo + "\n")
            print(userinfo)
            self.write_imgPathToFile(images)
            
        self.infrom_message("User save successfully!\nClick 'ok' to start collect and train data!")
        self.collect_data()
        self.infrom_message("Data collect succefully!\nClick 'ok' to start training")
        self.train_model()
        self.infrom_message("Training succefully!")
        self.close() #close window when data was removed aviod error
        
    def close(self):
        for window in QtWidgets.QApplication.topLevelWindows():
            pass
        window.close()
                


    def collect_data(self):
        #need direct file path
        exec(open( "Face-Regconittion\FacialRecognition\Dataset_pic.py").read())
    
    def train_model(self):
        #need direct file path
        exec(open("Face-Regconittion\FacialRecognition\Training.py").read())
        
    
    



    def setupUi(self, fourthWindow):
        fourthWindow.setObjectName("fourthWindow")
        fourthWindow.resize(640, 480)
        self.buttonBox = QtWidgets.QDialogButtonBox(fourthWindow)
        self.buttonBox.setGeometry(QtCore.QRect(10, 440, 621, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtWidgets.QWidget(fourthWindow)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(200, 20, 431, 411))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")

        self.gridLayout.addWidget(self.label_2, 0, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget,clicked = lambda:self.train())
        self.pushButton_3.setObjectName("pushButton_3")
        
        self.gridLayout.addWidget(self.pushButton_3, 2, 3, 1, 1)
        self.listWidget = QtWidgets.QListWidget(self.gridLayoutWidget)
        self.listWidget.setMouseTracking(True)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidget.setWordWrap(True)
        self.listWidget.setObjectName("listWidget")
        #print a promt on a window
        self.listWidget.clicked.connect(self.item_clicked)


        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 4)
        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget, clicked = lambda:self.remove_Image())
        self.pushButton_4.setObjectName("pushButton_4")
        
        self.gridLayout.addWidget(self.pushButton_4, 2, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget, clicked = lambda: self.get_Image())
        self.pushButton.setMouseTracking(True)
        self.pushButton.setObjectName("pushButton")
        
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget, clicked = lambda: self.selectAll())
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 2, 1, 1, 1)
        self.verticalLayoutWidget = QtWidgets.QWidget(fourthWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 40, 160, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.spinBox = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox.setObjectName("spinBox")
        self.verticalLayout.addWidget(self.spinBox)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.label_5 = QtWidgets.QLabel(fourthWindow)
        self.label_5.setGeometry(QtCore.QRect(20, 350, 141, 121))
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")

        self.retranslateUi(fourthWindow)
        self.buttonBox.accepted.connect(lambda: self.train())
        self.buttonBox.rejected.connect(fourthWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(fourthWindow)

    def retranslateUi(self, fourthWindow):
        _translate = QtCore.QCoreApplication.translate
        fourthWindow.setWindowTitle(_translate("fourthWindow", "Dialog"))
        self.label_2.setText(_translate("fourthWindow", "Selected:" + str(self.listWidget.count())))
        self.label.setText(_translate("fourthWindow", "List of selected image"))
        self.pushButton_3.setText(_translate("fourthWindow", "Train"))
        self.pushButton_4.setText(_translate("fourthWindow", "Remove Image"))
        self.pushButton.setText(_translate("fourthWindow", "Browser Image"))
        self.pushButton_2.setText(_translate("fourthWindow", "Select all"))
        self.textBrowser.setHtml(_translate("fourthWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ff0000;\">USER INFO</span></p></body></html>"))
        self.label_4.setText(_translate("fourthWindow", "User Id:"))
        self.label_3.setText(_translate("fourthWindow", "User Name:"))
        self.label_5.setText(_translate("fourthWindow", "Note: User must select images before pushing \"Remove Image\" or \"Train\" buttons after adding them into the showing list to confirm."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    fourthWindow = QtWidgets.QDialog()
    ui = Ui_fourthWindow()
    ui.setupUi(fourthWindow)
    fourthWindow.show()
    sys.exit(app.exec_())
