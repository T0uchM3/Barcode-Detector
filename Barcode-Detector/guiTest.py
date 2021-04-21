#import sys

## 1. Import `QApplication` and all the required widgets
#from PyQt5.QtWidgets import QApplication
#from PyQt5.QtWidgets import QLabel
#from PyQt5.QtWidgets import QWidget
#app = QApplication(sys.argv)
## 3. Create an instance of your application's GUI
#window = QWidget()
#window.setWindowTitle('PyQt5 App')
#window.setGeometry(100, 100, 280, 80)
#window.move(60, 15)
#helloMsg = QLabel('<h1>Hello World!</h1>', parent=window)
#helloMsg.move(60, 15)

## 4. Show your application's GUI
#window.show()

## 5. Run your application's event loop (or main loop)
#sys.exit(app.exec_())


# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

loader = QUiLoader()
app = QtWidgets.QApplication(sys.argv)
window = loader.load("form.ui", None)
window.show()
app.exec_()




#class test(QWidget):
#    def __init__(self):
#        super(test, self).__init__()
#        self.load_ui()

#    def load_ui(self):
#        loader = QUiLoader()
#        path = os.path.join(os.path.dirname(__file__), "form.ui")
#        ui_file = QFile(path)
#        ui_file.open(QFile.ReadOnly)
#        loader.load(ui_file, self)
#        ui_file.close()

#if __name__ == "__main__":
#    app = QApplication([])
#    widget = test()
#    widget.show()
#    sys.exit(app.exec_())
