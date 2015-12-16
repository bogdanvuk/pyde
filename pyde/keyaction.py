from PyQt4 import QtCore
from pyde.ddi import Dependency

class KeyAction:
    def __init__(self, action, key, dispatcher : Dependency('key_dispatcher'), context : Dependency('context'), modifier=QtCore.Qt.NoModifier, uri = '/', args=(), kwargs={}):
        self.dispatcher = dispatcher
        self.dispatcher.register_keyaction(self)
        self.action = action
        self.context_uri = uri
        self.context = context
        self.key = key
        self.modifier = modifier
        self.action_args = args
        self.action_kwargs = kwargs

    def event(self, source, event):
        if (str(self.context.active_uri()).startswith(self.context_uri) and
            event.key() == self.key and
            int(event.modifiers()) == self.modifier):
            
            self.action(*self.action_args, **self.action_kwargs)
            return True
            
        return False
