from PyQt4 import QtCore
from pyde.ddi import DependencyScope
from weakref import WeakValueDictionary

class View: #(DependencyScope):
#     child_added = QtCore.pyqtSignal(QtCore.QObject)
    
    def __init__(self, name, parent=None, **kwargs):
#         super().__init__(name, parent)
        self.child = {}
        self.name = name
        self.config = kwargs
        if parent:
            parent.child[name] = self
        self.parent = parent
        self._widget = None
        for k,v in kwargs.items():
            setattr(self, k, v)

    @property
    def uri(self):
        if self.parent:
            uri = self.parent.uri + [self.name]
        else:
            uri = [self.name]
            
        return uri
    
    @property
    def widget(self):
        return self._widget
    
    @widget.setter
    def widget(self, value):
        self._widget = value
        value.view = self
    
    def set_focus(self):
        self.widget.parent().setCurrentWidget(self.widget)
        self.widget.setFocus()

    def delete(self):
        del self.parent.child[self.name]
        
    def dump_config(self, var_name):
        config = []
        for _, child in self.child.items():
            config_dump = []
            for name, c in child.config.items():
                config_dump.append("{}='{}'".format(name, str(c)))

            view_config = ','.join(["'" + child.name + "'", var_name] + config_dump)
            config.append("ddic.provide('view/{0}', ddic['cls/view']({1}))".format(child.name, view_config))
        
        
#         if var_name != "ddic['win']":
#             if self.parent:
#                 parent_ref = "ddic['{}']".format('/'.join(self.parent.uri))
#             else:
#                 parent_ref = 'None'
#                 
#             config_dump = []
#             for name, c in self.config.items():
#                 config_dump.append("{}='{}'".format(name, str(c)))
#             
#             view_config = ','.join(["'" + self.name + "'", parent_ref] + config_dump)
#             view_inst = ["ddic.provide('{}', ddic['cls/view']({}))".format('/'.join(self.uri), view_config)]
#         else:
#             view_inst = []
#             
#         for _, v in self.providers.items():
#             view_inst.append(v.dump_config(''))
        
        if hasattr(self.widget, 'dump_config'):
            config.append(self.widget.dump_config('.'.join([var_name, 'widget'])))
        
        return '\n'.join(config)
#         config = []
# #         config.append('from PyQt4.QtCore import Qt')
# #         config.append('from pyde.pyde_frame import ChildLayout, Layout')
#         config.append('{}.set_layout({})'.format(var_name, self._dump_config_rec(self.layout)))
#         return '\n'.join(config)
# 
#         for v in self.providers:
#             
#         view = ddic['cls/view']('scratch.py', ddic['win'], file_name=os.path.join(ddic['config/wspace/path'], 'scratch.py'))
#         ddic.provide('win/', view)
#         ddic['win'].widget.place(view, [0])
# 
#         view = ddic['cls/view']('interpret', ddic['win'])
#         ddic.provide('win/', view)
#         ddic['win'].widget.place(view, [1])

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
        if self.child:
            child = next(self.child.__iter__())
            return self.child[child].active_view()
        else:
            return self
