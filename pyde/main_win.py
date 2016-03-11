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

        view.widget = self
        self.setWindowTitle("Writer")
        
        QtCore.QMetaObject.connectSlotsByName(self)
        self.views = {}

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
