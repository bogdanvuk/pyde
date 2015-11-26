from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSlot, QObject
from pyde.application import app

class MarkActivator(QObject):
    def __init__(self):
        super().__init__()
        app.view_added.connect(self.new_view)
    
    @pyqtSlot(QWidget)
    def new_view(self, obj):
        obj.textChanged.connect(self.text_changed)
        
    @pyqtSlot()
    def text_changed(self):
        try:
            mark_prev = app.globals.mark.cur()
        except IndexError:
            mark_prev = None
        app.globals.mark.new()
        mark_cur = app.globals.mark.cur()
        if mark_prev:
            if (mark_cur.editor == mark_prev.editor) \
                and (mark_cur.line == mark_prev.line):
                app.globals.mark.pop()
            
            
            
        
#     def new_view(self):
#         print("VIEW ADDED!")

app.register_global("mark_activator", MarkActivator())
# app.view_added.connect(app.globals.mark_activator.new_view)
