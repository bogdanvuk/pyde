from PyQt4 import QtGui, QtCore
from collections import namedtuple

# class DesktopDocument(object):
#     pass
orientation=QtCore.Qt.Vertical

ChildLayout = namedtuple('ChildLayout', 'stretch layout')
Layout = namedtuple('Layout', 'orientation children')

class PydeFrame(QtGui.QSplitter):
    
    def __init__(self, layout=None, parent=None):
        if layout is None:
            orientation = QtCore.Qt.Vertical
        else:
            orientation = layout.orientation  
        
        QtGui.QSplitter.__init__(self, orientation, parent)

        if layout is not None:
            self.set_layout(layout)

    def set_layout(self, layout):
        self.remove_layout()
        self.setOrientation(layout.orientation)
        self.layout = layout

        for i,c in enumerate(layout.children):
            if hasattr(c.layout, 'children'):
                self.addWidget(PydeFrame(c, self))
            else:
                self.addWidget(QtGui.QStackedWidget())
                
            self.setStretchFactor(i,c.stretch)
                
    def remove_layout(self):
        for i in range(self.count()):
            self.widget(i).hide()

    def add_view(self, view, location):
        loc = location[0]
        location = location[1:]
        if location:
            self.widget.add_view(view, location)
        else:
            self.widget(loc).insertWidget(0, view)
            self.widget(loc).setCurrentWidget(view)
    
    
    def _dump_config_rec(self, layout):
        
        child_config = []
        for c in layout.children:
            if hasattr(c.layout, 'children'):
                ret = self._dump_config_rec(c.layout)
            else:
                ret = 'None'
                
            child_config.append('ChildLayout({},{})'.format(c.stretch, ret))

        orientation = ['Qt.Vertical', 'Qt.Vertical'][layout.orientation - 1]
        return 'Layout({}, [{}])'.format(orientation, ','.join(child_config))
    
    def dump_config(self, var_name):
        config = []
        config.append('from PyQt4.QtCore import Qt')
        config.append('{}.set_layout({})'.format(var_name, self._dump_config_rec(self.layout)))
        return '\n'.join(config)

# class Desktop(object):
#     
#     def visit(self):
        