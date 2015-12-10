from PyQt4.QtCore import QObject
from pyde.ddi import Dependency
import grammars
import os
import subprocess
from PyQt4.Qsci import QsciScintilla
import json
import time
from PyQt4 import QtCore, QtGui
from pyde.plugins.context import Context

os.environ['CLASSPATH'] += ':' + os.path.dirname(grammars.__file__)

class NodeVisitor(object):

    def visit(self, node):
        """Visit a node."""
        method = 'visit_' + node['ctype']
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)
    
    def visit_all_enter(self, node):
        pass
    
    def visit_all_exit(self, node):
        pass

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        children = list(range(len(node['children'])))
        for field in node['_fields']:
            if isinstance(field, int):
                child = node['children'][field]
                self.visit_all_enter(child)
                self.visit(child)
                self.visit_all_exit(child)
                children.remove(field)
                
        for c in children:
            child = node['children'][c]
            self.visit_all_enter(child)
            self.visit(child)
            self.visit_all_exit(child)

class ContextBuilder(NodeVisitor):

    def __init__(self, tokens):
        self.cur_parent = None
        self.tree = None
        self.tokens = tokens

    def visit_all_enter(self, node):
        if self.cur_parent is not None:
            context = Context(name=node['ctype'], parent=self.cur_parent)
        else:
            context = Context(name=node['ctype'])
            
        if self.tree is None:
            self.tree = context
            
        self.cur_parent = context
        context.start_token = self.tokens[node['start']]
        context.stop_token = self.tokens[node['stop']]
        context.start = context.start_token['start']
        context.stop = context.stop_token['stop']
        
    def visit_all_exit(self, node):
        self.cur_parent = self.cur_parent.parent
            

class Parser(QObject):
    
    tree_modified = QtCore.pyqtSignal(list, object) #['QWidget'])
    
    def __init__(self, mode : Dependency('mode/inst/'), context: Dependency('context')):
        super().__init__()
        self.thread = QtCore.QThread()
        self.moveToThread(self.thread)
#        self.context
#        self.thread.started.connect(self.worker.loop)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.parse)
        self.timer.start(1000)
        self.thread.start()
        self.editor = mode.editor
        self.mode = mode
        self.context = context
        self.tree_modified.connect(self.context.update_context)
        self.language = 'python3'
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
        a = self.context.context_at_pos(0)
        if self.dirty:
            text = self.editor.text()
            self.dirty = False
            p = subprocess.Popen(['java', 'pyinterface.Main', 
                                  self.language + '.' + self.language, 
                                  'file_input', '-json', text + '\\n'], stdout=subprocess.PIPE).communicate()[0]
            parse_out = json.loads(p.decode())
            tokens = parse_out['tokens']
            dict_tree = parse_out['tree']
            builder = ContextBuilder(tokens)
            builder.visit(dict_tree)
            self.tree = builder.tree
            self.tree_modified.emit([self.editor.name], self.tree)
            pass
        
        
        