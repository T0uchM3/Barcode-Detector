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
    imageList = []
    codeList = []
    noneInside = True
    vidIsOpen = False
    capture = False
    path = ''
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
        self.ui.vidButton.clicked.connect(self.liveVideo)
        self.ui.stopButton.clicked.connect(self.liveVideo)
        self.ui.picButton.clicked.connect(self.captureImage)
        self.ui.capButton.clicked.connect(self.captureImage)
        self.ui.clearButton.clicked.connect(self.clearDisplay)
        self.ui.cancelButton.clicked.connect(self.cancelCap)

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

        self.out = ''

        #file types (add for to support more)
        self.imageEx = ['.png' , '.jpg']
        self.videoEx = ['.mp4' , '.avi']
    def addCaptured(self, img_name):
        """this get executed from vidThread class""" 
        #add the picture that got captured from cam to the ui list
        self.ui.picList.addItem(str(os.path.basename(img_name)))
        print("path",img_name)
        #add the picture that got captured from cam to the imageList (list of
        #paths?)
        self.imageList.append(img_name)
        self.ui.picDisplayer.clear()
    def clearDisplay(self):
        """clear the ui list, label and the path list"""
        self.ui.picList.clear()
        self.ui.picDisplayer.clear()
        self.imageList.clear()
        self.out = ''
        self.ui.logText.setPlainText(self.out)
        print("clear")
    def captureImage(self):
        """open cam to capture a picture"""
        print("image")
        if self.capture == True:
            print("FFFFF")
            #cam is open by now, thread already initialized
            #so just need to access the cap var and mark it "True"
            self.thread.cap = True
            self.capture = False
            return
        #initial click on the "open cam and take a picture" button
        #switch the stack widget to the "capture" button's page
        self.ui.stackedWidget.setCurrentIndex(2)
        self.capture = True
        #opening cam via thread
        self.thread = vidThread("", self.ui, self)
        self.thread.bool_signal.connect(self.captureDisabler)
        # start the thread
        self.thread.start()
    def captureDisabler(self, stat):
        #to avoid capturing a bad image, this will ensure the cap button 
        #will only be active when there's a readable code in the scene 
        self.ui.capButton.setEnabled(stat)
    def cancelCap(self):
        self.capture = False
        self.thread.stop()
        self.ui.stackedWidget.setCurrentIndex(0)
    def liveVideo(self, image):
        """open cam to detect and decode bar/qr-codes from feed"""
        if self.vidIsOpen == True:
            self.vidIsOpen = False
            self.thread.stop()
            self.ui.stackedWidget.setCurrentIndex(0)
            
            return
        self.vidIsOpen = True
        self.ui.stackedWidget.setCurrentIndex(1)
        # create a video capture thread, no path
        self.thread = vidThread("", self.ui, self)
        self.thread.log_signal.connect(self.logPrint)
        self.thread.abort_signal.connect(self.abort)
        # start the thread
        self.thread.start()
    def abort(self):
        if len(self.path)>0:
            self.decodeDisPic(self.path)
    def localVidThreadControl(self, path):
        """decode and display video inside main window"""
        self.threadLocal = vidThread(path, self.ui, self)
        self.threadLocal.log_signal.connect(self.logPrint)
        self.threadLocal.start()
    def logPrint(self, text):
        self.ui.logText.setPlainText(text)
        self.ui.logText.moveCursor(QtGui.QTextCursor.End)
    def decodeDisPic(self, path):
        """decode and display images"""
        print("pic")
        #pixmap = QtGui.QPixmap(path)
        print(self.ui.picList.currentItem().text())
        print(path)
        image = cv2.imread(path)
        

        barcode = zbar.decode(image)
        index = 0
        for obj in barcode:
            self.out += "Index: " + str(index) + "\n"
            #utf-8 to remove the byte 'b 
            self.out += "Barcode format: " + str(obj.data.decode("utf-8")) + "\n"
            self.out += "Barcode value: " + str(obj.type) + "\n"
            self.out += "------------------------------\n"
            index += 1
            self.ui.logText.setPlainText(self.out)
            self.ui.logText.moveCursor(QtGui.QTextCursor.End)
            print(obj.data)
            (x, y, w, h) = obj.rect
            cv2.rectangle(image, (x, y), (x + w, y + h),(0, 255, 0), 3)
        image2 = QImage(image, image.shape[1], image.shape[0], image.strides[0], QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(image2)
        self.ui.picDisplayer.setPixmap(pixmap)
    def selectionChanged(self):
        """ Detect item selection change inside the UI list """
        selected = self.ui.picList.currentItem().text()
        for self.path in self.imageList:
            #imageList contains the paths of all files in ui list
            #and the ui list selection only gives the name of what's selected
            #so we retrieve the path of what's currently selected in ui list
            if selected in self.path:
                #"selected" is the text in the ui list (xxx.yyy)
                #[0] returns the "xxx" part (name)
                #[1] returns the "yyy" part (type)
                extension = os.path.splitext(selected)[1]

                #depends on the file's type (image or video) we run their respective methods
                if (extension in self.imageEx):
                    self.decodeDisPic(self.path)
                if (extension in self.videoEx):
                    self.localVidThreadControl(self.path)
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
        
    def closeEvent(self):
        self.close()
    def minimizeEvent(self):
        self.showMinimized()

    def center(self):
        """make sure the window in the middle of the screen?"""
        screen = QtGui.QGuiApplication.screenAt(QtGui.QCursor().pos())
        x = screen.geometry().center().x() - 200
        y = screen.geometry().center().y()
        self.move(x - self.geometry().width() / 2, y - self.geometry().height() / 2)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.pressed = True

    def mouseMoveEvent(self, event):
        if self.pressed:
            self.setWindowOpacity(0.87)
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.setWindowOpacity(1)
        self.pressed = False
        print("release")
class vidThread(QThread):
    """__init__(path (if it's local video), ui, parent)"""
    log_signal = Signal(str)
    bool_signal = Signal(bool)
    codeList = []
    noneInside = True
    abort_signal = Signal(bool)
    def __init__(self, path, ui, parent):
        super().__init__()
        self.parent = parent
        self.path = path#path of the local video
        self.ui = ui#used to access the display label and the like
        self.cap = False#True when we take a picture
        self.run_flag = True
        self.out = ''
    def run(self):
        #if there's a path we open the pointed video
        if len(self.path) > 0:
            capture = cv2.VideoCapture(self.path)
        else:
            capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        #works for cam source or local
        while self.run_flag:
            ret, cv_img = capture.read()
            #preventing crash
            if ret == False:
                break
            self.bool_signal.emit(False)
            #if self.img==False:
            barcodes = pyzbar.decode(cv_img)
            index = 0
            for barcode in barcodes:#one frame can contains many barcodes
                self.demoCode = barcode
                barcodeData = barcode.data.decode()
                barcodeType = barcode.type
                self.bool_signal.emit(True)
                #(x, y, w, h) = barcode.rect
                #cv2.rectangle(cv_img, (x, y), (x + w, y + h),(0, 255, 0), 3)
                
                for obj in self.codeList:#we considering codeList a list of object "Code"
                    if obj.code == barcodeData:#so we compare class "Code" .code to the current barcode
                        self.noneInside = False
                    else:
                        self.noneInside = True
                if self.noneInside:
                    self.codeList.append(codes(barcodeData,barcodeType))
                    print("baaar  ",barcodeData)
                    self.out += "Index: " + str(index) + "\n"
                    self.out += "Barcode format: " + str(barcode.data.decode("utf-8")) + "\n"
                    self.out += "Barcode value: " + str(barcode.type) + "\n"
                    self.out += "------------------------------\n"
                    index += 1
                    self.log_signal.emit(self.out)
                    
            if cv2.waitKey(1) & 0xFF == ord('q'):#change waitKey val to slow down?
                break
            #if "capture" button clicked
            if self.cap == True:
                #take a picture, give it a unique name and add it to the ui list
                print(datetime.datetime.now())
                dateString = datetime.datetime.now().strftime("%I%M%S%d%Y")
                img_name = "opencv_{}.jpg".format(dateString)
                print(type(dateString))
                cv2.imwrite(img_name, cv_img)
                self.parent.addCaptured(img_name)
                self.cap = False
                self.bool_signal.emit(False)
                #stop video stream
                break

            #since qpixmap only accepts qimages we need to convert our image to that
            finalImage = QImage(cv_img, cv_img.shape[1], cv_img.shape[0], cv_img.strides[0], QImage.Format_BGR888)
            pixmap = QPixmap.fromImage(finalImage)
            #if self.run_flag == False:
            #    break
            self.ui.picDisplayer.setPixmap(pixmap)

        capture.release()
        #clear the display zone after finishing
        self.ui.picDisplayer.clear()
        self.abort_signal.emit(False)
    def stop(self):
        """while loop in "run" will stop"""
        self.run_flag = False
        

#class to help storing the bar/qr-code and their type 
class codes:
    def __init__(self, code, type):
        self.code = code
        self.type = type

app = QApplication([])
window = MainWidget()
window.show()
app.exec_()