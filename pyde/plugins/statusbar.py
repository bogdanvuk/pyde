from pyde.ddi import Dependency
from PyQt4 import QtGui, QtCore

class StatusBar(QtGui.QStatusBar):
    def __init__(self, app: Dependency('app'), win : Dependency('win')):
        super().__init__(win.widget)

        self.setObjectName("statusbar")
        win.widget.setStatusBar(self)
        app.focusChanged.connect(self.view_changed_focus)

    def view_changed_focus(self, old, now):
        if now:
            name = getattr(now.view, 'name', '')
            self.showMessage(name)
        