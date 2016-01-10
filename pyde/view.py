from PyQt4 import QtCore

class View(QtCore.QObject):
    child_added = QtCore.pyqtSignal(QtCore.QObject)
    
    def __init__(self, widget, parent=None):
        super().__init__()
        self.widget = widget
        self.children = {}
        self.parent = parent
        
        if parent is not None:
            self.parent.add(self)
    
    @property
    def name(self):
        if hasattr(self.widget, 'name'):
            return self.widget.name
        else:
            return ''
    
    def add(self, view):
        self.children[view.name] = view
        self.child_added.emit(view)
    
    @property
    def uri(self):
        if self.parent:
            uri = self.parent.uri + [self.name]
        else:
            uri = []
            
        return uri
    
    def active_view(self):
        if self.children:
            child = next(reversed(self.children))
            return child.active_view()
        else:
            return self
