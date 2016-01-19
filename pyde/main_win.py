from pyde.pyde_widget import PydeWidget
from PyQt4 import QtGui, QtCore
from pyde.ddi import Dependency, ddic
from PyQt4.QtGui import QApplication
from collections import OrderedDict
from pyde.view import View

class MainWindow(QtGui.QMainWindow):

    uri = []    
    view_added = QtCore.pyqtSignal(QtGui.QWidget) #['QWidget'])
    
    def __init__(self, layout: Dependency(feature='init_layout')):
        QtGui.QMainWindow.__init__(self)
#         self.view = View(self)
        self.name = 'view'
        self.view = View(self, ddic)
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
#         self.view = view_scope
        
        QtCore.QMetaObject.connectSlotsByName(self)
        self.centralLayout = gridLayout
        self.centralLayout.addWidget(layout, 0, 0, 1, 1)
        self.centralWidget = layout
        self.views = {}
    
    def place_view(self, view, location=[0]):
        view.last_location = location
        self.centralWidget.add_view(view, location)
       
#     def add_view(self, view, location=[0]):
#         self.context.update_context(self, ['/', view.name], view)
#         self.centralWidget.add_view(view, location)
#         self.view_added.emit(view)
#         self.view_scope.provide(view.name, view)
#         self.views.append(view)

#     def add_view(self, view):
#         self.views[view.name] = view

    def active_view(self):
        return QApplication.focusWidget().view.active_view()


#     def keyPressEvent(self, event):
# #         print("key_press")
#         if not app.key_press_fire_action(event, self):
#             QtGui.QMainWindow.keyPressEvent(self, event)
           
