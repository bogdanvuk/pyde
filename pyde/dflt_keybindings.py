from pyde.application import app
from pyde import actions 
from PyQt4.QtCore import Qt

def bind_keys():
    app.bind_key(actions.forward_char, Qt.Key_L, Qt.AltModifier, context='PydeEditor')
    app.bind_key(actions.backward_char, Qt.Key_J, Qt.AltModifier, context='PydeEditor')
    app.bind_key(actions.content_assist, Qt.Key_Space, Qt.ControlModifier, context='PydeEditor')
    app.bind_key(actions.evaluate, Qt.Key_Return, context='PyInerpretEditor')
    app.bind_key(actions.evaluate, Qt.Key_Enter, context='PyInerpretEditor')
    
    app.bind_key(app.globals.mark.new, Qt.Key_Space, Qt.AltModifier, context='PydeEditor')
    app.bind_key(app.globals.mark.prev, Qt.Key_P, Qt.AltModifier, context='PydeEditor')
    app.bind_key(app.globals.mark.next, Qt.Key_P, Qt.AltModifier + Qt.ShiftModifier, context='PydeEditor')
#     app.bind_key(actions.evaluate, Qt.Key_Tab, context='PyInerpretEditor')
