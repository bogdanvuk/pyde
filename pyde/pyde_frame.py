from PyQt4 import QtGui, QtCore
from collections import namedtuple

# class DesktopDocument(object):
#     pass
orientation=QtCore.Qt.Vertical

ChildLayout = namedtuple('ChildLayout', 'stretch layout')
Layout = namedtuple('Layout', 'orientation children')

class PydeFrameVisitor:
    
    def visit(self, node, index=None):
        if hasattr(node, 'frames'):
            method = 'visit_node'
            getattr(self, method, self.generic_visit)(node, index)
        else:
            if hasattr(self, 'visit_leaf'):
                self.visit_leaf(node, index)
    
    def generic_visit(self, node, index=None):
        for i,c in enumerate(node.frames):
            self.visit(node.children()[i], i)

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
        self.frames = [None]*len(layout.children)
        self.assigned_views = [None]*len(layout.children)
        for i,c in enumerate(layout.children):
            if hasattr(c.layout, 'children'):
                child_frame = PydeFrame(c, self)
                self.addWidget(child_frame)
                self.frames[i] = child_frame
            else:
                self.addWidget(QtGui.QStackedWidget(self))
                
            self.setStretchFactor(i,c.stretch)
                
    def remove_layout(self):
        for i in range(self.count()):
            self.widget(i).hide()

    def add_view(self, view, location):
        loc = location[0]
        location = location[1:]
        if location:
            self.widget.add_view(view, location)
        elif self.assigned_views[loc] != view:
            self.assigned_views[loc] = view
            self.widget(loc).insertWidget(0, view.widget)
            self.widget(loc).setCurrentWidget(view.widget)
    
    
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
        config.append('from pyde.pyde_frame import ChildLayout, Layout')
        config.append('{}.set_layout({})'.format(var_name, self._dump_config_rec(self.layout)))
        return '\n'.join(config)

# class Desktop(object):
#     
#     def visit(self):
        