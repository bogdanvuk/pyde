from PyQt4.Qsci import QsciScintilla
from pyde.QsciScintillaCompat import QsciScintillaCompat
from pyde.ddi import Amendment
import os
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QColor

class PydeEditor(QsciScintillaCompat):
    
#     @diinit
    def __init__(self, view: Amendment('view/', lambda v: hasattr(v, 'mode') and hasattr(v, 'status_provider') and hasattr(v, 'filebuf') and (v.widget is None))): #, orig_editor=None):
        self.view = view
        if view.widget is not None:
            super(PydeEditor, self).__init__()
            self.setDocument(view.widget.document())
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
        
#         self.indicators = {}
#         self.indicators['search'] = self.indicatorDefine(QsciScintilla.INDIC_ROUNDBOX, QColor(0xdd, 0xff, 0xdd, 100))
        
        
#         self.SCN_PAINTED.connect(self.__painted)

    def clone(self):
        return self.__class__(view=self.view) #, orig_editor = self)

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

    def del_forward_char(self):
        self.SendScintilla(QsciScintilla.SCI_CLEAR)
        
    def del_backward_char(self):
        self.SendScintilla(QsciScintilla.SCI_DELETEBACK)
        
    def forward_word(self):
        self.SendScintilla(QsciScintilla.SCI_WORDRIGHTEND)
        
    def backward_word(self):
        self.SendScintilla(QsciScintilla.SCI_WORDLEFTEND)

    def forward_page(self):
        self.SendScintilla(QsciScintilla.SCI_PAGEDOWN)
        
    def backward_page(self):
        self.SendScintilla(QsciScintilla.SCI_PAGEUP)
        
    def beginning_of_view(self):
        self.SendScintilla(QsciScintilla.SCI_DOCUMENTSTART)

    def end_of_view(self):
        self.SendScintilla(QsciScintilla.SCI_DOCUMENTEND)

    def beginning_of_line(self):
        self.SendScintilla(QsciScintilla.SCI_HOME)

    def end_of_line(self):
        self.SendScintilla(QsciScintilla.SCI_LINEEND)
    
    def _doSearchTarget(self):
        """
        Private method to perform the search in target.
        
        @return flag indicating a successful search (boolean)
        """
        if self.__targetSearchStart == self.__targetSearchEnd:
            self.__targetSearchActive = False
            return False
        
        self.SendScintilla(QsciScintilla.SCI_SETTARGETSTART,
                           self.__targetSearchStart)
        self.SendScintilla(QsciScintilla.SCI_SETTARGETEND,
                           self.__targetSearchEnd)
        self.SendScintilla(QsciScintilla.SCI_SETSEARCHFLAGS,
                           self.__targetSearchFlags)
        pos = self.SendScintilla(QsciScintilla.SCI_SEARCHINTARGET,
                                 len(self.__targetSearchExpr),
                                 self.__targetSearchExpr.encode())
        
        if pos == -1:
            self.__targetSearchActive = False
            return pos
        
        targend = self.SendScintilla(QsciScintilla.SCI_GETTARGETEND)
        self.__targetSearchStart = targend
        
        return pos
    
    def search(self, expr_, start=-1, end=-1, 
                        re_=False, cs_=False, wo_=False, ws_=False):
        """
        Public method to search in a specified range of text without
        setting the selection.
        
        @param expr_ search expression (string)
        @param re_ flag indicating a regular expression (boolean)
        @param cs_ flag indicating a case sensitive search (boolean)
        @param wo_ flag indicating a word only search (boolean)
        @keyparam begline line number to start from (-1 to indicate current
            position) (integer)
        @keyparam begindex index to start from (-1 to indicate current
            position) (integer)
        @keyparam endline line number to stop at (-1 to indicate end of
            document) (integer)
        @keyparam endindex index number to stop at (-1 to indicate end of
            document) (integer)
        @keyparam ws_ flag indicating a word start search (boolean)
        @return flag indicating a successful search (boolean)
        """
        self.__targetSearchFlags = 0
        if re_:
            self.__targetSearchFlags |= QsciScintilla.SCFIND_REGEXP
        if cs_:
            self.__targetSearchFlags |= QsciScintilla.SCFIND_MATCHCASE
        if wo_:
            self.__targetSearchFlags |= QsciScintilla.SCFIND_WHOLEWORD
        if ws_:
            self.__targetSearchFlags |= QsciScintilla.SCFIND_WORDSTART
        
        if start < 0:
            self.__targetSearchStart = self.SendScintilla(
                QsciScintilla.SCI_GETCURRENTPOS)
        else:
            self.__targetSearchStart = start
        
        if end < 0:
            self.__targetSearchEnd = self.SendScintilla(
                QsciScintilla.SCI_GETTEXTLENGTH)
        else:
            self.__targetSearchEnd = end
        
        self.__targetSearchExpr = expr_
        
        if self.__targetSearchExpr:
            self.__targetSearchActive = True
            
            return self._doSearchTarget()
        
        return False
    
#     def search(self, text):
#         if text:
#             pos = self.findFirstTarget(text, False, False, False, start = self.anchor)
#             if pos >= 0:
#     #             self.clearAllIndicators(self.indicators['search'])
#     #             self.setIndicatorRange(self.indicators['search'], pos, len(text))
#                 self.anchor = pos
#                 self.pos = pos
#                 self.SendScintilla(QsciScintilla.SCI_SETSELECTIONEND, pos+len(text))
        
    def content_assist(self):
        self.autoCompleteFromAll()
        
    def active_range(self):
        return (0, len(self.text()))
    
    def showFindIndicator(self, start, end):
        """
        Public method to show the find indicator for the given range.
        
        """
        if hasattr(QsciScintilla, "SCI_FINDINDICATORSHOW"):
            self.SendScintilla(QsciScintilla.SCI_FINDINDICATORSHOW, start, end)
    
    def dump_config(self, var_name):
        config = []
        config.append('{}.pos = {}'.format(var_name, self.pos))
        config.append('{}.anchor = {}'.format(var_name, self.anchor))
        return '\n'.join(config)
        
#     def pos_changed(self, line, pos):
        

