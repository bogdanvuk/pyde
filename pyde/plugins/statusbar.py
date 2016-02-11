from pyde.ddi import Dependency
from PyQt4 import QtGui, QtCore

class StatusBar(QtGui.QStatusBar):
    def __init__(self, app: Dependency('app'), win : Dependency('win')):
        super().__init__(win)

        self.setObjectName("statusbar")
        win.setStatusBar(self)
        app.focusChanged.connect(self.view_changed_focus)

    def view_changed_focus(self, old, now):
        name = getattr(now, 'name', '')
        self.showMessage(name)
        