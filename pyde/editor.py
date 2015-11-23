from pyde.pyde_widget import PydeWidget
from PyQt4.Qsci import QsciScintilla

class PydeEditor(PydeWidget, QsciScintilla):
    
    def __init__(self, parent=None):
        PydeWidget.__init__(self)
        QsciScintilla.__init__(self, parent)
        self.SendScintilla(QsciScintilla.SCI_SETCARETSTYLE, 2)
    
    def pos(self):
        return self.SendScintilla(QsciScintilla.SCI_GETCURRENTPOS)
    
    def forward_char(self):
        self.SendScintilla(QsciScintilla.SCI_GOTOPOS, self.pos() + 1)
        
    def backward_char(self):
        self.SendScintilla(QsciScintilla.SCI_GOTOPOS, self.pos() - 1)
        
    def content_assist(self):
        self.autoCompleteFromAll()

