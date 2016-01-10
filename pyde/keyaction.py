from PyQt4 import QtCore
from pyde.ddi import Dependency
from pyde.plugins.context import uri2str

def KeyActionDfltCondition(key_action, active_view, event):
    return (uri2str(active_view.uri).startswith(key_action.view_uri) and
            event.key() == key_action.key and
            int(event.modifiers()) == key_action.modifier)

class KeyAction:
    def __init__(self, action, key, 
                 dispatcher : Dependency('key_dispatcher'), 
#                  context : Dependency('context'), 
                 condition = KeyActionDfltCondition, 
                 modifier=QtCore.Qt.NoModifier, 
                 uri = '/', args=(), kwargs={}):
        
        self.dispatcher = dispatcher
        self.dispatcher.register_keyaction(self)
        self.action = action
        self.view_uri = uri
#         self.context = context
        self.key = key
        self.modifier = modifier
        self.action_args = args
        self.action_kwargs = kwargs
        self.condition = condition

    def event(self, source, event):
        active_view = source.active_view()
        if self.condition(self, active_view, event):
            self.action(*self.action_args, **self.action_kwargs)
            return True
            
        return False
