import sys
import os
import cv2
import datetime
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
    codeList=[]
    noneInside = True
    vidIsOpen = False
    capture = False
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
        

        self.ui.closeButton.clicked.connect(self.closeEvent)
        self.ui.minimizeButton.clicked.connect(self.minimizeEvent)
        self.ui.picList.currentItemChanged.connect(self.selectionChanged)
        self.ui.vidButton.clicked.connect(self.vidThreadControl)
        self.ui.stopButton.clicked.connect(self.vidThreadControl)
        self.ui.picButton.clicked.connect(self.imgThreadControl)
        self.ui.capButton.clicked.connect(self.imgThreadControl)
        self.ui.clearButton.clicked.connect(self.clearDisplay)
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
    def addCaptured(self, img_name):
        """this get executed from vidThread class""" 
        self.ui.picList.addItem(str(os.path.basename(img_name)))
        print("path",img_name)
        self.imageList.append(img_name)
        self.ui.picDisplayer.clear()
    def clearDisplay(self):
        """clear the label, list, and the other list"""
        self.ui.picList.clear()
        self.ui.picDisplayer.clear()
        self.imageList.clear()
        print("clear")
    def imgThreadControl(self):
        print("image")
        if self.capture ==True:
            print("FFFFF")
            self.thread.cap=True
            self.capture=False
            self.thread.stop()
            self.ui.stackedWidget.setCurrentIndex(0)
            return
        self.ui.stackedWidget.setCurrentIndex(2)
        self.capture =True
        self.thread = vidThread("", self.ui, True, False, self)
        # start the thread
        self.thread.start()
    def vidThreadControl(self, image):
        if self.vidIsOpen==True:
            self.vidIsOpen=False
            self.thread.stop()
            self.ui.stackedWidget.setCurrentIndex(0)
            return
        self.vidIsOpen= True
        self.ui.stackedWidget.setCurrentIndex(1)
        # create the video capture thread
        self.thread = vidThread("", self.ui, False, False, self)
        # start the thread
        self.thread.start()

    def localVidThreadControl(self, path):
        """decode and display video inside main window"""
        self.threadLocal = vidThread(path, self.ui, False, False, self)
        self.threadLocal.pixmap_signal.connect(self.startCamVid)
        self.threadLocal.start()

    def decodeDisPic(self, path):
        """decode and display images"""
        print("pic")
        #pixmap = QtGui.QPixmap(path)
        print(self.ui.picList.currentItem().text())
        print(path)
        image = cv2.imread(path)
        

        barcode = zbar.decode(image)
        for obj in barcode:
            #print('ZBar: {}'.format(barcode[0].data.decode("utf-8")))
            print(obj.data)
            (x, y, w, h) = obj.rect
            cv2.rectangle(image, (x, y), (x + w, y + h),(0, 255, 0), 3)
        image2 = QImage(image, image.shape[1], image.shape[0], image.strides[0], QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(image2)
        self.ui.picDisplayer.setPixmap(pixmap)
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
                    self.localVidThreadControl(path)
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
        """make sure the window in the middle of the screen?"""
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
class vidThread(QThread):
    pixmap_signal = Signal(np.ndarray)
    codeList=[]
    noneInside = True
    
    def __init__(self, path, ui, image, cap, parent):
        super().__init__()
        self.parent = parent
        self.path = path
        self.ui = ui
        self.img=image
        self.cap=cap
        self.run_flag = True
    def run(self):
        if len(self.path)>0:
            cap = cv2.VideoCapture(self.path)
        else:
            cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        # capture from cam
        while self.run_flag:
            ret, cv_img = cap.read()
            if ret == False:#preventing frame crash?
                break
            
            #if self.img==False:
            barcodes = pyzbar.decode(cv_img)
            for barcode in barcodes:#one frame can contains many barcodes
                self.demoCode = barcode
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type

                (x, y, w, h) = barcode.rect
                cv2.rectangle(cv_img, (x, y), (x + w, y + h),(0, 255, 0), 3)
                for obj in self.codeList:#we considering codeList a list of object "Code"
                    if obj.code == barcodeData:#so we compare class "Code" .code to the current barcode
                        self.noneInside=False
                    else:
                        self.noneInside=True
                if self.noneInside:
                    self.codeList.append( codes(barcodeData,barcodeType) )
                    print( barcodeData )
            if cv2.waitKey(1) & 0xFF == ord('q'):#change waitKey val to slow down?
                break
            #else:
            if self.cap == True:
                print(datetime.datetime.now())
                dateString = datetime.datetime.now().strftime("%I%M%S%d%Y")
                img_name = "opencv_{}.png".format(dateString)
                print(type(dateString))
                cv2.imwrite(img_name, cv_img)
                self.parent.addCaptured(img_name)
                self.cap = False

            image2 = QImage(cv_img, cv_img.shape[1], cv_img.shape[0], cv_img.strides[0], QImage.Format_BGR888)
            pixmap = QPixmap.fromImage(image2)
            self.ui.picDisplayer.setPixmap(pixmap)

        cap.release()
        self.ui.picDisplayer.clear()
    def stop(self):
        self.run_flag = False
        

class codes:
    def __init__(self, code, type):
        self.code = code
        self.type = type

app = QApplication([])
window = MainWidget()
window.show()
app.exec_()
