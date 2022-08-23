from copy import copy
from pydoc import describe
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PIL import Image, ImageQt
import io
import base64
import util
import os


backgroundSpellIcon = Image.open("./assets/spellBackground.png")

class PerkWidget(QWidget):
    perkIconSize = 50
    spacing = 0
    def __init__(self, parent: QWidget, icon: QPixmap, titleFont: QFont, descFont: QFont, title: str, description: str):
        super(PerkWidget, self).__init__(parent)

        self.icon = icon
        self.title = title
        self.description = description

        self.style_ = "* {color: " + parent.programData["styleColor"] + "; border: 0px;}"
        self.titleFontMetrics = QFontMetrics(titleFont)
        self.descFontMetrics = QFontMetrics(descFont)

        self.iconLabel = QLabel(self)
        self.iconLabel.setPixmap(self.icon.scaled(self.perkIconSize, self.perkIconSize))
        self.iconLabel.show()

        self.titleLabel = QLabel(self)
        self.titleLabel.setFont(titleFont)
        self.titleLabel.show()

        self.descriptionLabel = QLabel(self)
        self.descriptionLabel.setFont(descFont)
        self.descriptionLabel.show()

        self.setPosition(0, 0)
        

    def setPosition(self, x: int, y: int):
        self.iconLabel.setGeometry(self.spacing, self.spacing, self.perkIconSize, self.perkIconSize)
        iconSize = self.iconLabel.pixmap().size()
        self.iconLabel.setGeometry(0, 0, iconSize.width(), iconSize.height())

        self.titleSize = self.titleFontMetrics.size(0, self.title)
        geoWidth = self.spacing + self.perkIconSize + self.spacing + self.titleSize.width() + self.spacing

        self.titleLabel.setText(self.title)
        self.titleLabel.setStyleSheet(self.style_)
        self.titleLabel.setGeometry(self.spacing + self.perkIconSize + self.spacing, self.spacing, self.titleSize.width(), self.titleSize.height())

        boundingRect = QRect(self.spacing, self.spacing + self.perkIconSize, 0, 0)
        boundingRect = self.descFontMetrics.boundingRect(boundingRect, Qt.TextWordWrap, self.description)

        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setText(self.description)
        self.descriptionLabel.setStyleSheet(self.style_)
        self.descriptionLabel.setGeometry(boundingRect)

        self.setGeometry(x, y, geoWidth, self.spacing + self.perkIconSize + self.spacing + boundingRect.height())

class SpellWidget(QWidget):
    spellSize = 35
    spacing = 17
    vertSpacing = 70

    def __init__(self, parent: QWidget, spells: list[list[dict]], textFont: QFont):
        super(SpellWidget, self).__init__(parent)

        fontMetrics = QFontMetrics(textFont)

        self.widgets: list[QWidget] = []
        self.textWidgets: list[QWidget] = []
        self.numSpells = len(spells[0])

        for i in spells:
            for j in i:
                widget = QLabel(self)
                image = Image.open("assets/" + j[0]["image"]).convert("RGBA")

                image_ = copy(backgroundSpellIcon).convert("RGBA")
                image_.paste(image, (0, 0), image)

                widget.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(image_)).scaled(self.spellSize, self.spellSize))

                self.widgets.append(widget)
                
                widget = QLabel(self)
                widget.setFont(textFont)
                widget.setText(str(j[1]))
                
                size = fontMetrics.size(0, str(j[1]))
                widget.setGeometry(0, 0, size.width(), size.height())
                widget.setStyleSheet("* {color: " + parent.programData["styleColor"] + "; border: 0px;}")

                self.textWidgets.append(widget)
                
        self.setPosition(500, 100)

    def setPosition(self, x: int, y: int):
        currentX = 5
        currentY = 5

        width = (self.spellSize + self.spacing * 2) * self.numSpells
        height = (self.spellSize + self.vertSpacing) * 2 

        for i, j in enumerate(zip(self.widgets, self.textWidgets)):
            k, l = j
            
            k.setGeometry(currentX, currentY, self.spellSize, self.spellSize)
            l.setGeometry(k.geometry().left() + self.spellSize // 2 - l.geometry().width() // 2,
                          currentY + self.spellSize + 2, l.geometry().width(), l.geometry().height())

            currentX += self.spellSize + self.spacing
            if (i + 1 == self.numSpells):
                currentY += self.vertSpacing
                currentX = 5
        self.setGeometry(x, y, width, height)

