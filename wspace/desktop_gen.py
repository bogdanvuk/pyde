from pyde.application import app
from pyde.editors.python import PythonEdit
from pyde.editors.interpret import PyInerpretEditor 
from pyde.pyde_frame import PydeFrame
from PyQt4 import QtCore

def set_layout():
#     pyde.application.app.add_layout(PydeFrame(None, children=[PythonEdit(), PyInerpretEditor()], stretch=[5, 1]))
    app.add_layout(PydeFrame(QtCore.Qt.Vertical, [5, 1]))
    
def reload_buffers():
    app.add_view(PythonEdit(), [0])
    app.add_view(PyInerpretEditor(), [1])
#     app.centralWidget.widget(0).insertWidget(0, )
#     app.centralWidget.widget(1).insertWidget(0, PyInerpretEditor())
#     app.centralWidget.widget(1).currentWidget().setFocus()

