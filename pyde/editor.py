from PyQt4.Qsci import QsciScintilla
from pyde.QsciScintillaCompat import QsciScintillaCompat
from pyde.ddi import Amendment
import os
from PyQt4.QtCore import Qt

class PydeEditor(QsciScintillaCompat):
    
#     @diinit
    def __init__(self, view: Amendment('view/', lambda v: hasattr(v, 'mode') and hasattr(v, 'status_provider') and hasattr(v, 'filebuf') and (v.widget is None)), orig_editor=None):
        if orig_editor:
            super(PydeEditor, self).__init__()
            self.setDocument(orig_editor.document())
        else:
            super(PydeEditor, self).__init__(view.parent.widget)
            view.widget = self
            self.setAttribute(Qt.WA_KeyCompression)
            self.hide()
            self.setText(view.filebuf.load())
            self.setModified(False)
#             if hasattr(view, 'file_name'):
#                 self.file_name = view.file_name
#                 self.read_file(self.file_name)
#             else:
#                 self.file_name = None
                
        self.SendScintilla(QsciScintilla.SCI_SETCARETSTYLE, 2)
#         self.SCN_MODIFIED.connect(self.__modified)
        self.cursorPositionChanged.connect(self.__cursorPositionChanged)
        self.view.status_provider.add_field('line_pos', formatting='{:>15}')
#         self.SCN_PAINTED.connect(self.__painted)

    def clone(self):
        return self.__class__(view=None, orig_editor = self)

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

    def __cursorPositionChanged(self, line, index):
        self.view.status_provider.set('line_pos', 'L{}:C{}:{}%'.format(line, index, round(line*100/self.lines())))

    def __modified(self, pos, mtype, text, length, linesAdded, line, foldNow,
                   foldPrev, token, annotationLinesAdded):
        pass
#         print(pos, hex(mtype), text, length, linesAdded, line, foldNow,
#                    foldPrev, token, annotationLinesAdded)

    def read_file(self, fn):
        if os.path.exists(fn):
            with open(fn, 'r') as f:
                self.setText(f.read())
        else:
            with open(fn, "w"):
                pass
            
            self.setText('')

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

    def beginning_of_line(self):
        self.SendScintilla(QsciScintilla.SCI_HOME)

    def end_of_line(self):
        self.SendScintilla(QsciScintilla.SCI_LINEEND)
        
    def content_assist(self):
        self.autoCompleteFromAll()
        
    def active_range(self):
        return (0, len(self.text()))
    
    def dump_config(self, var_name):
        config = []
        config.append('{}.pos = {}'.format(var_name, self.pos))
        config.append('{}.anchor = {}'.format(var_name, self.anchor))
        return '\n'.join(config)
        
#     def pos_changed(self, line, pos):
        

