from pyde.pyde_widget import PydeWidget
from PyQt4 import QtGui, QtCore

class MainWindow(PydeWidget, QtGui.QMainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        self.setWindowTitle("Writer")
        self.resize(800, 600)

        centralwidget = QtGui.QWidget(self)
        centralwidget.setObjectName("centralwidget")
        gridLayout = QtGui.QGridLayout(centralwidget)
        gridLayout.setObjectName("gridLayout")
        
        self.setCentralWidget(centralwidget)
        
        statusbar = QtGui.QStatusBar(self)
        statusbar.setObjectName("statusbar")
        self.setStatusBar(statusbar)
        
        QtCore.QMetaObject.connectSlotsByName(self)
        self.centralLayout = gridLayout

#     def keyPressEvent(self, event):
# #         print("key_press")
#         if not app.key_press_fire_action(event, self):
#             QtGui.QMainWindow.keyPressEvent(self, event)
           
