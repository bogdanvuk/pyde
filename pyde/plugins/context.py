from PyQt4.QtCore import QObject, pyqtSlot
from pyde.ddi import Dependency
from PyQt4.QtGui import QWidget

class Context(object):
    def __init__(self, name, parent):
        self.parent = parent
        if parent is not None:
            self.parent.children[name] = self
        self.name = name
        self.children = {}
    
#     def find(self, path):
#         
    
    def __getitem__(self, item):
        return self.children[item]

    def __setitem__(self, item, val):
        self.children[item] = val

class ContextProvider(QObject):
    
    def __init__(self, win : Dependency('win')):
        super().__init__()
        self.root = Context('root', parent=None)
        for v in win.views:
            self.add_view(v)
            
        win.view_added.connect(self.add_view)

    @pyqtSlot(QWidget)
    def add_view(self, view):
        Context(view.name, self.root)
    
    def del_view(self, view):
        pass