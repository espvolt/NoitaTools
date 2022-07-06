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

import backup
import load

class MainWindow(QWidget, backup.Backup, load.Load):
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

        if ("backupData" not in data):
            data["backupData"] = {}

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


        self.menuBar = QMenuBar(self)
        self.menuBar.setFont(QFont("NoitaBlackLetter", 10))

        self.menuBar.setStyleSheet("QMenuBar {color: white; font-family: Noita BlackLetter;}" + \
                                   "QMenuBar::item:selected {background-color: rgb(60, 60, 60);}")
        self.menuBar.setGeometry(0, 25, 800, 40)

        self.fileMenuButton = QMenu("File", self)
        self.fileMenuButton.setFont(QFont("NoitaBlackLetter", 10))
        self.fileMenuButton.setStyleSheet("QMenu::item {color: white; font-family: Noita BlackLetter; border: 0px}" + \
                                          "QMenu::item:selected {background-color: rgb(50, 50, 50); border: 0px}")
        self.fileMenuButton.addAction("Change AppData Path", self.changeAppDataPath)
        self.fileMenuButton.addAction("Change Game Path", self.changeGamePath)

        self.menuBar.addMenu(self.fileMenuButton)

        self.buttonMetrics = QFontMetrics(QFont("Noita BlackLetter", 20))
        self.toolTipMetrics = QFontMetrics(QFont("Noita BlackLetter", 12))

        # BACKUP STUFF

        backup.Backup.initVariables(self)
        self.backupGeometry = self.backupSaveButton.geometry()

        # LOAD STUFF
        load.Load.initVariables(self)
        
        



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

    def disableAllOptions(self):
        self.backupSaveButton.setStyleSheet("* {background-color: rgb(40, 40, 40); border: 0px; color: gray;}")
        self.backupSaveButton.setEnabled(False)

        self.loadSaveButton.setStyleSheet("* {background-color: rgb(40, 40, 40); border: 0px; color: gray;}")
        self.loadSaveButton.setEnabled(False)

    def enableAllOptions(self):
        self.backupSaveButton.setStyleSheet("* {background-color: rgb(40, 40, 40); border: 0px; color: orange;}" + \
                                            "*:hover {background-color: rgb(60, 60, 60);}")
        self.backupSaveButton.setEnabled(True)

        self.loadSaveButton.setStyleSheet("* {color: orange; border: 0px;}" + \
                                          "*:hover {background-color: rgb(60, 60, 60);}")
        self.loadSaveButton.setEnabled(True)

    def hideAllOptions(self):
        self.backupSaveButton.hide()
        self.loadSaveButton.hide()

    def showAllOptions(self):
        self.backupSaveButton.show()
        self.loadSaveButton.show()


def exceptHook(*args):

    with open("./log.txt", "w") as f:
        f.write("There was an error. Traceback: \n")
        f.write(traceback.format_tb(args[2])[0])

    sys.__excepthook__(*args)


if __name__ == "__main__":
    sys.excepthook = exceptHook

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
