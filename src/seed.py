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

class Seed:
    staticmethod
    def initVariables(target):
        target.seedSize = target.buttonMetrics.size(0, "Seed")
        target.seedButton = QPushButton(target)
        target.seedButton.setFont(target.buttonFont)
        target.seedButton.setText("Seed")
        target.seedButton.setStyleSheet(target.genericButtonStyle)
        target.seedButton.setGeometry(target.loadGeometry.left(), target.loadGeometry.top() + target.loadGeometry.height() + 5,
                                    target.seedSize.width(), target.seedSize.height())
        target.seedButton.clicked.connect(target.seedButtonCallback)

        target.seedList = QListWidget(target)
        target.seedList.setGeometry(5, 25 + 5, 400, 400 - 25 - 10)
        target.seedList.setStyleSheet("* {background-color: rgb(50, 50, 50); border: 2px; color: " + target.programData["styleColor"] + ";}")
        target.seedList.verticalScrollBar().setStyleSheet("* {background-color: rgb(30, 30, 30);}")
        target.seedList.setFont(QFont("Noita BlackLetter", 12))
        target.seedList.clicked.connect(target.seedListClickedCallback)
        target.seedList.hide()

        target.seedBackButton = QPushButton(target)
        target.seedBackButton.setFont(target.buttonFont)
        target.seedBackButton.setText("Back")
        target.seedBackButton.setGeometry(800 - target.backSize.width() - 5, 400 - target.backSize.height() - 5,
                                        target.backSize.width(), target.backSize.height())
        target.seedBackButton.setStyleSheet(target.genericButtonStyle)
        target.seedBackButton.hide()
        target.seedBackButton.clicked.connect(target.seedBackCallback)

        target.seedSaveInput = QLineEdit(target)
        target.seedSaveInput.setStyleSheet("* {color: white; selection-background-color: " + target.programData["styleColor"] + \
                                             "; border: 2px solid rgb(70, 70, 70)}" + \
                                             "*:hover {background-color: rgb(50, 50, 50);}")
        target.seedSaveInput.setFont(target.lineFont)
        target.seedSaveInput.setGeometry(410, 50 + 5, 250, 30)
        target.seedSaveInput.setToolTip("Save Seed (Seed)")
        target.seedSaveInput.textChanged.connect(target.seedSaveTextChanged)

        target.seedNameSaveInput = QLineEdit(target)
        target.seedNameSaveInput.setStyleSheet("* {color: white; selection-background-color: " + target.programData["styleColor"] + \
                                             "; border: 2px solid rgb(70, 70, 70)}" + \
                                             "*:hover {background-color: rgb(50, 50, 50);}")
        target.seedNameSaveInput.setFont(target.lineFont)
        target.seedNameSaveInput.setGeometry(410, 50 + 30 + 10, 250, 30)
        target.seedNameSaveInput.setToolTip("Save Seed (Name)")

        target.saveSize = target.buttonMetrics.size(0, "Save")
        target.seedNameGeometry = target.seedNameSaveInput.geometry()
        target.seedSaveButton = QPushButton(target)
        target.seedSaveButton.setFont(target.buttonFont)
        target.seedSaveButton.setText("Save")
        target.seedSaveButton.setStyleSheet(target.genericButtonStyle)
        target.seedSaveButton.setGeometry(target.seedNameGeometry.left() + target.seedNameGeometry.width() + 5,
                                        target.seedNameGeometry.top() + target.seedNameGeometry.height() - target.saveSize.height(),
                                        target.saveSize.width(), target.saveSize.height())
        target.seedSaveButton.clicked.connect(target.seedSaveButtonCallback)
        
        target.seedLoadInput = QLineEdit(target)
        target.seedLoadInput.setStyleSheet("* {color: white; selection-background-color: " + target.programData["styleColor"] + \
                                             "; border: 2px solid rgb(70, 70, 70)}" + \
                                             "*:hover {background-color: rgb(50, 50, 50);}")
        target.seedLoadInput.setGeometry(410, 250, 250, 30)
        target.seedLoadInput.setFont(target.lineFont)
        target.seedLoadInput.textChanged.connect(target.seedLoadTextChanged)
        
        target.seedLoadLGeometry = target.seedLoadInput.geometry()

        target.seedLoadButton = QPushButton(target)
        target.seedLoadButton.setFont(target.buttonFont)
        target.seedLoadButton.setText("Load")
        target.seedLoadButton.setGeometry(target.seedLoadLGeometry.left() + target.seedLoadLGeometry.width() + 5,
                                        target.seedLoadLGeometry.top() + target.seedLoadLGeometry.height() - target.loadSize.height(),
                                        target.loadSize.width(), target.loadSize.height())
        target.seedLoadButton.setStyleSheet(target.genericButtonStyle)
        target.seedLoadButton.clicked.connect(target.seedLoadButtonCallback)
        target.seedLoadButton.hide()

        target.seedLoadBGeometry = target.seedLoadButton.geometry()

        target.seedDeleteButton = QPushButton(target)
        target.seedDeleteButton.setFont(target.buttonFont)
        target.seedDeleteButton.setText("Delete")
        target.seedDeleteButton.setGeometry(target.seedLoadBGeometry.left(), target.seedLoadBGeometry.top() + target.seedLoadBGeometry.height() + 5,
                                          target.deleteSize.width(), target.deleteSize.height())
        target.seedDeleteButton.setStyleSheet(target.genericButtonStyle)
        target.seedDeleteButton.clicked.connect(target.seedDeleteButtonCallback)



        target.resetSeedMenu()

    def seedButtonCallback(self):
        self.hideAllOptions()
        self.resetSeedMenu()
        
        self.seedList.addItem(QListWidgetItem("")) # why

        self.seedList.show()
        self.seedLoadButton.show()
        self.seedBackButton.show()
        self.seedSaveInput.show()
        self.seedNameSaveInput.show()
        self.seedSaveButton.show()
        self.seedLoadInput.show()
        self.seedDeleteButton.show()

        for seed in self.programData["seeds"]:
            item = QListWidgetItem(self.programData["seeds"][seed])
            item.setToolTip(seed)
            self.seedList.addItem(item)
    
    
    def seedListClickedCallback(self):
        selected = self.seedList.selectedItems()[0]
        
        for i in self.programData["seeds"]:            
            if (selected.text() == self.programData["seeds"][i]):
                self.seedLoadInput.setText(i)
                self.seedDeleteButton.setStyleSheet(self.genericButtonStyle)
                self.seedDeleteButton.setEnabled(True)
                break

                
    def seedSaveButtonCallback(self):
        seedText = self.seedLoadInput.text()

        self.programData["seeds"][self.seedSaveInput.text()] = self.seedNameSaveInput.text()
        self.saveData(self.programData)
        self.resetLoadSave()
        self.seedButtonCallback()
        self.seedLoadInput.setText(seedText)

    def seedBackCallback(self):
        self.resetSeedMenu()
        self.showAllOptions()

    def seedDeleteButtonCallback(self):
        selected = self.seedList.selectedIndexes()

        for i in selected:
            item = self.seedList.takeItem(i.row())

            for i in self.programData["seeds"]:
                if (self.programData["seeds"][i] == item.text()):
                    self.programData["seeds"].pop(i)
                    break
        self.saveData(self.programData)
        self.seedList.selectionModel().clear()

    def seedSaveTextChanged(self):
        if (self.seedSaveInput.text() == ""):
            self.seedSaveButton.setEnabled(False)
            self.seedSaveButton.setStyleSheet("* {color: gray; border: 0px}")
        else:
            lastChar = self.seedSaveInput.text()[-1]

            if (lastChar.isalpha()):
                self.seedSaveInput.setText(self.seedSaveInput.text()[:-1])
            else:
                self.seedSaveButton.setEnabled(True)
                self.seedSaveButton.setStyleSheet(self.genericButtonStyle)
    
    def seedLoadTextChanged(self):
        if (self.seedLoadInput.text() == ""):
            self.seedLoadButton.setEnabled(False)
            self.seedLoadButton.setStyleSheet("* {color: gray; border: 0px}")
        else:
            lastChar = self.seedLoadInput.text()[-1]

            if (lastChar.isalpha()):
                self.seedLoadInput.setText(self.seedSaveInput.text()[:-1])
            else:
                self.seedLoadButton.setEnabled(True)
                self.seedLoadButton.setStyleSheet(self.genericButtonStyle)

    def seedLoadButtonCallback(self):
        def loadSeed(seed):
            self.seedLoadInput.hide()
            self.seedBackButton.hide()
            self.seedLoadButton.hide()
            self.seedNameSaveInput.hide()
            self.seedSaveInput.hide()
            self.seedSaveButton.hide()
            self.seedDeleteButton.hide()
            self.seedList.setEnabled(False)

            self.loadingLabel.show()

            util.safeDelete(self.programData["appDataPath"] + "\\save00\\world")
            util.safeDelete(self.programData["appDataPath"] + "\\save00\\mod_config.xml")
            util.safeDelete(self.programData["appDataPath"] + "\\save00\\world_state.xml")
            util.safeDelete(self.programData["appDataPath"] + "\\save00\\player.xml")


            with open(self.programData["gamePath"] + "\\magic.txt", "w", encoding="utf-8") as f:
                print(seed)
                f.write(f"<MagicNumbers WORLD_SEED=\"{seed}\"/>")
            
            subprocess.Popen("\"" + self.programData["gamePath"] + "\\noita.exe\" -no_logo_splashes -magic_numbers magic.txt",
                             cwd=self.programData["gamePath"])

            self.seedLoadInput.show()
            self.seedBackButton.show()
            self.seedLoadButton.show()
            self.seedNameSaveInput.show()
            self.seedSaveInput.show()
            self.seedSaveButton.show()
            self.seedDeleteButton.show()
            self.seedList.setEnabled(True)

            self.loadingLabel.hide()





        seed = self.seedLoadInput.text()

        if (seed != ""):
            thread = threading.Thread(target=loadSeed, args=[seed])
            thread.daemon = True
            thread.start()

        ...


    def resetSeedMenu(self):
        self.seedList.clear()
        self.seedLoadInput.clear()
        self.seedNameSaveInput.clear()
        self.seedSaveInput.clear()
        
        self.seedBackButton.hide()
        self.seedLoadButton.hide()
        self.seedList.hide()
        self.seedSaveInput.hide()
        self.seedNameSaveInput.hide()
        self.seedSaveButton.hide()
        self.seedLoadInput.hide()
        self.seedDeleteButton.hide()

        self.seedSaveButton.setStyleSheet("* {color: gray; border: 0px;}")
        self.seedLoadButton.setStyleSheet("* {color: gray; border: 0px;}")
        self.seedDeleteButton.setStyleSheet("* {color: gray; border: 0px}")
        
        self.seedLoadButton.setEnabled(False)
        self.seedDeleteButton.setEnabled(False)
        self.seedSaveButton.setEnabled(False)