class BigWandWidget(QWidget): # I mean this shit kinda works
    def __init__(self, parent: QWidget, wand: list[dict], font: QFont):
        super(BigWandWidget, self).__init__(parent)

        image = Image.open(io.BytesIO(base64.b64decode(wand[1]))).rotate(90)
        image = image.resize((int(image.width * 6.5), int(image.height * 6.5)), Image.NEAREST)
        self.wand = QLabel(self)
        self.wand.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(image)))
        self.wand.setGeometry(0, 0, self.wand.pixmap().width(), self.wand.pixmap().height())

        wand = wand[0]
        

        metrics = QFontMetrics(font)
        self.descriptor = QLabel(self)
        self.descriptor.setFont(font)
        self.descriptor.setStyleSheet("* {color: " + parent.programData["styleColor"] + "; border: 0px;}")
        self.descriptor.setText("Shuffle: " + ("Yes" if wand["shuffle_deck_when_empty"] else "No") + "\n" + \
            "Spells/Cast: " + str(wand["actions_per_round"]) + "\n" + \
            "Cast Delay: " + str(round(wand["fire_rate_wait"] / 60, 2)) + "\n" + \
            "Recharge Time: " + str(round(wand["reload_time"] / 60, 2)) + "\n" + \
            "Mana Max: " + str(round(wand["mana_max"])) + "\n" + \
            "Mana Charge Speed: " + str(round(wand["mana_charge_speed"])) + "\n" + \
            "Capacity: " + str(int(wand["deck_capacity"])) + "\n" + \
            "Spread: " + str(round(wand["spread_degrees"], 2)))

        width = max(*[metrics.size(0, t).width() for t in self.descriptor.text().split("\n")])
        self.descriptor.setGeometry(0, 0, width, (self.descriptor.text().count("\n") + 1) * metrics.lineSpacing())
        
        numCards = 0
        pixels = 0
        spellImages = []
        currentImage = Image.new('RGBA', (0, 16))
        maxPixels = -1
        
        for i, cards in enumerate(wand["cards"]["cards"]):
            if (pixels > self.descriptor.geometry().width()):
                maxPixels = pixels
                pixels = 0 
                spellImages.append(currentImage)
                currentImage = Image.new("RGBA", (0, 16))
                
            image = Image.open("assets/" + cards["image"]).convert("RGBA")
            image_ = copy(backgroundSpellIcon).convert("RGBA")
            image_.paste(image, (0, 0), image)
            currentImage = util.get_concat_h(currentImage, image_)
            numCards += 1
            pixels += 16 * 2

        for _ in range(int(wand["deck_capacity"] - numCards)):
            currentImage = util.get_concat_h(currentImage, backgroundSpellIcon)
            if (pixels > self.descriptor.geometry().width()):
                maxPixels = pixels
                pixels = 0 
                spellImages.append(currentImage)
                currentImage = Image.new("RGBA", (0, 16))

            pixels += 16 * 2

        spellImages.append(currentImage)
        if (maxPixels == -1):
            maxPixels = pixels
        compiledImage = Image.new("RGBA", (maxPixels, 16))

        for i in spellImages:
            compiledImage = util.get_concat_v(compiledImage, i)

        compiledImage = compiledImage.resize((compiledImage.width * 2, compiledImage.height * 2), Image.NEAREST)

        self.cardWidget = QLabel(self)
        self.cardWidget.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(compiledImage)))
        self.cardWidget.setGeometry(0, 0, self.cardWidget.pixmap().width(), self.cardWidget.pixmap().height())

        
        self.setPosition(500, 20)


    def setPosition(self, x: int, y: int):
        self.descriptor.setGeometry(5, 5,
            self.descriptor.geometry().width(),
            self.descriptor.geometry().height())

        self.cardWidget.setGeometry(5, self.descriptor.geometry().bottom() + 5, self.cardWidget.geometry().width(),
            self.cardWidget.geometry().height())
        self.wand.setGeometry(self.descriptor.geometry().right() + 5, 5, self.wand.geometry().width(),
            self.wand.geometry().height())
        
        self.setGeometry(x, y, self.wand.geometry().right(), self.cardWidget.geometry().bottom())
        
        ...
    


