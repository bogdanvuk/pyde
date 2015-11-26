from PyQt4.QtGui import QWidget
from pyde.application import app
from PyQt4.QtCore import QObject

class PydeWidget(object):
    
    def keyPressEvent(self, event):
        if not app.key_press_fire_action(event, self):
            super().keyPressEvent(event)
    
    