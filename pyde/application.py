import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, pyqtSlot
import PyQt4
from PyQt4.QtGui import QWidget

try:
    _fromUtf8 = QtCore.QString.fromUtf8  # @UndefinedVariable
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

class App(QtGui.QApplication):

    def __init__(self):
        super().__init__([])
        self.focusChanged.connect(self.focus_changed)
    
    def init_ui(self):
        self.centralLayout = self.win.centralLayout
        self.key_bindings = {}
        self.focus_history = []
    
    def add_layout(self, widget):
        self.centralLayout.addWidget(widget, 0, 0, 1, 1)
        self.centralWidget = widget

    def key_press_fire_action(self, event, widget):
        key_pair = (event.key(), int(event.modifiers()))
        if key_pair in self.key_bindings:
            contexts = self.key_bindings[key_pair]
            base_names = [widget.__class__.__name__] + [b.__name__ for b in widget.__class__.__bases__]
            for c in contexts:
                if c in base_names:
                    contexts[c]()
                    return True

            event.ignore()
            return True
                
        return False
    
#     @pyqtSlot(QWidget, QWidget)
    def focus_changed(self, old, new):
        self.focus_history.append(new)
        
    def active_widget(self):
        return self.focusWidget()
#         return self.focus_history[-1]
    
    def bind_key(self, action, key, modifier=QtCore.Qt.NoModifier, context="App"):
        key_pair = (key, modifier)
        if key_pair not in self.key_bindings:
            self.key_bindings[key_pair] = {}
        
        self.key_bindings[key_pair][context] = action

app = App()
