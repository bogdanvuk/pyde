from PyQt4.Qsci import QsciScintilla
from PyQt4 import QtCore, QtGui
from pyde.ddi import Dependency
from pyde.plugins.parser import Antlr4GenericParser

class EditorAstManager(QtCore.QObject):
    
    tree_modified = QtCore.pyqtSignal(object) #['QWidget'])
    suggestions_created = QtCore.pyqtSignal(object, object, object) #['QWidget'])
    
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
        self.editor = mode.view.widget
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
        self.parse()
        cmd(self.editor, self.parser)

    def parse(self):
        if self.dirty:
            self.dirty = False
            self.parser.parse(self.editor.text(), self.editor.active_range())
            self.tree_modified.emit(self.ast)
            
    def completion_suggestions(self, cmd):
        self.parse()
        carret_pos = self.editor.pos
        self.suggestions = self.parser.completion_suggestions(self.editor.text(), (self.editor.active_range()[0], carret_pos))
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
            
    def completion_suggestions(self, cmd):
        self.parse()
        carret_pos = self.editor.pos
        cmd_range = self.editor.active_range()
        if (carret_pos >= cmd_range[0]) and (carret_pos <= cmd_range[1]): 
            self.suggestions = self.parser.completion_suggestions(self.editor.text(), (cmd_range[0], carret_pos))
            self.suggestions_created.emit(self.suggestions, self.editor.text(), (cmd_range[0], carret_pos))
            for s in self.suggestions:
                if s.feature:
                    method_name = '_'.join(['complete', s.type, s.feature[0]])
                else:
                    method_name = '_'.join(['complete', s.type])
                    
                if hasattr(cmd, method_name):
                    if s.feature:
                        getattr(cmd, method_name)(self.editor, s.node, s.feature, s.parse_node)
                    else:
                        getattr(cmd, method_name)(self.editor, s.node, s.parse_node)
