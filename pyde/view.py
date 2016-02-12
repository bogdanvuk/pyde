from PyQt4 import QtCore
from pyde.ddi import DependencyScope
from weakref import WeakValueDictionary

class View(DependencyScope):
#     child_added = QtCore.pyqtSignal(QtCore.QObject)
    
    def __init__(self, name, parent=None, **kwargs):
        super().__init__(name, parent)
        
        for k,v in kwargs:
            setattr(self, k, v)
        
    def set_focus(self):
        self.widget.parent().setCurrentWidget(self.widget)
        self.widget.setFocus()

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
