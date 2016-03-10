from PyQt4.QtCore import QObject, pyqtSlot
from pyde.ddi import Dependency, ddic
from PyQt4.QtGui import QWidget
from PyQt4 import QtCore, QtGui
import fnmatch
from pyde.plugins.parser import uri2str

class KeyDispatcher(QObject):
    def __init__(self):
        super().__init__()
        ddic.provide_on_demand(provider=self.view_added)
        self.actions = []
        
    def view_added(self, view : Dependency('view/', lambda v: v.widget is not None)):
        view.widget.installEventFilter(self)
    
    def register_keyaction(self, action, uri_filter='*'):
        uri_split = uri_filter.split('/')
        uri_levels = len(uri_split)
        if uri_levels > len(self.actions):
            self.actions.extend([ [] for _ in range(uri_levels - len(self.actions))])
            
        self.actions[uri_levels - 1].append((uri_filter, action))
         
#         self.actions.append(action)
    
    def eventFilter(self, source, event):
#         resp = False
        if (event.type() == QtCore.QEvent.KeyPress):
            if event.key() == 75:
                pass
            print(event.key())
            active_view = source.active_view()
#             active_view = source.view
            while active_view.parent is not None:
                for actions in reversed(self.actions):
                    for a in actions:
                        if fnmatch.fnmatch(uri2str(active_view.uri), a[0]):
                            ret = a[1].event(active_view, event)
                            if ret:
                                return True
            
                active_view = active_view.parent

        
#         if resp:
#             return True
#         else:
        return QtGui.QWidget.eventFilter(self, source, event)

    