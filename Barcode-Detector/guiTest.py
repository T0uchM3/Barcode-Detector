import sys
import os
import cv2
from PySide2.QtWidgets import QApplication, QWidget
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import QUiLoader
from PIL import Image
from PySide2.QtWidgets import *
import pyzbar.pyzbar as zbar

class MainWidget(QWidget):    
    def __init__(self):
        QWidget.__init__(self)

        full_path = os.path.realpath(__file__)
        path, filename = os.path.split(full_path)
        designer_file = QFile(path + "\\form.ui")
        designer_file.open(QFile.ReadOnly)

        self.setWindowFlags(Qt.CustomizeWindowHint)
        loader = QUiLoader()
        self.ui = loader.load(designer_file, self)
        self.center()#position the window in the center
        
        #w = QtWidgets.QDialog()
        #w.setSizeGripEnabled(True)
        self.ui.closeButton.clicked.connect(self.closeEvent)
        self.ui.minimizeButton.clicked.connect(self.minimizeEvent)

        #list stuff
        #for i in range(40):
        #    self.ui.picList.addItem(str(i))

        #self.ui.splitter.setStretchFactor(1,1)
        self.ui.splitter.setSizes([200,200])#even split of splitter sides

        #the resize doesn't seems to working without this grid layout
        grid_layout = QGridLayout() 
        grid_layout.addWidget(self.ui) 
        self.setLayout(grid_layout)
        #grid_layout.setMargin(0)

        self.setAcceptDrops(True)
        designer_file.close()

        self.setMouseTracking(True)  # Set widget mouse tracking
        self.pressed = False

    def closeEvent(self):
        self.close()
    def minimizeEvent(self):
        self.showMinimized()

    def center(self):
          screen = QtGui.QGuiApplication.screenAt(QtGui.QCursor().pos())
          x = screen.geometry().center().x()-200
          y = screen.geometry().center().y()-200
          self.move(x - self.geometry().width()/2, y - self.geometry().height()/2)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.pressed =True

    def mouseMoveEvent(self, event):
        if self.pressed:
            delta = QPoint (event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.pressed = False
        print("release")

app = QApplication([])
window = MainWidget()
window.show()
app.exec_()
