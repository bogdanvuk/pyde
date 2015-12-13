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

# class NodeVisitor(object):
# 
#     def visit(self, node):
#         """Visit a node."""
#         method = 'visit_' + node['ctype']
#         visitor = getattr(self, method, self.generic_visit)
#         self.visit_all_enter(node)
#         ret = visitor(node)
#         self.visit_all_exit(node)
#         return ret
#     
#     def visit_all_enter(self, node):
#         pass
#     
#     def visit_all_exit(self, node):
#         pass
# 
#     def generic_visit(self, node):
#         """Called if no explicit visitor function exists for a node."""
#         children = list(range(len(node['children'])))
#         for field in node['_fields']:
#             if isinstance(field, int):
#                 child = node['children'][field]
#                 self.visit(child)
#                 children.remove(field)
#             elif isinstance(field, list):
#                 
#                 
#         for c in children:
#             child = node['children'][c]
#             self.visit(child)

class ContextBuilder(object):

    def __init__(self, tokens, text):
        self.cur_parent = None
        self.tree = None
        self.tokens = tokens
        self.text = text
        self.cur_tok_index = -1

    def visit(self, node):
        context = Context(name=node['type'], parent=self.cur_parent)
          
        if self.tree is None:
            self.tree = context
            
        self.cur_parent = context
        
        if 'children' in node:        
            children = list(range(len(node['children'])))
        else:
            children = []
        
        
        if 'index' in node:
            if node['index'] >= 0:
                self.cur_tok_index = node['index']
                context.start = node['start']
                context.stop = node['stop']
            else:
                if self.cur_tok_index >= 0: 
                    context.start = self.tokens[self.cur_tok_index]['stop'] + 1
                else:
                    context.start = 0
                    
                context.stop = self.tokens[self.cur_tok_index + 1]['start']

        else:
            context.start_token = self.tokens[node['start']]
            context.stop_token = self.tokens[node['stop']]
            context.start = context.start_token['start']
            context.stop = context.stop_token['stop']

        context.text = self.text[context.start:context.stop+1]

        if children:
            for field_name in node['_fields']:
                if field_name == 'value':
                    pass
                field = node[field_name]
                if isinstance(field, int):
                    child = node['children'][field]
                    context[field_name] = self.visit(child)
                    children.remove(field)
                elif isinstance(field, list):
                    field_val = []
                    for elem in field:
                        child = node['children'][elem]
                        field_val.append(self.visit(child))
                        
                    context[field_name] = field_val
    
            free_children = []                
            for c in children:
                child = node['children'][c]
                free_children.append(self.visit(child))
        
        self.cur_parent = context.parent
            
        if context.parent:
            if len(children) == 1:
                if not node['_fields']:
                    free_children[0].parent = self.cur_parent
                    return free_children[0]
            elif len(children) > 1:
                if not node['_fields']:
                    for n in free_children:
                        context[n.name] = n

        return context

class Parser(QObject):
    
    tree_modified = QtCore.pyqtSignal(list, object) #['QWidget'])
    
    def __init__(self, mode : Dependency('mode/inst/'), context: Dependency('context'), language):
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
        self.language = language
        self.editor.SCN_MODIFIED.connect(self.text_modified)
        self.editor.cursorPositionChanged.connect(self.pos_changed)
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

    def pos_changed(self, line, col):
        a = self.context.context_at_pos(self.editor.pos)
    
    def parse(self):
#       
#         text = "2+3\n"
        if self.dirty:
            text = self.editor.text()
            self.dirty = False
            p = subprocess.Popen(['java', 'pyinterface.Main', 
                                  self.language + '.' + self.language, 
                                  'file_input', '-json', text + '\\n'], stdout=subprocess.PIPE).communicate()[0]
            parse_out = json.loads(p.decode())
            tokens = parse_out['tokens']
            dict_tree = parse_out['tree']
#             print(json.dumps(dict_tree, sort_keys=True, indent=4, separators=(',', ': ')))
            builder = ContextBuilder(tokens, text)
            builder.visit(dict_tree)
            self.tree = builder.tree
            self.tree_modified.emit([self.editor.name], self.tree)
#             a = self.context.context_at_pos(0)
#             pass
        
        
        