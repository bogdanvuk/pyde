from pyde.pyde_widget import PydeWidget
from PyQt4 import QtGui, QtCore
from pyde.ddi import Dependency, ddic, Amendment
from PyQt4.QtGui import QApplication
from collections import OrderedDict
from pyde.view import View
from pyde.pyde_frame import PydeFrameVisitor

class MainWindow(QtGui.QMainWindow):

    uri = []    
    view_added = QtCore.pyqtSignal(QtGui.QWidget) #['QWidget'])
    
    def __init__(self, view: Amendment('win')): #, layout: Dependency('win_layout')):
        QtGui.QMainWindow.__init__(self)
#         self.view = View(self)
#         self.name = 'winview'
        view.widget = self
#         self.view = View(self, ddic)
        self.setWindowTitle("Writer")
#         self.resize(800, 600)

#         centralwidget = QtGui.QWidget(self)
#         centralwidget.setObjectName("centralwidget")
#         
#         gridLayout = QtGui.QGridLayout(centralwidget)
#         gridLayout.setObjectName("gridLayout")
#         self.centralLayout = gridLayout
#         
#         self.setCentralWidget(centralwidget)
#         self.centralLayout.addWidget(layout, 0, 0, 1, 1)
#         self.centralWidget = layout
        
#         self.view = view_scope
        
        QtCore.QMetaObject.connectSlotsByName(self)
        self.views = {}
    
#     def place(self, view, location=[0]):
#         self
#         view.last_location = location
#         self.centralWidget.add_view(view, location)
       
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


    def dump_config(self, var_name):
        config = []
        
        config.append('{}.resize({}, {})'.format(var_name, self.width(), self.height()))
        if self.isMaximized():
            config.append('{}.showMaximized()'.format(var_name))
        
        class LayoutVisitor(PydeFrameVisitor):
            def __init__(self, config=[]):
                self.loc = []
                self.config = config
                
            def visit_node(self, node, index=None):
                if index:
                    self.loc.append(index)

                self.generic_visit(node, index)
                
                if self.loc:
                    self.loc.pop()
                
            def visit_leaf(self, node, index=None):
                self.loc.append(index)
                view = node.parent().assigned_views[index]
                self.config.append("ddic['win'].widget.place(ddic['view/{}'], {})".format(view.name, self.loc))
                self.config.append(view.dump_config("ddic['view/{}']".format(view.name)))
                self.loc.pop()
        
        v = LayoutVisitor()
        v.visit(self.centralWidget)
        config.extend(v.config)
        
        return '\n'.join(config)

#     def keyPressEvent(self, event):
# #         print("key_press")
#         if not app.key_press_fire_action(event, self):
#             QtGui.QMainWindow.keyPressEvent(self, event)
           
