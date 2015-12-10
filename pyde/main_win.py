from pyde.pyde_widget import PydeWidget
from PyQt4 import QtGui, QtCore
from pyde.ddi import Dependency, ddic

class MainWindow(QtGui.QMainWindow):
    
    view_added = QtCore.pyqtSignal(QtGui.QWidget) #['QWidget'])
    
    def __init__(self, layout: Dependency(feature='init_layout'), view_scope: Dependency('view')):
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
        self.view_scope = view_scope
        
        QtCore.QMetaObject.connectSlotsByName(self)
        self.centralLayout = gridLayout
        self.centralLayout.addWidget(layout, 0, 0, 1, 1)
        self.centralWidget = layout
        self.views = []
       
    def add_view(self, view, location=[0]):
        self.centralWidget.add_view(view, location)
        self.view_added.emit(view)
        self.view_scope.provide(view.name, view)
        self.views.append(view)


#     def keyPressEvent(self, event):
# #         print("key_press")
#         if not app.key_press_fire_action(event, self):
#             QtGui.QMainWindow.keyPressEvent(self, event)
           
