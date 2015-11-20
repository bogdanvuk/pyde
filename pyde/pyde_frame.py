from PyQt4 import QtGui, QtCore

# class DesktopDocument(object):
#     pass

class PydeFrame(QtGui.QSplitter):
    
    def __init__(self, orientation=QtCore.Qt.Vertical, stretch=None, parent=None):
        QtGui.QSplitter.__init__(self, orientation, parent)
        
        if stretch:
            for i,s in enumerate(stretch):
                self.addWidget(QtGui.QStackedWidget())
                self.setStretchFactor(i,s)

# class Desktop(object):
#     
#     def visit(self):
        