import sys
from PyQt4 import QtCore, QtGui
from pyde.editors.python import PythonEdit
from pyde.editors.interpret import InterpretEdit 
from pyde.desktop import DesktopFrame

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Buffer(QtGui.QTextEdit):
    def __init__(self, text="", parent=None):
        QtGui.QTextEdit.__init__(self, text, parent)
        self.setCurrentFont(QtGui.QFont("DejaVu Sans Mono-10"))

    def keyPressEvent(self, event):
        if event.modifiers() == QtCore.Qt.AltModifier:
            if event.key() == QtCore.Qt.Key_L:
                self.moveCursor(QtGui.QTextCursor.Right)
        else:
            return QtGui.QTextEdit.keyPressEvent(self, event)

class Main(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self,parent)

        self.initUI()

    def initUI(self):

        # x and y coordinates on the screen, width, height
#        self.setGeometry(100,100,1030,800)

        self.setWindowTitle("Writer")
        self.resize(800, 600)

        centralwidget = QtGui.QWidget(self)
        centralwidget.setObjectName(_fromUtf8("centralwidget"))
        gridLayout = QtGui.QGridLayout(centralwidget)
        gridLayout.setObjectName(_fromUtf8("gridLayout"))
#         verticalLayout = QtGui.QVBoxLayout()
#         verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        splitter = DesktopFrame(centralwidget, children=[PythonEdit(), InterpretEdit()], stretch=[1, 5])
        
#         splitter = QtGui.QSplitter(centralwidget)
#         splitter.setOrientation(QtCore.Qt.Vertical)
#         splitter.setObjectName(_fromUtf8("splitter"))
# 
# #         textEdit = Buffer(parent=centralwidget)
#         textEdit = PythonEdit(splitter)
# #         verticalLayout.addWidget(textEdit)
# 
# #         lineEdit = QtGui.QLineEdit(centralwidget)
#         lineEdit = InterpretEdit(splitter)
#         lineEdit.setObjectName(_fromUtf8("lineEdit"))
# #         verticalLayout.addWidget(lineEdit)

        gridLayout.addWidget(splitter, 0, 0, 1, 1)
        self.setCentralWidget(centralwidget)

        statusbar = QtGui.QStatusBar(self)
        statusbar.setObjectName(_fromUtf8("statusbar"))
        self.setStatusBar(statusbar)

        QtCore.QMetaObject.connectSlotsByName(self)
