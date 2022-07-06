from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from datetime import datetime

import shutil

import threading


class Backup:
    @staticmethod
    def initVariables(target):
        target.backupSize = target.buttonMetrics.size(0, "Backup")

        target.backSize = target.buttonMetrics.size(0, "Back")

        target.backupSaveButton = QPushButton(target)
        target.backupSaveButton.setToolTip("Backup current save (Game should be closed)")
        target.backupSaveButton.setText("Backup")
        target.backupSaveButton.setGeometry(5, 50, target.backupSize.width(), target.backupSize.height())
        target.backupSaveButton.setFont(QFont("Noita BlackLetter", 20))

        target.backupSaveButton.clicked.connect(target.backupCallback)

        target.backupInputLine = QLineEdit(target)
        target.backupInputLine.setFont(QFont("Noita BlackLetter", 10))
        target.backupInputLine.setStyleSheet("* {color: white; selection-background-color: orange; border: 2px solid rgb(70, 70, 70)}" + \
                                             "*:hover {background-color: rgb(50, 50, 50);}")
        backupLineShape = (225, 30)

        target.backupInputLine.setGeometry(400 - backupLineShape[0] // 2, 300 - backupLineShape[1] // 2, backupLineShape[0], backupLineShape[1])
        target.backupInputLine.returnPressed.connect(target.backupCheckStart)
        target.backupInputLine.hide()


        target.backupBackButton = QPushButton(target)
        target.backupBackButton.setFont(QFont("Noita BlackLetter", 20))
        target.backupBackButton.setText("Back")
        target.backupBackButton.setGeometry(800 - target.backSize.width() - 5, 400 - target.backSize.height() - 5,
                                            target.backSize.width(), target.backSize.height())
        target.backupBackButton.setStyleSheet("* {border: 0px; color: orange;}" + \
                                              "*:hover {background-color: rgb(50, 50, 50);}")
        target.backupBackButton.clicked.connect(target.backupBack)
        target.backupBackButton.hide()

        target.backupWarningSize = target.toolTipMetrics.size(0, "Existing backup with duplicate name.")
        target.backupDuplicateWarning = QLabel(target)
        target.backupDuplicateWarning.setFont(QFont("Noita BlackLetter", 12))
        target.backupDuplicateWarning.setText("Existing backup with duplicate name.")
        target.backupDuplicateWarning.setStyleSheet("* {color: red;}")
        target.backupDuplicateWarning.setGeometry(400 - target.backupWarningSize.width() // 2, 
                                                  target.backupInputLine.geometry().top() + target.backupInputLine.geometry().height() + 5, 
                                                  target.backupWarningSize.width(), target.backupWarningSize.height())
        target.backupDuplicateWarning.hide()



    def backupCallback(self):
        self.disableAllOptions()
        
        self.backupBackButton.show()
        self.backupInputLine.setEnabled(True)
        self.backupInputLine.setText(datetime.now().strftime("Noita Backup %m\\%d\\%Y %H:%M:%S"))
        self.backupInputLine.show()

    def backupBack(self):
        self.enableAllOptions()

        self.backupInputLine.hide()
        self.backupBackButton.hide()

    def backupCheckStart(self):
        name = self.backupInputLine.text()
        dupe = False
        self.backupDuplicateWarning.hide()
        for i in self.programData["backupData"]:
            if (self.programData["backupData"][i]["name"] == name):
                dupe = True

        if (dupe):
            self.backupDuplicateWarning.show()
        else:
            self.threadedBackupSave()
        ...
        
    def threadedBackupSave(self):
        def copySave():
            appDataPath = self.programData["appDataPath"] + "\\save00"
            self.loadingLabel.show()
            self.backupBackButton.hide()
            self.backupInputLine.setEnabled(False)

            shutil.copytree(appDataPath, "backups\\" + str(self.programData["numBackups"]))
            self.programData["backupData"][str(self.programData["numBackups"])] = {
                "path": "backups\\" + str(self.programData["numBackups"]),
                "name": self.backupInputLine.text(),
                "time": datetime.now().strftime("%m\\%d\\%Y %H:%M:%S")
            }
            self.programData["numBackups"] += 1

            self.saveData(self.programData)
            
            self.loadingLabel.hide()

            self.backupInputLine.hide()
            self.enableAllOptions()
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))


        thread = threading.Thread(target=copySave)
        thread.daemon = True
        thread.start()