from pyde.pyde_frame import PydeFrame
from PyQt4 import QtCore
from pyde.ddi import Dependency, ddic

def set_layout(app : Dependency(feature='app')):
#     pyde.application.app.add_layout(PydeFrame(None, children=[PythonEdit(), PyInerpretEditor()], stretch=[5, 1]))
    app.add_layout(PydeFrame(QtCore.Qt.Vertical, [5, 1]))
    
def reload_buffers(app : Dependency(feature='app')):
    app.add_view(ddic['cls.python'](), [0])
    app.add_view(ddic['cls.ipython'](), [1])
#     app.centralWidget.widget(0).insertWidget(0, )
#     app.centralWidget.widget(1).insertWidget(0, PyInerpretEditor())
    app.centralWidget.widget(1).currentWidget().setFocus()

