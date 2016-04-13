from PyQt5.QtCore import QObject, pyqtSlot
from ddi.ddi import Dependency, ddic
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtWidgets
import fnmatch
from pyde.plugins.parser import uri2str

class KeyDispatcher(QObject):
    def __init__(self):
        super().__init__()
        ddic.provide_on_demand(provider=self.view_added)
        self.actions = []
        
    def view_added(self, widget : Dependency('widget/*', lambda w: hasattr(w, 'view'))):
        widget.installEventFilter(self)
    
    def register_keyaction(self, action, uri_filter='*'):
        uri_split = uri_filter.split('/')
        uri_levels = len(uri_split)
        if uri_levels > len(self.actions):
            self.actions.extend([ [] for _ in range(uri_levels - len(self.actions))])
            
        self.actions[uri_levels - 1].append((uri_filter, action))
         
#         self.actions.append(action)
    
    def eventFilter(self, source, event):
#         resp = False
#         active_view = None
        if (event.type() == QtCore.QEvent.KeyPress):
            active_view = source.view.active_view()
#             print(hex(int(event.modifiers())))
#             print(event.key())
#             active_view = source.view
            if active_view is not None:
                while active_view.parent is not None:
                    for actions in reversed(self.actions):
                        for a in actions:
                            if fnmatch.fnmatch(uri2str(active_view.uri), a[0]):
                                ret = a[1].event(active_view, event)
                                if ret:
    #                                 import gc
    #                                 ref = gc.get_referrers(active_view)
    #                                 refw = gc.get_referrers(active_view.widget)
    
                                    return True
                
                    active_view = active_view.parent
        

        return QtWidgets.QWidget.eventFilter(self, source, event)

    