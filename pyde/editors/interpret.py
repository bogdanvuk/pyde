import sys

from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from pyde.editor import PydeEditor
from PyQt5.QtGui import QFont, QFontMetrics, QColor
from ddi.ddi import ddic, Amendment

class PyInerpretEditor(PydeEditor):
                            
    def __init__(self, view: Amendment('view/*', lambda v: all([hasattr(v, a) for a in ['mode', 'status_provider', 'filebuf']]) and (v.mode.name == 'ipython') and (v.widget is None))): #, orig_editor=None):
        if view.widget is None:
            self.globals = {}
            self.globals['ddic'] = ddic
            for name, a in ddic.filter('actions/*'):
                self.globals[name.partition('/')[-1]] = a
                
            self.locals = {}
#             ddic.provide('interactive', -1)
        else:
            self.globals = view.widget.globals
            self.locals = view.widget.locals
        
        super().__init__(view)

        # Set the default font
        font = QFont()
        font.setFamily('DejaVu Sans Mono')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
#        self.parser = Parser(self, 'python3')
#         self.ca = PyInterpretContentAssist()
        fontmetrics = QFontMetrics(font)

        # Brace matching: enable for a brace immediately before or after
        # the current position
        #
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))

        # Set Python lexer
        # Set style for Python comments (style number 1) to a fixed-width
        # courier.
        #
#         self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'DejaVu Sans Mono'.encode())
        

        # Don't want to see the horizontal scrollbar at all
        # Use raw message to Scintilla here (all messages are documented
        # here: http://www.scintilla.org/ScintillaDoc.html)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)
        self.SendScintilla(QsciScintilla.SCI_SETVSCROLLBAR, 0)
#         self.SendScintilla(QsciScintilla.SCI_AUTOCSETTYPESEPARATOR, ord('`'))
        self.SendScintilla(QsciScintilla.SCI_AUTOCSETSEPARATOR, 1)
        self.SendScintilla(QsciScintilla.SCI_AUTOCSETTYPESEPARATOR, 1)
        
        
        self.setMinimumSize(fontmetrics.width("00000"), fontmetrics.height()+4)
        
        self.markerDefine(QsciScintilla.RightArrow,
            self.ARROW_MARKER_NUM)
#         self.setMarkerBackgroundColor(QColor("#ee1111"),
#             self.ARROW_MARKER_NUM)

        self.prompt_begin = 0
        self.focus_view = None
        self.interactive = False
        
    @property
    def prompt_begin(self):
        return self._prompt_begin
    
    @prompt_begin.setter
    def prompt_begin(self, value):
        if hasattr(self, '_prompt_begin'):
            self.markerDeleteAll(self.ARROW_MARKER_NUM)
            
        self._prompt_begin = value
        self.markerAdd(self.lineIndexFromPosition(self._prompt_begin)[0], self.ARROW_MARKER_NUM)

#     def active_text(self):
# #         start, stop = self.active_range()
#         return super().text()[self.prompt_begin:self.length()]
    
#     def active_range(self):
#         return (self.prompt_begin, self.length())

    def is_interactive(self):
        return self.interactive

    def cycle_frame(self, old):
        return False

    def cmd_range(self):
        return (self.prompt_begin, self.length())
    
    def cmd_text(self):
        return self.text()[self.prompt_begin:self.length()]

    def execute_view_action(self, view, interactive=False):
        self.focus_view = view
        self.view.set_focus()
        if interactive:
            self.interactive = 0
            self.SCN_MODIFIED.connect(self.text_modified)
        else:
            self.interactive = -1
#         ddic['actions/switch_view'](self.view, self.view.last_location)

    def text_modified(self, pos, mtype, text, length, linesAdded, line, foldNow,
                   foldPrev, token, annotationLinesAdded):
          
        if ((mtype & QsciScintilla.SC_MOD_INSERTTEXT) != 0) or \
            ((mtype & QsciScintilla.SC_MOD_DELETETEXT) != 0):
            self._evaluate()
            self.interactive += 1

    def _evaluate(self):
        if self.focus_view is not None:
            ddic['actions/switch_view'](self.focus_view, self.focus_view.widget.loc)

        cmd = self.cmd_text()
        ddic['interactive'] = self.interactive
        try:
            eval(cmd, self.globals, self.locals)
        except:
            print('\n{0}: {1}\n'.format(sys.exc_info()[0].__name__, sys.exc_info()[1]))
        ddic['interactive'] = -1
        self.view.set_focus()

    def cancel(self):
        self.SendScintilla(QsciScintilla.SCI_DELETERANGE, self.prompt_begin, self.length() - self.prompt_begin)
        if self.focus_view is not None:
            ddic['actions/switch_view'](self.focus_view, self.focus_view.widget.loc)

    def evaluate(self):
        if self.focus_view is not None:
            ddic['actions/switch_view'](self.focus_view, self.focus_view.widget.loc)
            self.focus_view = None
            if self.interactive >= 0:
                self.SCN_MODIFIED.disconnect(self.text_modified)
                
        cmd = self.cmd_text()
        
        self.pos = self.length()
        
        try:
             
            ret = eval(cmd, self.globals, self.locals)
            if ret is not None:
                ret_str = '\n' + str(ret) + '\n'
            else:
                ret_str = '\n'
                 
#                 stdout_text = buffer.getvalue()
#                 if stdout_text:
#                     ret_str += stdout_text
             
            self.insert(ret_str)
        except SyntaxError:
            exec(cmd, self.globals, self.locals)
            self.insert('\n')
        except:
            self.insert('\n{0}: {1}\n'.format(sys.exc_info()[0].__name__, sys.exc_info()[1]))
        
#             sys.stdout = sys.__stdout__
#             self.setCursorPosition(self.lines(), 0)
        self.pos = self.length()
        self.prompt_begin = self.length()
