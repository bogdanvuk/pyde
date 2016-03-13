from PyQt4 import QtCore
from pyde.ddi import DependencyScope, ddic
from weakref import WeakValueDictionary
from PyQt4.QtCore import QObject

class View(QObject): #(DependencyScope):
#     child_added = QtCore.pyqtSignal(QtCore.QObject)
    
    def __init__(self, name, parent=None, widget=None, **kwargs):
#         super().__init__(name, parent)
        super().__init__()
        self.child = []
        self.name = name
        self.config = kwargs
        if parent:
            parent.child.append(self)
        self.parent = parent
        self.clones = []
        self.active_widget = None

        if widget:
            self._widget = [widget]
        else:
            self._widget = []
            
        for k,v in kwargs.items():
            setattr(self, k, v)
            
        ddic['app'].focusChanged.connect(self.focus_changed)

    def child_by_name(self, name):
        for c in self.child:
            if c.name == name:
                return c
            
        return None

    def clone_widget(self):
        w = self.widget.clone()
        self.widget = w
        ddic.provide('widget/', w)
        
        return w

    def remove_widget(self, w):
        del self._widget[self._widget.index(w)]
        ddic.unprovide('widget/{}'.format(id(w)))
        if not self._widget:
            self.delete()

#     def clone(self, **kwargs):
#         kwargs.update(self.config)
#         clone = self.__class__(name=self.name, parent=self.parent, **kwargs)
#         self.clones.append(clone)
#         clone.widget = self.widget.clone()
#         ddic.provide('view/', clone)
#         return clone
            
    @property
    def uri(self):
        if self.parent:
            uri = self.parent.uri + [self.name]
        else:
            uri = [self.name]
            
        return uri
    
    @property
    def widget(self):
        return self.active_widget

    @widget.setter
    def widget(self, value):
        self._widget.append(value)

        if self.active_widget is None:
            self.active_widget = value
            
        value.view = self
    
    def focus_changed(self, old, new):
        if new in self._widget:
            self.active_widget = new
    
    def set_focus(self, view=None):
        if view is None:
            self.parent.set_focus(self)
        else:
            self.layout.place(view, view.widget.loc)
            view.widget.setFocus()

    def add(self, view):
        self.child.append(view)
        view.parent = self
        
    def remove(self, view):
        del self.child[self.child.index(view)]

    def show(self, location):
        self.parent.place(self, location)

    def delete(self):
        self.parent.remove(self)
        for w in self._widget:
            w.hide()
            w.parent = None
            w.view = None
#         del self.parent.child[self.name]
        
    def dump_config(self, var_name):
        config = []
        for child in self.child:
            config_dump = []
            for name, c in child.config.items():
                config_dump.append("{}='{}'".format(name, str(c)))

            view_config = ','.join(["'" + child.name + "'", var_name] + config_dump)
            config.append("ddic.provide('view/{0}', ddic['cls/view']({1}))".format(child.name, view_config))
        
        if hasattr(self.widget, 'dump_config'):
            config.append(self.widget.dump_config('.'.join([var_name, 'widget'])))
        
        return '\n'.join(config)
    
    def active_view(self):
        for c in self.child:
            view = c.active_view()
            if view is not None:
                return view
        else:
            if self.widget.hasFocus():
                return self
            else:
                return None
#         if self.child:
#             child = next(self.child.__iter__())
#             return self.child[child].active_view()
#         else:
#             return self

class WindowView(View):
    def add(self, view, location=None):
        super().add(view)
        if location:
            view.show(location)

    def show(self, view, location):
        self.child[view.name] = view

