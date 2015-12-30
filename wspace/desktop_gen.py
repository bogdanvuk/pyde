from pyde.pyde_frame import PydeFrame
from PyQt4 import QtCore
from pyde.ddi import Dependency, ddic

def get_layout():
#     pyde.application.app.add_layout(PydeFrame(None, children=[PythonEdit(), PyInerpretEditor()], stretch=[5, 1]))
    return PydeFrame(QtCore.Qt.Vertical, [5, 1])
    
def reload_buffers(win : Dependency(feature='win')):
#     ddic.provide_on_demand('cls/python', inst_feature='view/*scratch.py*', inst_kwargs={'parent': win})
#     ddic.provide_on_demand('cls/ipython', inst_feature='view/*interpret*', inst_kwargs={'parent': win})


    ddic.provide('view/*scratch.py*', ddic['cls/python']('*scratch.py*', parent=win))
    ddic.provide('view/*interpret*', ddic['cls/ipython']('*interpret*', parent=win))
    win.place_view(ddic['view/*scratch.py*'], [0])
    win.place_view(ddic['view/*interpret*'], [1])
#     app.centralWidget.widget(0).insertWidget(0, )
#     app.centralWidget.widget(1).insertWidget(0, PyInerpretEditor())
    win.centralWidget.widget(1).currentWidget().setFocus()

