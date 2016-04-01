from PyQt5 import QtCore
from pyde.ddi import Dependency

def KeyActionDfltCondition(key_action, active_view, event):
#     return (fnmatch.fnmatch(uri2str(active_view.uri), key_action.view_uri) and
    return  (event.key() == key_action.key and
            int(event.modifiers()) == key_action.modifier)

class KeyAction:
    def __init__(self, action, key, 
                 dispatcher : Dependency('key_dispatcher'), 
#                  context : Dependency('context'), 
                 condition = KeyActionDfltCondition, 
                 modifier=QtCore.Qt.NoModifier, 
                 uri = '*', args=(), kwargs={}):
        
        self.dispatcher = dispatcher
        self.dispatcher.register_keyaction(self, uri)
        self.action = action
        self.view_uri = uri
#         self.context = context
        self.key = key
        self.modifier = modifier
        self.action_args = args
        self.action_kwargs = kwargs
        self.condition = condition

    def event(self, active_view, event):
        if self.condition(self, active_view, event):
#             sig = signature(self.action)
#             self.action
            self.action(*self.action_args, active_view = active_view, **self.action_kwargs)
            return True
            
        return False
