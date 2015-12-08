from pyde.pyde_widget import PydeWidget
from PyQt4.Qsci import QsciScintilla
from pyde.QsciScintillaCompat import QsciScintillaCompat

class PydeEditor(PydeWidget, QsciScintillaCompat):
    
    def __init__(self, name, parent=None):
        PydeWidget.__init__(self)
        self.name = name
        QsciScintillaCompat.__init__(self, parent)
        self.SendScintilla(QsciScintilla.SCI_SETCARETSTYLE, 2)
        self.SCN_MODIFIED.connect(self.__modified)
        
    @property
    def pos(self):
        return self.SendScintilla(QsciScintilla.SCI_GETCURRENTPOS)
    
    @pos.setter
    def pos(self, val):
        return self.SendScintilla(QsciScintilla.SCI_GOTOPOS, val)

    @property
    def anchor(self):
        return self.SendScintilla(QsciScintilla.SCI_GETANCHOR)
    
    @anchor.setter
    def anchor(self, val):
        return self.SendScintilla(QsciScintilla.SCI_SETANCHOR, val)

    def __modified(self, pos, mtype, text, length, linesAdded, line, foldNow,
                   foldPrev, token, annotationLinesAdded):
        pass
#         print(pos, hex(mtype), text, length, linesAdded, line, foldNow,
#                    foldPrev, token, annotationLinesAdded)
    
    def forward_char(self):
        self.SendScintilla(QsciScintilla.SCI_GOTOPOS, self.pos + 1)
        
    def backward_char(self):
        self.SendScintilla(QsciScintilla.SCI_GOTOPOS, self.pos - 1)
        
    def content_assist(self):
        self.autoCompleteFromAll()
        
#     def pos_changed(self, line, pos):
        

