from pyde.application import app
from pyde import actions 
from PyQt4.QtCore import Qt

def bind_keys():
    app.bind_key(actions.forward_char, Qt.Key_L, Qt.AltModifier, context='PydeEditor')
    app.bind_key(actions.backward_char, Qt.Key_J, Qt.AltModifier, context='PydeEditor')
    app.bind_key(actions.content_assist, Qt.Key_Space, Qt.ControlModifier, context='PydeEditor')
    app.bind_key(actions.evaluate, Qt.Key_Return, context='PyInerpretEditor')
    app.bind_key(actions.evaluate, Qt.Key_Enter, context='PyInerpretEditor')
