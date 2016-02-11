from pyde.pyde_frame import PydeFrame, ChildLayout, Layout
from PyQt4 import QtCore
from pyde.ddi import Dependency, ddic

def get_layout():
#     pyde.application.app.add_layout(PydeFrame(None, children=[PythonEdit(), PyInerpretEditor()], stretch=[5, 1]))
    return PydeFrame(Layout(QtCore.Qt.Vertical, [ChildLayout(5, None), ChildLayout(1, None)]))
    
def reload_buffers(win : Dependency(feature='win')):
    s = ddic['cls/editor_generic']('scratch.py', parent_view=win)
    i = ddic['cls/ipython']('interpret', parent_view=win)
    win.place_view(s, [0])
    win.place_view(i, [1])
#     win.centralWidget.widget(1).currentWidget().setFocus()

