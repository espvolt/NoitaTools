from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class CustomBar(QWidget):
    def __init__(self, parent):
        super(CustomBar, self).__init__()
        self.parent: QWidget = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.title = QLabel("NoitaTools")
        self.title.setFont(QFont("Noita BlackLetter", 16))

        btn_size = 25

        self.btn_close = QPushButton("x")
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size,btn_size)
        self.btn_close.setStyleSheet("background-color: rgb(30, 30, 30); border: 0px; color: white;")

        self.btn_min = QPushButton("-")
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size, btn_size)
        self.btn_min.setStyleSheet("background-color: rgb(30, 30, 30); border: 0px; color: white;")

        self.title.setFixedHeight(25)
        
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_close)

        self.title.setStyleSheet("""
            background-color: rgb(30, 30, 30);
            color: white;
        """)
        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False
        self.max = False

        

    def resizeEvent(self, event: QResizeEvent):
        super(CustomBar, self).resizeEvent(event)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event: QMouseEvent):
        self.start = self.mapToGlobal(event.pos())
        self.parent.resize(800, 400)
        self.max = False
        self.pressing = True

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, _: QMouseEvent):
        self.pressing = False


    def btn_close_clicked(self):
        self.parent.close()

    def btn_min_clicked(self):
        self.parent.showMinimized()
