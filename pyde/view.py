from PyQt4 import QtCore
from pyde.ddi import DependencyScope
from weakref import WeakValueDictionary

class View(DependencyScope):
#     child_added = QtCore.pyqtSignal(QtCore.QObject)
    
    def __init__(self, widget, parent):
        super().__init__(widget.name, parent)
        self.widget = widget
#         self.children = {}
#         self.parent = parent
        self.parent.provide(widget.name, self)
#         self.parent[widget.name] = self

    def delete(self):
        self.parent.unprovide(self.widget.name)
        
#     def __del__(self):
#         self.parent.unprovide(self.widget.name)
#     @property
#     def name(self):
#         if hasattr(self.widget, 'name'):
#             return self.widget.name
#         else:
#             return ''
#     
#     def add(self, view):
#         self.children[view.name] = view
#         self.child_added.emit(view)
#     
    
    def active_view(self):
        if self.providers:
            child = next(self.providers.__iter__())
            return self.providers[child].active_view()
        else:
            return self
