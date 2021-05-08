import sys
import os
import cv2
from PySide2.QtWidgets import QApplication, QWidget
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import *
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
        #loader.registerCustomWidget(DragBar)
        #self.drag = DragBar(self)
        #self.layout  = QVBoxLayout()
        #self.layout.addWidget(self.ui.DragBar)
        #self.setLayout(self.layout)
        self.center()
        self.pressed = False
        
        #w = QtWidgets.QDialog()
        #w.setSizeGripEnabled(True)
        self.ui.closeButton.clicked.connect(self.closeEvent)
        self.ui.minimizeButton.clicked.connect(self.minimizeEvent)
        #drag.center(self)
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
        
        #self.gripSize = 16
        #self.grips = []
        #for i in range(4):
        #    grip = QSizeGrip(self)
        #    grip.resize(self.gripSize, self.gripSize)
        #    self.grips.append(grip)

        self.setAcceptDrops(True)
        designer_file.close()
        
        #self._initDrag()  # Set the default value of mouse tracking judgment trigger

        self.setMouseTracking(True)  # Set widget mouse tracking
        #self.DragBar.installEventFilter(self)  # Initialize event filter
        #self.DragBar.installEventFilter(self)


    def gribSelect(self):
        print("CLIIII")
    def closeEvent(self):
        self.close()
    def minimizeEvent(self):
        self.showMinimized()
    def dragEnterEvent(self, e):
        """
        This function will detect the drag enter event from the mouse on the main window
        """
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()
    def dropEvent(self,e):
        """
        This function will enable the drop file directly on to the
        main window. The file location will be stored in the self.filename
        """
        for url in e.mimeData().urls():
            fname = str(url.toLocalFile())
            self.ui.picList.addItem(str(os.path.basename(fname)))
        self.filename = fname
        print("ADR ", self.filename)
        
        image = cv2.imread(self.filename)
        barcode = zbar.decode(image)
        print('ZBar: {}'.format(barcode[0].data.decode("utf-8")))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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
    def resizeEvent(self, event):
        print("REEEEEEE")
        QMainWindow.resizeEvent(self, event)
        rect = self.rect()
        # top left grip doesn't need to be moved...
        # top right
        self.grips[1].move(rect.right() - self.gripSize, 0)
        # bottom right
        self.grips[2].move(
            rect.right() - self.gripSize, rect.bottom() - self.gripSize)
        # bottom left
        self.grips[3].move(0, rect.bottom() - self.gripSize)
