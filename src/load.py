from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import threading
import shutil
import noita

class Load:
    @staticmethod
    def initVariables(target):
        target.loadSize = target.buttonMetrics.size(0, "Load")
        target.loadSaveButton = QPushButton(target)

        target.loadSaveButton.setFont(target.buttonFont)
        target.loadSaveButton.setText("Load")
        target.loadSaveButton.setGeometry(target.backupGeometry.left(), target.backupGeometry.top() + target.backupGeometry.height(),
                                    target.loadSize.width(), target.loadSize.height())
        target.loadSaveButton.clicked.connect(target.loadCallback)
        

        target.loadSaveList = QListWidget(target)
        target.loadSaveList.setGeometry(5, 25 + 5, 400, 400 - 25 - 10)
        target.loadSaveList.setStyleSheet("* {background-color: rgb(50, 50, 50); border: 2px; color: " + target.programData["styleColor"] + ";}")
        target.loadSaveList.verticalScrollBar().setStyleSheet("* {background-color: rgb(30, 30, 30);}")
        target.loadSaveList.setFont(target.toolTipFont)
        target.loadSaveList.clicked.connect(target.loadListClickedCallback)



        target.loadSaveBackButton = QPushButton(target)
        target.loadSaveBackButton.setStyleSheet("* {color: " + target.programData["styleColor"] + \
                                                "; border: 0px; background-color: rgb(40, 40, 40);}" + \
                                                "*:hover {background-color: rgb(60, 60, 60);}")

        target.loadSaveBackButton.setText("Back")
        target.loadSaveBackButton.setFont(target.buttonFont)
        target.loadSaveButton.setToolTip("Loads a stored backup (Game should be closed)")
        target.loadSaveBackButton.setGeometry(800 - target.backSize.width() - 5, 400 - target.backSize.height() - 5,
                                            target.backSize.width(), target.backSize.height())
        target.loadSaveBackButton.clicked.connect(target.loadBackCallback)
        
        target.loadSaveSelected = QPushButton(target)
        target.loadSaveSelected.setText("Load")
        target.loadSaveSelected.setFont(target.buttonFont)
        target.loadSaveSelected.setGeometry(target.loadSaveBackButton.geometry().left(),
                                          target.loadSaveBackButton.geometry().top() - target.loadSize.height() - 5, 
                                          target.loadSize.width(), target.loadSize.height())
        target.loadSaveSelected.clicked.connect(target.threadedLoadSave)

        target.deleteSize = target.buttonMetrics.size(0, "Delete")
        target.loadDeleteButton = QPushButton(target)
        target.loadDeleteButton.setFont(target.buttonFont)
        target.loadDeleteButton.setText("Delete")
        target.loadDeleteButton.setGeometry(800 - target.deleteSize.width() - 5,
                                          target.loadSaveSelected.geometry().top() - target.loadDeleteButton.geometry().height() - 5,
                                          target.deleteSize.width(), target.deleteSize.height())
        target.loadDeleteButton.clicked.connect(target.loadDeleteCallback)
        target.resetLoadSave()   

        ...

    def loadDeleteCallback(self):
        selected = self.loadSaveList.selectionModel().selectedIndexes()

        for i in selected:
            item = self.loadSaveList.takeItem(i.row())
            backupName = item.text()

            self.threadedLoadDelete(backupName)
        
            break

        self.loadSaveList.selectionModel().clear()

        
    def threadedLoadSave(self, target: str):
        selected = self.loadSaveList.selectedItems()

        backupName = None

        for i in selected:
            backupName = i.text()
            break

        
        def loadSave(target: str):
            self.loadDeleteButton.hide()
            self.loadSaveSelected.hide()
            self.loadSaveBackButton.hide()
            self.loadSaveList.setEnabled(False)
            
            self.loadingLabel.show()

            for i in self.programData["backupData"]:
                if (self.programData["backupData"][i]["name"] == target):
                    directory = self.programData["backupData"][i]["path"]

                    shutil.rmtree(self.programData["appDataPath"] + "\\save00")
                    shutil.copytree(directory, self.programData["appDataPath"] + "\\save00")
            
            self.loadDeleteButton.show()
            self.loadSaveSelected.show()
            self.loadSaveBackButton.show()
            self.loadingLabel.hide()
            self.loadSaveList.setEnabled(True)

            
        
        thread = threading.Thread(target=loadSave, args=[backupName])
        thread.daemon = True
        thread.start()
        
        self.loadSaveList.selectionModel().clear()

    def threadedLoadDelete(self, target: str):
        def deleteSave(target: str):
            self.loadDeleteButton.hide()
            self.loadSaveSelected.hide()
            self.loadSaveBackButton.hide()
            self.loadSaveList.setEnabled(False)
            
            self.loadingLabel.show()

            for i in self.programData["backupData"]:
                if (target == self.programData["backupData"][i]["name"]):
                    shutil.rmtree(self.programData["backupData"][i]["path"])
                    self.programData["backupData"].pop(i)
                    break

            self.loadingLabel.hide()

            self.loadDeleteButton.show()
            self.loadSaveSelected.show()
            self.loadSaveBackButton.show()
            self.loadSaveList.setEnabled(True)
            self.saveData(self.programData)

            self.loadSaveSelected.setStyleSheet("* {color: gray; border: 0px; background-color: rgb(40, 40, 40)}")
            self.loadDeleteButton.setStyleSheet("* {color: gray; border: 0px; background-color: rgb(40, 40, 40)}")

            self.loadSaveSelected.setEnabled(False)
            self.loadDeleteButton.setEnabled(False)

        thread = threading.Thread(target=deleteSave, args=[target])
        thread.daemon = True
        thread.start()

    def loadCallback(self):
        self.hideAllOptions()

        self.loadSaveList.clear()
        self.loadSaveList.addItem(QListWidgetItem(""))
        self.loadSaveList.show()

        for i in self.programData["backupData"]:
            self.loadSaveList.addItem(QListWidgetItem(self.programData["backupData"][i]["name"]))
        
        self.loadSaveBackButton.show()
        self.loadSaveSelected.show()
        self.loadDeleteButton.show()
    
    def loadListClickedCallback(self):
        self.loadSaveSelected.setStyleSheet("* {color: " + self.programData["styleColor"] + "; border: 0px;}" + \
                                            "*:hover {background-color: rgb(60, 60, 60);}")

        self.loadDeleteButton.setStyleSheet("* {color: " + self.programData["styleColor"] + "; border: 0px;}" + \
                                            "*:hover {background-color: rgb(60, 60, 60);}")

        self.loadDeleteButton.setEnabled(True)
        self.loadSaveSelected.setEnabled(True)
        
    def loadBackCallback(self):
        self.showAllOptions()
        self.enableAllOptions()

        self.resetLoadSave()

    def resetLoadSave(self):
        self.loadSaveList.clear()
        
        self.loadSaveSelected.setStyleSheet("* {color: gray; border: 0px; background-color: rgb(40, 40, 40)}")
        self.loadDeleteButton.setStyleSheet("* {color: gray; border: 0px; background-color: rgb(40, 40, 40)}")

        self.loadSaveSelected.setEnabled(False)
        self.loadDeleteButton.setEnabled(False)

        self.loadSaveSelected.hide()
        self.loadDeleteButton.hide()
        
        self.loadSaveBackButton.hide()
        self.loadSaveList.hide()