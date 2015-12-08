from PyQt4.QtCore import QObject
from pyde.ddi import Dependency
import grammars
import os

os.environ['CLASSPATH'] += ':' + os.path.dirname(grammars.__file__)

class Parser(QObject):
     
    def __init__(self, editor : Dependency('editor.'), language):
        super().__init__()
        self.editor = editor
        self.language = language
#         self.editor.SCN_MODIFIED.connect(self.text_modified)
        self.incremental_state = 'connector'
        self.tree = None
        
     
    def leaf_node_at(self, pos):
        if self.tree is not None:
            return self.context_at_pos(self, pos)[-1]
        else:
            return None 
     
    def context_at_pos(self, lineno, col):
        if self.tree is not None:
            return context_at_pos(self.tree, lineno, col)
        else:
            return None 
 
    def text_modified(self, pos, mtype, text, length, linesAdded, line, foldNow,
                   foldPrev, token, annotationLinesAdded):
         
        if ((mtype & QsciScintilla.SC_MOD_INSERTTEXT) != 0) or \
            ((mtype & QsciScintilla.SC_MOD_DELETETEXT) != 0):
            self.parse(self.editor.active_text())
 
    def parse(self, text):
#         os.chdir('/home/bvukobratovic/projects/pyde/grammars/python3')
        print(text)
        p = subprocess.Popen(['java', 'python3.Main', 'python3.Python3', 'file_input', '-json', text + '\\n'], stdout=subprocess.PIPE).communicate()[0]
        self.tree = json.loads(p.decode())