class DragBar(QWidget):
    #p = MainWidget
    def __init__(self, parent):
        #QWidget.__init__(self, parent)
        print("test")
        print("parent",str(parent))
        super(DragBar, self).__init__()
        
        self.parent = parent
        #QWidget.__init__(self, parent)
        #self.center(parent)
        global p
        #p = parent
        #self.isPressed = False
        self.start = QPoint(0, 0)
        self.pressing = False
    #def center(self,parent):
    #    qr = parent.frameGeometry()
    #    cp = QDesktopWidget().availableGeometry().center()
    #    qr.moveCenter(cp)
    #    parent.move(qr.topLeft())
    #def mouseReleaseEvent(self, event):
    #    self.isPressed = False
    #def mousePressEvent(self, event):
    #    self.isPressed = True
    #    #self.oldPos = event.globalPos()
    #    self.startMovePos = event.globalPos()

    #def mouseMoveEvent(self, event):
        #delta = QPoint (event.globalPos() - p.oldPos)
        #p.move(p.x() + delta.x(), p.y() + delta.y())
        #p.oldPos = event.globalPos()


        #mainWin = self.parent().parent().parent()
        #mainWinPos = mainWin.pos()
        #delta = QPoint (event.globalPos() - self.oldPos)
        #mainWin.move(mainWinPos.x() + delta.x(), mainWinPos.y() + delta.y())


         #if self.isPressed:
         #   movePoint = event.globalPos() - self.startMovePos
         #   widgetPos = self.parentWidget().parentWidget().parentWidget().pos()
         #   self.startMovePos = event.globalPos()
         #   self.parentWidget().parentWidget().parentWidget().move(widgetPos.x() + movePoint.x(), widgetPos.y() + movePoint.y())




    def mousePressEvent(self, event):
        self.parent.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.parent.oldPos)
        self.parent.move(self.parent.x() + delta.x(), self.parent.y() + delta.y())
        self.parent.oldPos = event.globalPos()



    #def mousePressEvent(self, event):
    #    self.start = self.mapToGlobal(event.pos())
    #    self.pressing = True
    #    print("PRESSSSED")

    #def mouseMoveEvent(self, event):
    #    if self.pressing:
    #        self.end = self.mapToGlobal(event.pos())
    #        self.movement = self.end-self.start
    #        #mainWin = self.parent().parent()
    #        #print(str(mainWin))
    #        self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
    #                            self.mapToGlobal(self.movement).y(),
    #                            self.parent.width(),
    #                            self.parent.height())
    #        self.start = self.end

    #def mouseReleaseEvent(self, QMouseEvent):
    #    self.pressing = False
















    #def resizeEvent(self, QResizeEvent):
    ## Custom window sizing events
    ## Change the window size by three coordinate ranges
    #    self._right_rect = [QPoint(x, y) for x in range(self.width() - 5, self.width() + 5)
    #                        for y in range(self.widget.height() + 20, self.height() - 5)]
    #    self._bottom_rect = [QPoint(x, y) for x in range(1, self.width() - 5)
    #                         for y in range(self.height() - 5, self.height() + 1)]
    #    self._corner_rect = [QPoint(x, y) for x in range(self.width() - 5, self.width() + 1)
    #                     for y in range(self.height() - 5, self.height() + 1)]

    #def mousePressEvent(self, event):
    #    # Override mouse click events
    #    if (event.button() == Qt.LeftButton) and (event.pos() in self._corner_rect):
    #        # Left click the border area in the lower right corner
    #        self._corner_drag = True
    #        event.accept()
    #    elif (event.button() == Qt.LeftButton) and (event.pos() in self._right_rect):
    #        # Left click on the right border area
    #        self._right_drag = True
    #        event.accept()
    #    elif (event.button() == Qt.LeftButton) and (event.pos() in self._bottom_rect):
    #        # Click the lower border area with the left mouse button
    #        self._bottom_drag = True
    #        event.accept()
    #    elif (event.button() == Qt.LeftButton) and (event.y() < self.widget.height()):
    #        # Left click on the title bar area
    #        self._move_drag = True
    #        self.move_DragPosition = event.globalPos() - self.pos()
    #        event.accept()

    #def mouseMoveEvent(self, QMouseEvent):
    #    # Determine mouse position and switch mouse gesture
    #    if QMouseEvent.pos() in self._corner_rect:  # QMouseEvent.pos() get relative position
    #        self.setCursor(Qt.SizeFDiagCursor)
    #    elif QMouseEvent.pos() in self._bottom_rect:
    #        self.setCursor(Qt.SizeVerCursor)
    #    elif QMouseEvent.pos() in self._right_rect:
    #        self.setCursor(Qt.SizeHorCursor)

    #    # When the left mouse button click and meet the requirements of the click area, different window adjustments are realized
    #    # There is no definition of the left and top five directions, mainly because the implementation is not difficult, but the effect is very poor. When dragging and dropping, the window flickers, and then study whether there is a better implementation
    #    if Qt.LeftButton and self._right_drag:
    #        # Right adjust window width
    #        self.resize(QMouseEvent.pos().x(), self.height())
    #        QMouseEvent.accept()
    #    elif Qt.LeftButton and self._bottom_drag:
    #        # Lower adjustment window height
    #        self.resize(self.width(), QMouseEvent.pos().y())
    #        QMouseEvent.accept()
    #    elif Qt.LeftButton and self._corner_drag:
    #        #  Since I used the rounded corners, I didn't have to adjust the size of the window
    #        # Adjust the height and width at the same time in the lower right corner
    #        self.resize(QMouseEvent.pos().x(), QMouseEvent.pos().y())
    #        QMouseEvent.accept()
    #    elif Qt.LeftButton and self._move_drag:
    #        # Title bar drag and drop window position
    #        self.move(QMouseEvent.globalPos() - self.move_DragPosition)
    #        QMouseEvent.accept()

    #def mouseReleaseEvent(self, QMouseEvent):
    ## After the mouse is released, each trigger is reset
    #    self._move_drag = False
    #    self._corner_drag = False
    #    self._bottom_drag = False
    #    self._right_drag = False
    #def _initDrag(self):
    #    # Set the default value of mouse tracking judgment trigger
    #    self._move_drag = False
    #    self._corner_drag = False
    #    self._bottom_drag = False
    #    self._right_drag = False

app = QApplication([])
window = MainWidget()
window.show()
app.exec_()

