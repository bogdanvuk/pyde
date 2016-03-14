from pyde.ddi import Dependency, Amendment
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QLineEdit
from pyde.plugins.editor_mode import ViewMode

class StatusbarMode(ViewMode):
    name = '__statusbar__'
    
    def __init__(self, view : Amendment('view/', lambda v: v.name == '__statusbar__')):
        super().__init__(view)

class Statusbar(QLineEdit):

    def __init__(self, view: Amendment('view/', lambda v: hasattr(v, 'mode') and (v.mode.name == '__statusbar__') and (v.widget is None))):
        super().__init__()
        self.view = view
        self.view.widget = self
        
    def cycle_frame(self, old):
        return False



# class StatusBar(QtGui.QStatusBar):
#     def __init__(self, app: Dependency('app'), win : Dependency('win')):
#         super().__init__(win.widget)
# 
#         self.setObjectName("statusbar")
#         win.widget.setStatusBar(self)
#         app.focusChanged.connect(self.view_changed_focus)
# 
#     def view_changed_focus(self, old, now):
#         if now:
#             name = getattr(now.view, 'name', '')
#             self.showMessage(name)
        