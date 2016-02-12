from PyQt4.QtCore import QObject, pyqtSlot
from pyde.ddi import Dependency, ddic
from PyQt4.QtGui import QWidget
from PyQt4 import QtCore, QtGui
import fnmatch
from pyde.plugins.context import uri2str

class KeyDispatcher(QObject):
#     def __init__(self, view, action, key, modifier=QtCore.Qt.NoModifier, args=(), kwargs={}):
    def __init__(self, win : Dependency('win'), context : Dependency('context')):
        super().__init__()
        self.win = win
        self.context = context

        for v in win:
            self.view_added(win, v)
             
        win.provided.connect(self.view_added)
        
#         ddic.provide_on_demand('cls/key_dispatcher_view_add', self.add_view)
        self.actions = []
        
    def view_added(self, view, child_name):
        view[child_name].widget.installEventFilter(self)
    
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
#             if event.key() == QtCore.Qt.Key_Tab:
#                 pass
            active_view = source.active_view()
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

    