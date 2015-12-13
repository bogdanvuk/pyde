from PyQt4.QtCore import QObject
from PyQt4 import QtCore, QtGui

class KeyAction(QObject):
    def __init__(self, view, action, key, modifier=QtCore.Qt.NoModifier, args=(), kwargs={}):
        super().__init__()
        self.view = view
        self.action = action
        self.key = key
        self.modifier = modifier
        self.action_args = args
        self.action_kwargs = kwargs
        
        self.view.installEventFilter(self)
        
    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.KeyPress and
            source is self.view and 
            event.key() == self.key and
            int(event.modifiers()) == self.modifier):
            
            self.action(*self.action_args, **self.action_kwargs)
            return True
            
        return QtGui.QWidget.eventFilter(self, source, event)
