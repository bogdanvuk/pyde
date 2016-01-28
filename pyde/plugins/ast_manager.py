from PyQt4.Qsci import QsciScintilla
from PyQt4 import QtCore, QtGui
from pyde.ddi import Dependency
from pyde.plugins.parser import Antlr4GenericParser

class EditorAstManager(QtCore.QObject):
    
    tree_modified = QtCore.pyqtSignal(object) #['QWidget'])
    
    def __init__(self, mode : Dependency('mode/inst/')):
        super().__init__()
        self.qthread = QtCore.QThread()
        self.moveToThread(self.qthread)
        if mode.name in ['python', 'ipython']:
            language = 'python3'
            start_rule = 'file_input'
        else:
            language = mode.name
            start_rule = 'main'
            
        self.parser = Antlr4GenericParser(language, start_rule)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.parse)
        self.timer.start(1000)
        self.qthread.start()
        self.editor = mode.editor.widget
        self.editor.ast = self
        self.mode = mode
        self.language = language
        self.editor.SCN_MODIFIED.connect(self.text_modified)
        self.dirty = True
        self.ast = None
 
    def __del__(self):
        self.qthread.quit()
 
    def text_modified(self, pos, mtype, text, length, linesAdded, line, foldNow,
                   foldPrev, token, annotationLinesAdded):
          
        if ((mtype & QsciScintilla.SC_MOD_INSERTTEXT) != 0) or \
            ((mtype & QsciScintilla.SC_MOD_DELETETEXT) != 0):
            self.dirty = True

    def read_only(self, cmd):
        print('begin ast.read_only')
        self.parse()
        cmd(self.editor, self.parser)
        print('end ast.read_only')

    def parse(self):
        if self.dirty:
            self.dirty = False
            self.parser.parse(self.editor.text(), self.editor.active_range())
            self.tree_modified.emit(self.ast)
            
    def completion_suggestions(self, cmd):
        self.parse()
        self.suggestions = self.parser.completion_suggestions(self.editor.text(), self.editor.active_range())
        for s in self.suggestions:
            if s.feature:
                method_name = '_'.join(['complete', s.type, s.feature])
            else:
                method_name = '_'.join(['complete', s.type])
                
            if hasattr(cmd, method_name):
                getattr(cmd, method_name)(self.editor, s.node)
#             self.tree_modified.emit(self.ast)


class IPythonEditorAstManager(EditorAstManager):

    def parse(self):
        if self.dirty:
            self.dirty = False
            self.ast = self.parser.parse(self.editor.text(), self.editor.cmd_range())
            self.tree_modified.emit(self.ast)
