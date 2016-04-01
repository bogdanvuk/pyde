from PyQt5.Qsci import QsciScintilla
from PyQt5 import QtCore, QtWidgets
from pyde.ddi import Dependency, Amendment, ddic
from pyde.plugins.parser import Antlr4GenericParser

class EditorAstManager(QtCore.QObject):
    
    tree_modified = QtCore.pyqtSignal(object) #['QWidget'])
    suggestions_created = QtCore.pyqtSignal(object, object, object) #['QWidget'])
    
    def __init__(self, view : Amendment('view/*', lambda v: v.widget is not None)):
        super().__init__()
        self.qthread = QtCore.QThread()
        self.moveToThread(self.qthread)
#         if view.mode.name in ['python', 'ipython']:
#             language = 'python3'
#             start_rule = 'file_input'
#         else:
#             language = view.mode.name
#             start_rule = 'main'
            
#         self.parser = Antlr4GenericParser(language, start_rule)
        self.parser = ddic['parser/cls/{}'.format(view.mode.name)]()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.parse)
        self.timer.start(1000)
        self.qthread.start()
        self.editor = view.widget
        self.view = view
        view.ast = self
        self.mode = view.mode
#         self.language = language
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
    
    def get_suggestions(self, parser, text, text_range):
        suggestions = parser.completion_suggestions(text, text_range)
        self.suggestions_created.emit(suggestions, text, text_range)
        return suggestions

    def dispatch_suggestions(self, cmd, suggestions):
        for s in suggestions:
            print(s)
            if s.feature:
                method_name = '_'.join(['complete', s.type, s.feature[0]])
                if hasattr(cmd, method_name):
                    getattr(cmd, method_name)(self.editor, s.node, s.feature, s.parse_node)
                
            method_name = '_'.join(['complete', s.type])
            if hasattr(cmd, method_name):
                getattr(cmd, method_name)(self.editor, s.node, s.parse_node)

    def completion_suggestions(self, cmd):
        self.parse()
        carret_pos = self.editor.pos
        suggestions = self.get_suggestions(self.parser, self.editor.text(), (self.editor.active_range()[0], carret_pos))
        self.dispatch_suggestions(cmd, suggestions)

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
