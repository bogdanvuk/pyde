from PyQt4.QtCore import QObject, pyqtSlot
from pyde.ddi import Dependency, ddic
from PyQt4.QtGui import QWidget
from PyQt4 import QtCore, QtGui

class KeyDispatcher(QObject):
#     def __init__(self, view, action, key, modifier=QtCore.Qt.NoModifier, args=(), kwargs={}):
    def __init__(self, win : Dependency('win'), context : Dependency('context')):
        super().__init__()
        self.win = win
        self.context = context
#         for v in win.views:
#             self.add_view(v)
#             
#         win.view_added.connect(self.add_view)
        
        ddic.provide_on_demand('cls/key_dispatcher_view_add', self.add_view)
        self.actions = []
        
    def add_view(self, view : Dependency('view/')):
        view.installEventFilter(self)
    
    def register_keyaction(self, action):
        self.actions.append(action)
    
    def eventFilter(self, source, event):
#         resp = False
        if (event.type() == QtCore.QEvent.KeyPress):
#             if event.key() == QtCore.Qt.Key_Tab:
#                 pass
            for a in self.actions:
                ret = a.event(source, event)
                if ret:
                    return True
        
#         if resp:
#             return True
#         else:
        return QtGui.QWidget.eventFilter(self, source, event)

    