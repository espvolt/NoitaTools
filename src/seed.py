
import base64
import io
import math
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import pymem
import util
import threading
import subprocess
import noita
import customWidgets
from PIL import Image, ImageQt

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

        target.caronSize = target.unicodeButtonMetrics.size(0, "ˇ")
        
        target.extraSeedInfoButton = QPushButton(target)
        target.extraSeedInfoButton.setStyleSheet(target.genericButtonStyle)
        target.extraSeedInfoButton.setFont(target.unicodeButtonFont)
        target.extraSeedInfoButton.setText("ˇ")
        target.extraSeedInfoButton.setGeometry(target.seedLoadLGeometry.left(), target.seedLoadLGeometry.bottom() + 5,
                                               target.caronSize.width(), target.caronSize.width() + 7)
        target.extraSeedInfoButton.clicked.connect(target.extraSeedInfoButtonCallback)

        target.extraSeedInfoInput = QLineEdit(target)
        target.extraSeedInfoInput.setGeometry(5, 55, target.seedLoadLGeometry.width(), target.seedLoadLGeometry.height())
        target.extraSeedInfoInput.setFont(target.lineFont)
        target.extraSeedInfoInput.setStyleSheet(target.genericLineStyle)
        target.extraSeedInfoInput.textChanged.connect(target.extraSeedInfoInputTextChanged)
        target.extraSeedInfoInput.hide()
        target.extraSeedInfoLGeometry = target.extraSeedInfoInput.geometry()

        target.circumflexSize = target.unicodeButtonMetrics.size(0, "ˆ")
        target.hideSeedInfoButton = QPushButton(target)
        target.hideSeedInfoButton.setStyleSheet(target.genericButtonStyle)
        target.hideSeedInfoButton.setFont(target.unicodeButtonFont)
        target.hideSeedInfoButton.setText("ˆ")
        target.hideSeedInfoButton.setGeometry(target.extraSeedInfoLGeometry.left(), target.extraSeedInfoLGeometry.bottom() + 5,
                                               target.circumflexSize.width(), target.circumflexSize.width() + 10)
        target.hideSeedInfoButton.clicked.connect(target.hideSeedButtonCallback)
        target.hideSeedInfoButton.hide()

        target.perkWidgets: list[QPushButton] = []
        target.customWidgets: list[QWidget] = []
        target.perkModifiers: dict[int, dict] = {}

        target.resetPerkVariables()

        target.perkRerollData = {}

        for i in range(7):
            target.perkRerollData[i] = 0


        target.selectedIndexes = []
        

        target.shopIndex = -1


        

        target.resetSeedMenu()

    def resetPerkVariables(self):
        for widget in self.perkWidgets:
            widget.deleteLater()

        for widget in self.customWidgets:
            widget.deleteLater()
        
        self.perkWidgets.clear()
        self.customWidgets.clear()

        for i in range(7):
            self.perkModifiers[i] = {"extraLevel": 0, "chance": 100, "displayLucky": False}


    def seedButtonCallback(self):
            
        self.hideAllOptions()
        self.resetSeedMenu()
        def setCurrentNoitaSeed():
            if (noita.isNoitaOpen()):
                self.seedSaveInput.setText(str(noita.getCurrentNoitaSeed()))

        thread = threading.Thread(target=setCurrentNoitaSeed)
        thread.daemon = True
        thread.start()

        self.seedList.addItem(QListWidgetItem("")) # why

        self.seedList.show()
        self.seedLoadButton.show()
        self.seedBackButton.show()
        self.seedSaveInput.show()
        self.seedNameSaveInput.show()
        self.seedSaveButton.show()
        self.seedLoadInput.show()
        self.seedDeleteButton.show()
        self.extraSeedInfoButton.show()
        self.hideSeedInfoButton.hide()

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

            if (lastChar.isalpha() or lastChar == " "):
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

            if (lastChar.isalpha() or lastChar == " "):
                self.seedLoadInput.setText(self.seedLoadInput.text()[:-1])
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
            util.safeDelete(self.programData["appDataPath"] + "\\save00\\world_state.xml")
            util.safeDelete(self.programData["appDataPath"] + "\\save00\\player.xml")


            with open(self.programData["gamePath"] + "\\magic.txt", "w", encoding="utf-8") as f:
                print(seed)
                f.write(f"<MagicNumbers WORLD_SEED=\"{seed}\"/>")
            
            subprocess.Popen("\"" + self.programData["gamePath"] + "\\noita.exe\" -magic_numbers magic.txt",
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

    def resetSeedMenu(self):
        self.seedList.clear()
        self.seedLoadInput.clear()
        self.seedNameSaveInput.clear()
        self.seedSaveInput.clear()
        self.extraSeedInfoInput.clear()
        self.extraSeedInfoInput.clear()


        self.seedBackButton.hide()
        self.seedLoadButton.hide()
        self.seedList.hide()
        self.seedSaveInput.hide()
        self.seedNameSaveInput.hide()
        self.seedSaveButton.hide()
        self.seedLoadInput.hide()
        self.seedDeleteButton.hide()
        self.hideSeedInfoButton.hide()
        self.extraSeedInfoInput.hide()
        self.hideSeedInfoButton.hide()
        self.extraSeedInfoButton.hide()

        self.perkWidgets.clear()
        

        self.seedSaveButton.setStyleSheet("* {color: gray; border: 0px;}")
        self.seedLoadButton.setStyleSheet("* {color: gray; border: 0px;}")
        self.seedDeleteButton.setStyleSheet("* {color: gray; border: 0px}")
        
        self.seedLoadButton.setEnabled(False)
        self.seedDeleteButton.setEnabled(False)
        self.seedSaveButton.setEnabled(False)


    def extraSeedInfoButtonCallback(self):
        self.extraSeedInfoButton.hide()
        self.seedLoadButton.hide()
        self.seedList.hide()
        self.seedSaveInput.hide()
        self.seedNameSaveInput.hide()
        self.seedSaveButton.hide()
        self.seedLoadInput.hide()
        self.seedDeleteButton.hide()
        self.hideSeedInfoButton.hide()

        self.extraSeedInfoInput.show()
        self.hideSeedInfoButton.show()

        self.extraSeedInfoInput.setText(self.seedLoadInput.text())

    def displayPerks(self, seed): # THIS IS FUCKING AWFUL :)
        perkList = noita.getPerkList(seed, self.programData["perkAssets"], [], None)

        startX = self.extraSeedInfoInput.geometry().right() + 100

        currentY = self.extraSeedInfoInput.geometry().top()

        currentIndex = 0
        buttonSize = 30
        perkRerollIndex = -1
        self.shopIndex = -1
        
        shopWidgets: list[QPushButton] = []

        for i in self.perkModifiers:
            numPerks = self.perkModifiers[i]["extraLevel"] + 3

            currentX = int(startX - buttonSize / 2 * math.sqrt((2 ** numPerks))) # Needs work
            rerollPerks = None
            perkLuckyData = noita.getPerkLucky(seed, self.perkModifiers[i]["chance"], self.perkModifiers[i]["extraLevel"], i)

            if (self.perkRerollData[i] != 0):
                for _ in range(self.perkRerollData[i]):
                    data = noita.perkReroll(seed, self.programData["perkAssets"], numPerks, 0, perkRerollIndex)

                    perkRerollIndex = data["rerollIndex"]
                    rerollPerks = data["perks"]

            for j in range(numPerks):
                currentPerk = perkList[currentIndex]
                currentPerkData = None
                tempIndex = currentIndex

                if (rerollPerks is not None):
                    currentPerk = rerollPerks[j]
                    currentIndex = perkRerollIndex + 3 - j

                for k in self.programData["perkAssets"]:
                    if (k["id"] == currentPerk):
                        currentPerkData = k
                        break
                
                button = QPushButton(self)

                if (currentIndex in self.selectedIndexes): # if currentPerk has been selected
                    color = QColor(self.programData["styleColor"])
                    asArr = [color.red() - 50, color.green() - 50, color.blue() - 50]
                    asArrStr = [str(max(0, i)) for i in asArr]
                    colorString = "rgb(" + ", ".join(asArrStr) + ")"

                    button.setStyleSheet("* {background-color: " + self.programData["styleColor"] + "; border: 0px;}" + \
                                        "*:hover {background-color: " + colorString + ";}")

                    if (currentPerkData["id"] == "EXTRA_PERK"):
                        self.perkModifiers[i]["extraLevel"] += 1
                    
                    if (currentPerkData["id"] == "PERKS_LOTTERY"):
                        self.perkModifiers[i]["chance"] -= 50
                        self.perkModifiers[i]["displayLucky"] = True
                        perkLuckyData = noita.getPerkLucky(seed, self.perkModifiers[i]["chance"], self.perkModifiers[i]["extraLevel"], i) # THIS CODE IS SO BAD :))

                else:
                    button.setStyleSheet(self.genericButtonStyle)

                button.setGeometry(currentX, currentY, buttonSize, buttonSize)
                if (not self.perkModifiers[i]["displayLucky"]):
                    button.setIcon(QIcon(QPixmap("assets/" + currentPerkData["image"]).scaled(99, 99)))
                else:
                    if (perkLuckyData[j]):
                        button.setIcon(QIcon(noita.addLuckyIcon("assets/" + currentPerkData["image"],
                                                        "assets/data/ui_gfx/perk_icons/perks_lottery.png", (50, 50)).scaled(99, 99)))
                    else:
                        button.setIcon(QIcon(QPixmap("assets/" + currentPerkData["image"]).scaled(99, 99)))

                button.setIconSize(QSize(34, 34))

                def buttonCallback(_, index=currentIndex):
                    if (index in self.selectedIndexes):
                        self.selectedIndexes.remove(index)
                    else:
                        self.selectedIndexes.append(index)

                    self.resetPerkVariables()

                    self.displayPerks(seed) # redraws the perks
                
                icon = QPixmap("assets/" + currentPerkData["image"])
                customWidget = customWidgets.PerkWidget(self, icon, self.perkTitleFont, self.perkDescriptionFont,
                    currentPerkData["name"], "PlaceHolder")


                def enterEvent(_, customWidget=customWidget):
                    if (self.shopIndex == -1):
                        customWidget.show()
                    

                def leaveEvent(_, customWidget=customWidget):
                    customWidget.hide()

                customWidget.setPosition(5, self.hideSeedInfoButton.geometry().bottom() - 10)

                button.enterEvent = enterEvent
                button.leaveEvent = leaveEvent
                button.clicked.connect(buttonCallback)
                button.show()

                if (rerollPerks is not None):
                    currentIndex = tempIndex

                currentX += buttonSize + 5

                self.perkWidgets.append(button)
                rerollButton = QPushButton(self)

                def rerollButtonCallback(event, but=rerollButton, level=i):
                    if (event.button() == 1):
                        self.perkRerollData[level] += 1

                    if (event.button() == 2):
                        self.perkRerollData[level] = max(0, self.perkRerollData[level] - 1)

                    self.resetPerkVariables()
                    self.displayPerks(seed)
                    

                rerollButton.setStyleSheet(self.genericButtonStyle)
                rerollButton.setIcon(QIcon(QPixmap("assets/rerollIcon.png").scaled(99, 99)))
                rerollButton.setIconSize(QSize(buttonSize, buttonSize))
                rerollButton.setGeometry(currentX, currentY, buttonSize, buttonSize)
                rerollButton.mousePressEvent = rerollButtonCallback
                rerollButton.show()
                self.perkWidgets.append(customWidget)
                self.perkWidgets.append(rerollButton)
                currentIndex += 1
            
            if (i < 6):
                self.perkModifiers[i + 1]["extraLevel"] = self.perkModifiers[i]["extraLevel"]
                self.perkModifiers[i + 1]["chance"] = self.perkModifiers[i]["chance"]
                self.perkModifiers[i + 1]["displayLucky"] = self.perkModifiers[i]["displayLucky"]
            currentY += buttonSize + 5

        currentY = self.extraSeedInfoInput.geometry().top()
        currentX += buttonSize + 5
        
        for i in range(7):
            shop, shopType = noita.getShop(self.filteredSpellData, seed, i, 5)
            shopButton = QPushButton(self)
            shopButton.setGeometry(currentX, currentY, buttonSize, buttonSize)
            shopButton.setStyleSheet(self.genericButtonStyle)
            customWidget = None
            if (shopType == 1): # Spell Shop
                firstIcon = "assets/" + shop[0][0][0]["image"]
                shopButton.setIcon(QIcon(QPixmap(firstIcon).scaled(50, 50)))

                customWidget = customWidgets.SpellWidget(self, shop, self.perkDescriptionFont)
                customWidget.setPosition(5, self.hideSeedInfoButton.geometry().bottom() - 10)
                
                def clicked(_, shop=shop, widget=customWidget, shopIndexClicked=i):
                    if (self.shopIndex == -1):
                        self.shopIndex = shopIndexClicked
                        widget.show()

                    elif (self.shopIndex == shopIndexClicked):
                        self.shopIndex = -1
                        widget.hide()

                    else:
                        shopWidgets[self.shopIndex].click()
                        self.shopIndex = shopIndexClicked
                        widget.show()

                shopButton.clicked.connect(clicked)


            else:
                image = Image.open(io.BytesIO(base64.b64decode(shop[0][0][1])))
                qtImage = ImageQt.ImageQt(image)
                shopButton.setIcon(QIcon(QPixmap.fromImage(qtImage).scaled(50, 50)))
                image.close()

                customWidget = customWidgets.WandWidget(self, shop, self.perkDescriptionFont)
                customWidget.setPosition(5, self.hideSeedInfoButton.geometry().bottom() - 10, self.extraSeedInfoInput.geometry().width() - 5)
                customWidget.bigWandDrawPositionX = currentX + buttonSize + 5
                customWidget.bigWandDrawPositionY = self.extraSeedInfoInput.geometry().top()
                

                def clicked(_, shop=shop, widget=customWidget, shopIndexClicked=i):
                    if (self.shopIndex == -1):
                        self.shopIndex = shopIndexClicked
                        widget.show()

                    elif (self.shopIndex == shopIndexClicked):
                        self.shopIndex = -1
                        widget.hide()

                    else:
                        shopWidgets[self.shopIndex].click()
                        self.shopIndex = shopIndexClicked
                        widget.show()

                shopButton.clicked.connect(clicked)


                


            shopButton.show()
            self.perkWidgets.append(customWidget)
            self.perkWidgets.append(shopButton)
            shopWidgets.append(shopButton)
            currentY += buttonSize + 5




    def extraSeedInfoInputTextChanged(self):
        if (self.extraSeedInfoInput.text() == ""):
            self.resetPerkVariables()
            ...
        
        else:
            lastChar = self.extraSeedInfoInput.text()[-1]

            if (lastChar.isalpha() or lastChar == " "):
                self.extraSeedInfoInput.setText(self.extraSeedInfoInput.text()[:-1])

            self.resetPerkVariables()

            self.perkWidgets.clear()
            self.displayPerks(int(self.extraSeedInfoInput.text()))

    def hideSeedButtonCallback(self):
        text = self.extraSeedInfoInput.text()
        self.resetSeedMenu()
        self.seedButtonCallback()
        self.seedLoadInput.setText(text)
        

            



        