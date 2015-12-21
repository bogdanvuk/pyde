from PyQt4 import QtCore
from pyde.ddi import Dependency
from pyde.plugins.context import uri2str

def KeyActionDfltCondition(key_action, source, event):
    context = key_action.context.active_context()
    if context:
        return (uri2str(context.uri).startswith(key_action.context_uri) and
                event.key() == key_action.key and
                int(event.modifiers()) == key_action.modifier)
    else:
        return False

class KeyAction:
    def __init__(self, action, key, 
                 dispatcher : Dependency('key_dispatcher'), 
                 context : Dependency('context'), 
                 condition = KeyActionDfltCondition, 
                 modifier=QtCore.Qt.NoModifier, 
                 uri = '/', args=(), kwargs={}):
        
        self.dispatcher = dispatcher
        self.dispatcher.register_keyaction(self)
        self.action = action
        self.context_uri = uri
        self.context = context
        self.key = key
        self.modifier = modifier
        self.action_args = args
        self.action_kwargs = kwargs
        self.condition = condition

    def event(self, source, event):
        if self.condition(self, source, event):
            return self.action(*self.action_args, **self.action_kwargs)
            
        return False
