from PyQt5 import QtWidgets, QtCore
from ddi.ddi import Amendment
from PyQt5.QtWidgets import QApplication
from pyde.pyde_frame import PydeFrameVisitor

class MainWindow(QtWidgets.QMainWindow):

    uri = []    
    view_added = QtCore.pyqtSignal(QtWidgets.QWidget) #['QWidget'])
    
    def __init__(self, view: Amendment('win')): #, layout: Dependency('win_layout')):
        self.view = view
        QtWidgets.QMainWindow.__init__(self)

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
        
#         v = LayoutVisitor()
#         v.visit(self.centralWidget)
        config.append(self.view.layout.dump_config('win.layout'))
        
        return '\n'.join(config)
