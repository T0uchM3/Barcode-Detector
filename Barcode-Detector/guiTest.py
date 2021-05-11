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
from pyzbar import pyzbar
import pyzbar.pyzbar as zbar
import numpy as np

class MainWidget(QWidget):   
    imageList=[]
    #codeList=[]
    noneInside = True
    #mapSingnal = Signal(np.ndarray)
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
        
        #global codeList
        self.codeList = []
        #global imageList
        #self.imageList = QtGui.QDrag(self)

        #w = QtWidgets.QDialog()
        #w.setSizeGripEnabled(True)
        self.ui.closeButton.clicked.connect(self.closeEvent)
        self.ui.minimizeButton.clicked.connect(self.minimizeEvent)
        self.ui.picList.currentItemChanged.connect(self.selectionChanged)
        #self.ui.vidButton.clicked.connect(self.readVideo)
        self.ui.picButton.clicked.connect(self.testMeth)
        #self.mapSingnal.connect(self.displayVideo)
        #list stuff
        #for i in range(40):
        #    self.ui.picList.addItem(str(i))

        #self.ui.splitter.setStretchFactor(1,0)
        self.ui.splitter.setSizes([500,600])#splitting the splitter's sides??

        #the resize doesn't seems to working without this grid layout
        grid_layout = QGridLayout() 
        grid_layout.addWidget(self.ui) 
        self.setLayout(grid_layout)
        grid_layout.setMargin(0)

        self.setAcceptDrops(True)
        designer_file.close()

        self.setMouseTracking(True)  # Set widget mouse tracking
        self.pressed = False

        #file types (add for to support more)
        self.imageEx = ['.png' , '.jpg']
        self.videoEx = ['.mp4' , '.avi']
    def testMeth(self):
        print("len ", len(self.codeList))
        for obj in self.codeList:
            print( obj.code )
    def decodeDisVid(self, path):
        """decode and display video"""
        print("vid")
        cap = cv2.VideoCapture(path)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == False:
                break
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.ui.picDisplayer.setPixmap(pixmap)
            if cv2.waitKey(1) & 0xFF == ord('q'):#change waitKey val to slow down?
              break
            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
               barcodeData = barcode.data.decode("utf-8")
               barcodeType = barcode.type
               text = "{} ({})".format(barcodeData, barcodeType)
               #print(text)
               for obj in self.codeList:
                   if obj.code == barcodeData:
                       self.noneInside=False
                   else:
                       self.noneInside=True
               if self.noneInside:
                   self.codeList.append( codes(barcodeData,barcodeType) )
        for obj in self.codeList:
            print( obj.code )
        cap.release()
        cv2.destroyAllWindows()
    def decodeDisPic(self, path):
        """decode and display images"""
        print("pic")
        pixmap = QtGui.QPixmap(path)
        self.ui.picDisplayer.setPixmap(pixmap)
        print(self.ui.picList.currentItem().text())
        print(path)
        image = cv2.imread(path)
        barcode = zbar.decode(image)
        print('ZBar: {}'.format(barcode[0].data.decode("utf-8")))

    def selectionChanged(self):
        """ Detect item selection change inside the UI list """
        selected = self.ui.picList.currentItem().text()
        for path in self.imageList:
            #imageList contains the paths of all files in ui list
            #and the ui list selection only gives the name of what's selected
            #so we retrieve the path of what's currently selected in ui list
            if selected in path:
                extension = os.path.splitext(selected)[1]
                if (extension in self.imageEx):
                    self.decodeDisPic(path)
                if (extension in self.videoEx):
                    self.decodeDisVid(path)
    def dragEnterEvent(self, e):
        """
        This function will detect the drag enter event from the mouse on the main window
        Like it open the window to accept file dropping
        """
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()
    def dropEvent(self,e):
        """
        This function will enable the drop file(s) directly on to the
        main window. The file location will be stored in the self.filename
        """

        #self.imageList.setMimeData(e.mimeData())
        for url in e.mimeData().urls():
            fname = str(url.toLocalFile())
            self.ui.picList.addItem(str(os.path.basename(fname)))
            print("path",fname)
            self.imageList.append(fname)
        self.filename = fname
        print("ADR ", self.filename)
        
        #image = cv2.imread(self.filename)
        #barcode = zbar.decode(image)
        #print('ZBar: {}'.format(barcode[0].data.decode("utf-8")))


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
            self.setWindowOpacity(0.8)
            delta = QPoint (event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.setWindowOpacity(1)
        self.pressed = False
        print("release")
class codes:
    def __init__(self, code, type):
        self.code = code
        self.type = type

app = QApplication([])
window = MainWidget()
window.show()
app.exec_()
