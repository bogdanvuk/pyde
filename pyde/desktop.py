from PyQt4 import QtGui, QtCore

# class DesktopDocument(object):
#     pass

class DesktopFrame(QtGui.QSplitter):
    
    def __init__(self, parent=None, orientation=QtCore.Qt.Vertical, children=[], stretch=None):
        QtGui.QSplitter.__init__(self, orientation, parent)
        
        for i,c in enumerate(children):
            self.addWidget(c)
            self.setStretchFactor(i,stretch[i])

# class Desktop(object):
#     
#     def visit(self):
        