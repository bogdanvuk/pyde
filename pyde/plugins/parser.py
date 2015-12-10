from PyQt4.QtCore import QObject
from pyde.ddi import Dependency
import grammars
import os
import subprocess
from PyQt4.Qsci import QsciScintilla
import json
import time
from PyQt4 import QtCore
from pyde.plugins.context import Context

os.environ['CLASSPATH'] += ':' + os.path.dirname(grammars.__file__)

class Parser(QObject):
    
    def __init__(self, editor : Dependency('editor.'), language):
        super().__init__()
        self.thread = QtCore.QThread()
        self.moveToThread(self.thread)
#        self.context
#        self.thread.started.connect(self.worker.loop)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.parse)
        self.timer.start(1000)
        self.thread.start()
        self.editor = editor
        self.language = language
        self.editor.SCN_MODIFIED.connect(self.text_modified)
        self.dirty = False
    
    def leaf_node_at(self, pos):
        if self.tree is not None:
            return self.context_at_pos(self, pos)[-1]
        else:
            return None 
     
#     def context_at_pos(self, lineno, col):
#         if self.tree is not None:
#             return context_at_pos(self.tree, lineno, col)
#         else:
#             return None 
 
    def text_modified(self, pos, mtype, text, length, linesAdded, line, foldNow,
                   foldPrev, token, annotationLinesAdded):
          
        if ((mtype & QsciScintilla.SC_MOD_INSERTTEXT) != 0) or \
            ((mtype & QsciScintilla.SC_MOD_DELETETEXT) != 0):
            self.dirty = True
    
    def hook(self, d):
        c = Context()
        for k,v in d.items():
            c[k] = v
            if isinstance(v, Context):
                v.name = k
                v.parent = c

        return c
    
    def parse(self):
        if self.dirty:
            text = self.editor.text()
            self.dirty = False
            p = subprocess.Popen(['java', 'pyinterface.Main', 
                                  self.language + '.' + self.language, 
                                  'file_input', '-json', text + '\\n'], stdout=subprocess.PIPE).communicate()[0]
            self.tree = json.loads(p.decode(), object_hook=self.hook)
            pass