# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'thirdwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.



from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
import os
from PIL import Image
import numpy as np
import cv2

from nbformat import write

class Ui_removeWindow(object):
    pathName ="Face-Regconittion\listOfUser.txt"

    def item_clicked(self):
        clicked = self.listWidget.selectedItems()
        items = []
        for i in range(len(clicked)):
            items.append(str(self.listWidget.selectedItems()[i].text()))
        self.label.setText("Click 'ok' to remove: "+ str(items))
    
    def load_items_from_file(self):
        with open(self.pathName) as reader:
            for line in reader:
                temp = line.strip()
                item = QtWidgets.QListWidgetItem(temp)
                self.listWidget.addItem(item)
        self.listWidget.sortItems()

    def remove_OnListFile(self,items):
        tempFile = "Face-Regconittion\Temp.txt"
        with open(self.pathName,'r') as reader:
            with open(tempFile,'w') as writer:
                for line in reader:
                    item = line.rstrip()
                    if item not in items:
                        writer.write(item + "\n")
        os.replace(tempFile, self.pathName)

    def remove_onDataSet(self,items):
        try:
            for item in items:
                for i in range(30):
                    pictureName =os.getcwd()+"\\Face-Regconittion\\FacialRecognition\\dataset\\User." + str(item[0]) +"."+ str(i+1) +".jpg"
                    os.remove(pictureName)
        except:
            self.warning_message("FileNotFoundError: "+ pictureName)


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

    def train_model(self):
        #need direct file path
        exec(open("Face-Regconittion\FacialRecognition\Training.py").read())


    def remove_it(self):
        clicked = self.listWidget.selectedItems()
        items = []
        for i in range(len(clicked)):
            items.append(str(self.listWidget.selectedItems()[i].text()))
        if (len(items)) > 0:
            self.remove_OnListFile(items)
            self.remove_onDataSet(items)
            self.infrom_message("Data was remove successfully!\n Click 'ok' to start retrain model")
            self.train_model()
            self.infrom_message("Retraining succefully!")    
        else:
            self.infrom_message("You didn't select any!")
        self.close() #close window when data was removed aviod error
        
    def close(self):
        for window in QtWidgets.QApplication.topLevelWindows():
            pass
        window.close()


    def setupUi(self, removeWindow):
        removeWindow.setObjectName("removeWindow")
        removeWindow.resize(241, 319)
        self.buttonBox = QtWidgets.QDialogButtonBox(removeWindow)
        self.buttonBox.setGeometry(QtCore.QRect(150, 5, 81, 61))
        self.buttonBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.buttonBox.setMouseTracking(True)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(removeWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 70, 221, 241))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.listWidget.setMouseTracking(True)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.load_items_from_file()
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(removeWindow)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 100, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        #print a promt on a window
        self.listWidget.clicked.connect(self.item_clicked)

        self.retranslateUi(removeWindow)
        self.listWidget.setCurrentRow(-1)
        self.buttonBox.accepted.connect(lambda: self.remove_it())
        self.buttonBox.rejected.connect(removeWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(removeWindow)

    def retranslateUi(self, removeWindow):
        _translate = QtCore.QCoreApplication.translate
        removeWindow.setWindowTitle(_translate("removeWindow", "Remove_User"))
        removeWindow.setAccessibleName(_translate("removeWindow", "list of user"))
        self.listWidget.setSortingEnabled(True)
        self.label.setText(_translate("removeWindow", "Total: " + str(self.listWidget.count())))
        self.label_2.setText(_translate("removeWindow", "List Of Users"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    removeWindow = QtWidgets.QDialog()
    ui = Ui_removeWindow()
    ui.setupUi(removeWindow)
    removeWindow.show()
    sys.exit(app.exec_())
