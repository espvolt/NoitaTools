import sys
import traceback

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pkg_resources import FileMetadata
from datetime import datetime
from custom_bar import CustomBar

import noita
import util
import json
import threading
import shutil
import os
import re
import subprocess

import backup
import load
import seed

class MainWindow(QWidget, backup.Backup, load.Load, seed.Seed):
    def initData(self):
        data = util.safeReadJson("./data.json", dict)

        if ("appDataPath" not in data):
            appDataPath = noita.noitaAppDataPath()
            data["appDataPath"] = appDataPath

        if ("gamePath" not in data):
            steamPath = noita.noitaSteamPath()

            if (steamPath != None):
                data["gamePath"] = steamPath

        if ("numBackups" not in data):
            data["numBackups"] = 0

        if ("styleColor" not in data):
            data["styleColor"] = "orange"
        
        if ("backupData" not in data):
            data["backupData"] = {}
        
        if ("seeds" not in data):
            data["seeds"] = {}

        if (not os.path.exists("./backups")):
            os.mkdir("backups")

        self.cleanData(data)
        self.saveData(data)

        return data

    def cleanData(self, data):
        backupPops = []
        for i in data["backupData"]:
            if (not os.path.exists(data["backupData"][i]["path"])):
                backupPops.append(i)

        for pop in backupPops:
            data["backupData"].pop(pop)

    def saveData(self, data):
        with open("./data.json", "w") as f:
            json.dump(data, f, indent=4)

    def __init__(self):
        super(MainWindow, self).__init__()

        self.programData = self.initData()

        fontDB = QFontDatabase()
        fontDB.addApplicationFont("./assets/NoitaBlackLetter.ttf")

        self.layout  = QVBoxLayout()
        self.layout.addWidget(CustomBar(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addStretch(-1)
        self.setMinimumSize(800,400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        self.pressing = False

        self.setStyleSheet("background-color: rgb(40, 40, 40);")

        self.loadingMovie = QMovie("./assets/loading.gif")
        self.loadingMovie.setScaledSize(QSize(32, 32))
        self.loadingMovie.start()

        self.loadingLabel = QLabel("", self)
        self.loadingLabel.setGeometry(800 - 32 - 5, 400 - 32 - 5, 32, 32)

        self.loadingLabel.setMovie(self.loadingMovie)
        self.loadingLabel.hide()

        self.buttonMetrics = QFontMetrics(QFont("Noita BlackLetter", 20))
        self.toolTipMetrics = QFontMetrics(QFont("Noita BlackLetter", 12))

        self.buttonFont = QFont("Noita BlackLetter", 20)
        self.toolTipFont = QFont("Noita BlackLetter", 12)
        self.lineFont = QFont("Noita BlackLetter", 10)

        self.genericButtonStyle = "* {color: " + self.programData["styleColor"] + "; border: 0px;}" + \
                                  "*:hover {background-color: rgb(60, 60, 60);}"

        # BACKUP STUFF

        backup.Backup.initVariables(self)
        self.backupGeometry = self.backupSaveButton.geometry()

        # LOAD STUFF

        load.Load.initVariables(self)
        self.loadGeometry = self.loadSaveButton.geometry()

        # SEED 
        
        seed.Seed.initVariables(self)
        
        

        # END

        self.menuBar = QMenuBar(self)
        self.menuBar.setFont(QFont("NoitaBlackLetter", 10))

        self.menuBar.setStyleSheet("QMenuBar {color: white; font-family: Noita BlackLetter;}" + \
                                   "QMenuBar::item:selected {background-color: rgb(60, 60, 60);}")
        self.menuBar.setGeometry(0, 25, 800, 30)

        self.fileMenuButton = QMenu("File", self)
        self.fileMenuButton.setFont(QFont("NoitaBlackLetter", 10))
        self.fileMenuButton.setStyleSheet("QMenu::item {color: white; font-family: Noita BlackLetter; border: 0px}" + \
                                          "QMenu::item:selected {background-color: rgb(50, 50, 50); border: 0px}")
        self.fileMenuButton.addAction("Change AppData Path", self.changeAppDataPath)
        self.fileMenuButton.addAction("Change Game Path", self.changeGamePath)

        self.menuBar.addMenu(self.fileMenuButton)

        self.optionsMenuButton = QMenu("Options", self)
        self.optionsMenuButton.setFont(QFont("NoitaBlackLetter", 10))
        self.optionsMenuButton.setStyleSheet("QMenu::item {color: white; font-family: Noita BlackLetter; border: 0px}" + \
                                             "QMenu::item:selected {background-color: rgb(50, 50, 50); border: 0px}")
        self.optionsMenuButton.addAction("Change Style Color (Restart)", self.changeStyleColor)
        
        # CHANGE COLOR STUFF

        changeColorLineShape = (225, 30)
        
        self.changeColorLine = QLineEdit(self)
        self.changeColorLine.setFont(QFont("Noita BlackLetter", 10))
        self.changeColorLine.setStyleSheet("* {color: white; selection-background-color: " + self.programData["styleColor"] + \
                                             "; border: 2px solid rgb(70, 70, 70)}" + \
                                             "*:hover {background-color: rgb(50, 50, 50);}")

        self.changeColorLine.setGeometry(400 - changeColorLineShape[0] // 2, 300 - changeColorLineShape[1] // 2,
                                           changeColorLineShape[0], changeColorLineShape[1])
        self.changeColorLine.returnPressed.connect(self.saveNewColor)
        self.changeColorLine.hide()

        self.changeColorBackButton = QPushButton(self)
        self.changeColorBackButton.setText("Back")
        self.changeColorBackButton.setFont(QFont("Noita BlackLetter", 20))
        self.changeColorBackButton.setGeometry(800 - self.backSize.width() - 5, 400 - self.backSize.height() - 5,
                                            self.backSize.width(), self.backSize.height())
        self.changeColorBackButton.clicked.connect(self.changeColorBack)
        self.changeColorBackButton.setStyleSheet(self.genericButtonStyle)
        self.changeColorBackButton.hide()

        self.menuBar.addMenu(self.optionsMenuButton)        
        # END

        self.enableAllOptions()

    def changeAppDataPath(self):
        self.programData["appDataPath"] = QFileDialog.getExistingDirectory(self, "Noita AppData Directory",
                                             self.programData["appDataPath"] if self.programData["appDataPath"] is not None else "C:",
                                             QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

        self.saveData(self.programData)

    def changeGamePath(self):
        self.programData["gamePath"] = QFileDialog.getExistingDirectory(self, "Noita Game Directory",
                                             self.programData["gamePath"] if self.programData["gamePath"] is not None else "C:",
                                             QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        
        self.saveData(self.programData)

    def changeStyleColor(self):
        self.disableAllOptions()
        self.showAllOptions()

        self.hideOptionWidgets()

        self.changeColorLine.show()
        self.changeColorBackButton.show()

    def saveNewColor(self):
        text = self.changeColorLine.text()
        self.changeColorLine.clear()
        self.changeColorBack()

        self.programData["styleColor"] = text
        self.saveData(self.programData)

    def changeColorBack(self):
        self.enableAllOptions()
        self.changeColorLine.hide()
        self.changeColorBackButton.hide()

    def disableAllOptions(self):
        self.backupSaveButton.setStyleSheet("* {background-color: rgb(40, 40, 40); border: 0px; color: gray;}")
        self.backupSaveButton.setEnabled(False)

        self.loadSaveButton.setStyleSheet("* {background-color: rgb(40, 40, 40); border: 0px; color: gray;}")
        self.loadSaveButton.setEnabled(False)

        self.seedButton.setStyleSheet("* {background-color: rgb(40, 40, 40); border: 0px; color: gray;}")
        self.seedButton.setEnabled(False)

    def enableAllOptions(self):
        self.backupSaveButton.setStyleSheet("* {background-color: rgb(40, 40, 40); border: 0px; color: " + self.programData["styleColor"] + \
                                            ";}" + \
                                            "*:hover {background-color: rgb(60, 60, 60);}")
        self.backupSaveButton.setEnabled(True)

        self.loadSaveButton.setStyleSheet("* {color: " + self.programData["styleColor"] + "; border: 0px;}" + \
                                          "*:hover {background-color: rgb(60, 60, 60);}")
        self.loadSaveButton.setEnabled(True)

        self.seedButton.setStyleSheet("* {color: " + self.programData["styleColor"] + "; border: 0px;}" + \
                                          "*:hover {background-color: rgb(60, 60, 60);}")
        self.seedButton.setEnabled(True)


    def hideOptionWidgets(self):
        self.backupBackButton.hide()
        self.backupInputLine.hide()

        self.loadSaveList.hide()
        self.loadSaveSelected.hide()
        self.loadDeleteButton.hide()
        self.loadSaveBackButton.hide()

        self.seedBackButton.hide()
        self.seedLoadButton.hide()
        self.seedList.hide()
        self.seedSaveInput.hide()
        self.seedNameSaveInput.hide()
        self.seedSaveButton.hide()
        self.seedLoadInput.hide()
        self.seedDeleteButton.hide()


    def hideAllOptions(self):
        self.backupSaveButton.hide()
        self.loadSaveButton.hide()
        self.seedButton.hide()

    def showAllOptions(self):
        self.backupSaveButton.show()
        self.loadSaveButton.show()
        self.seedButton.show()

    
        
    



def exceptHook(*args):
    with open("./log.txt", "w") as f:
        f.write("There was an error. Traceback: \n\n")
        f.write("".join(traceback.format_exception(args[1])))

    sys.__excepthook__(*args)

if __name__ == "__main__":
    sys.excepthook = exceptHook
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()
    
    app.setWindowIcon(QIcon("./assets/icon.ico"))
    app.exec_()
    

