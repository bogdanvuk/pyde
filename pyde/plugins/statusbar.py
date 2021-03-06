from pyde.ddi import Dependency, Amendment, ddic
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QLineEdit, QFont
from pyde.plugins.editor_mode import ViewMode

class StatusbarMode(ViewMode):
    name = '__statusbar__'
    
    def __init__(self, view : Amendment('view/', lambda v: v.name == '__statusbar__')):
        super().__init__(view)

class Statusbar(QLineEdit):

    def __init__(self, view: Amendment('view/', lambda v: hasattr(v, 'mode') and (v.mode.name == '__statusbar__') and (v.widget is None))):
        super().__init__()
        self.view = view
        self.view.widget = self
        font = QFont()
        font.setFamily('DejaVu Sans Mono')
        font.setFixedPitch(True)
        font.setPointSize(10)    
        self.setFont(font);
        
    def cycle_frame(self, old):
        return False

class DefStatusProvider:
    def __init__(self, view: Amendment('view/', lambda v: (v.name != '__statusbar__') and (not hasattr(v, 'status_provider')))):
        super().__init__()
        self.view = view
        self.view.status_provider = self
        self.view.focus_in.connect(self.capture_statusbar)
        self.view.focus_out.connect(self.release_statusbar)
        self.fields = []
        self.add_field('dirty')
        self.add_field('view', dflt=self.view.name)
        self.active = False

    def add_field(self, name, formatting='{}', position=None, dflt=''):
        field = {'name':name, 'formatting':formatting, 'val':dflt}
        if position is None:
            self.fields.append(field)
        else:
            self.fields.insert(position, field)
    
    def capture_statusbar(self, view):
        self.active = True
        self.refresh()

    def release_statusbar(self, view):
        self.active = False
        
    def set(self, name, val):
        field = [f for f in self.fields if f['name'] == name]
        if field:
            field = field[0]
        else:
            return
        
        field['val'] = val
        self.refresh()
    
    def refresh(self):
        if 'view/__statusbar__' in ddic:
            vals = []
            formatting = ''
            for f in self.fields:
                formatting += f['formatting']
                vals.append(f['val'])
                
            ddic['view/__statusbar__'].widget.setText(formatting.format(*vals))
    
    def cycle_frame(self, old):
        return False


# class StatusBar(QtGui.QStatusBar):
#     def __init__(self, app: Dependency('app'), win : Dependency('win')):
#         super().__init__(win.widget)
# 
#         self.setObjectName("statusbar")
#         win.widget.setStatusBar(self)
#         app.focusChanged.connect(self.view_changed_focus)
# 
#     def view_changed_focus(self, old, now):
#         if now:
#             name = getattr(now.view, 'name', '')
#             self.showMessage(name)
        