class WandWidget(QWidget):
    spacing = 20
    vertSpacing = 2
    def __init__(self, parent: QWidget, wands: list[dict], textFont: QFont):
        super(WandWidget, self).__init__(parent)
        
        self.bigWandDrawPositionX = 0
        self.bigWandDrawPositionY = 0
        
        self.wandWidgets: list[QWidget] = []
        self.bigWandWidgets: list[QWidget] = []
        self.spellWidgets: list[QWidget] = []
        self.priceWidgets: list[QWidget] = []

        self.metrics = QFontMetrics(textFont)

        for wand, cost in wands:
            bigWand = BigWandWidget(parent, wand, textFont)
            bigWand.hide()

            self.bigWandWidgets.append(bigWand)

            b64 = wand[1]
            wand = wand[0]
            
            image = Image.open(io.BytesIO(base64.b64decode(b64))).rotate(90)
            image = image.resize((int(image.width * 3.5), int(image.height * 3.5)), Image.NEAREST) 
            
            smallPixmap = QPixmap.fromImage(ImageQt.ImageQt(image))
                    
            image = image.resize((int(image.width * 2.5), int(image.height * 2.5)), Image.NEAREST)            

            def enterEvent(_, bigWand=bigWand):
                bigWand.setPosition(self.bigWandDrawPositionX, self.bigWandDrawPositionY)
                bigWand.show()

            def leaveEvent(_, bigWand=bigWand):
                bigWand.hide()

            wand = QLabel(self)
            wand.setPixmap(smallPixmap)
            wand.enterEvent = enterEvent
            wand.leaveEvent = leaveEvent
            wand.setGeometry(0, 0, wand.pixmap().width(), wand.pixmap().height())

            text = QLabel(self)
            text.setText(str(cost))
            text.setStyleSheet("* {color: " + parent.programData["styleColor"] + "; border: 0px;}")
            text.setFont(textFont)
            boundingBox = self.metrics.size(0, str(cost))
            text.setGeometry(0, 0, boundingBox.width(), boundingBox.height())
            self.priceWidgets.append(text)
            self.wandWidgets.append(wand)


        self.setPosition(0, 0)

    def deleteLater(self) -> None:
        for i in self.bigWandWidgets:
            i.deleteLater()

        return super().deleteLater()

    def setPosition(self, x: int, y: int, maxPix: int=10000):
        width = 5
        currentX = 5
        currentY = 5

        maxY = 0
        maxX = 0

        for i in self.wandWidgets:
            maxY = max(maxY, i.geometry().height())

        for i, k in zip(self.wandWidgets, self.priceWidgets):
            if (currentX + i.geometry().width() > maxPix):
                currentX = 5
                currentY = maxY + self.metrics.lineSpacing() + 5

            y_ = maxY - i.geometry().height()
            
            i.setGeometry(currentX, currentY + y_, i.geometry().width(), i.geometry().height())

            k.setGeometry(int(currentX + i.geometry().width() / 2 - k.geometry().width() / 2 + 2),
                     i.geometry().bottom() + 5,
                     k.geometry().width(),
                     k.geometry().height())
            currentX += i.geometry().width() + self.spacing
            width += currentX + self.spacing
            maxX = max(currentX, maxX)





        self.setGeometry(x, y, maxX, maxY + self.metrics.lineSpacing() + currentY)
