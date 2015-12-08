from pyde.pyde_frame import PydeFrame
from PyQt4 import QtCore
from pyde.ddi import Dependency, ddic

def get_layout():
#     pyde.application.app.add_layout(PydeFrame(None, children=[PythonEdit(), PyInerpretEditor()], stretch=[5, 1]))
    return PydeFrame(QtCore.Qt.Vertical, [5, 1])
    
def reload_buffers(win : Dependency(feature='win')):
    win.add_view(ddic['cls.python']('*scratch.py*'), [0])
    win.add_view(ddic['cls.ipython']('*interpret*'), [1])
#     app.centralWidget.widget(0).insertWidget(0, )
#     app.centralWidget.widget(1).insertWidget(0, PyInerpretEditor())
    win.centralWidget.widget(1).currentWidget().setFocus()

