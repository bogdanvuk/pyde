from pyde.pyde_widget import PydeWidget
from PyQt4.Qsci import QsciScintilla
from pyde.QsciScintillaCompat import QsciScintillaCompat
from pyde.ddi import Dependency, diinit
from pyde.plugins.context import ViewContext, BoundedSlice
from collections import OrderedDict
from pyde.view import View

class PydeEditor(QsciScintillaCompat):
    
    @diinit
    def __init__(self, name, parent_view, parent=None):
#         PydeWidget.__init__(self)
#         self.name = name
#         self.context = context
#         self.context.update_context([name], ViewContext(self))
        super(PydeEditor, self).__init__(parent)
        self.name = name
        self.view = View(self, parent_view.view)
#         View.__init__(self, name, parent_view)
        self.SendScintilla(QsciScintilla.SCI_SETCARETSTYLE, 2)
        self.SCN_MODIFIED.connect(self.__modified)
    
#     def focusInEvent(self, event):
#         self.parent_view.active_view()
#         self.context.set_active_path([BoundedSlice(None, self.name), 
#                                          BoundedSlice(self,self.pos)])
#         super().focusInEvent(event)
    
    def __getitem__(self, item):
        return self.text().__getitem__(item)
    
    def active_view(self):
        return self.view.active_view()
    

    @property
    def line(self):
        return self.lineAt(self.pos)

    @property
    def anchor(self):
        return self.SendScintilla(QsciScintilla.SCI_GETANCHOR)
    
    @anchor.setter
    def anchor(self, val):
        return self.SendScintilla(QsciScintilla.SCI_SETANCHOR, val)

    @property
    def pos(self):
        return self.SendScintilla(QsciScintilla.SCI_GETCURRENTPOS)
    
    @pos.setter
    def pos(self, val):
        return self.SendScintilla(QsciScintilla.SCI_GOTOPOS, val)

    def __modified(self, pos, mtype, text, length, linesAdded, line, foldNow,
                   foldPrev, token, annotationLinesAdded):
        pass
#         print(pos, hex(mtype), text, length, linesAdded, line, foldNow,
#                    foldPrev, token, annotationLinesAdded)

    def previous_line(self):
        self.SendScintilla(QsciScintilla.SCI_GOTOLINE, self.line - 1)
    
    def next_line(self):
        self.SendScintilla(QsciScintilla.SCI_GOTOLINE, self.line + 1)
    
    def forward_char(self):
        self.SendScintilla(QsciScintilla.SCI_GOTOPOS, self.pos + 1)
        
    def backward_char(self):
        self.SendScintilla(QsciScintilla.SCI_GOTOPOS, self.pos - 1)
        
    def beginning_of_view(self):
        self.SendScintilla(QsciScintilla.SCI_DOCUMENTSTART)

    def end_of_view(self):
        self.SendScintilla(QsciScintilla.SCI_DOCUMENTEND)
        
    def content_assist(self):
        self.autoCompleteFromAll()
        
    def active_range(self):
        return (0, len(self.text()))
        
#     def pos_changed(self, line, pos):
        

