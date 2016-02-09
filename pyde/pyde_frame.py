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
                
    def add_view(self, view, location):
        loc = location[0]
        location = location[1:]
        if location:
            self.widget.add_view(view, location)
        else:
            self.widget(loc).insertWidget(0, view)
            self.widget(loc).setCurrentWidget(view)

# class Desktop(object):
#     
#     def visit(self):
        