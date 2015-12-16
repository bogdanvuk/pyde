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

class RuleContext(Context):
        
    def get_child_feature(self, child):
        for c in self.children:
            if isinstance(c, list):
                for cl in c:
                    if cl == child:
                        return cl
            else:
                if self.children[c] == child:
                    return c
        return None
    
    @property
    def start(self):
        first_child_name = next(iter(self.children))
        value = self.children[first_child_name]
        if isinstance(value, list):
            if value:
                value = value[0]
            else:
                return 0
        
        return value.start

    @property
    def stop(self):
        last_child_name = next(reversed(self.children))
        value = self.children[last_child_name]
        if isinstance(value, list):
            if value:
                value = value[-1]
            else:
                return 0

        return value.stop

class ContextBuilder(object):

    def __init__(self, tokens, text, active_range):
        self.cur_parent = None
        self.tree = None
        self.tokens = tokens
        self.text = text
        self.cur_tok_index = -1
        self.active_range = active_range

    def visit(self, node):
        if node['type'] == 'tokref':
            index = node['index']
            if index >= 0:
                self.cur_tok_index = index
                self.tokens[index].parent = self.cur_parent
                return self.tokens[index]
            else:
                context = Context(self.cur_parent)
                context.name = node['toktype']
                if self.cur_tok_index >= 0: 
                    context.start = self.tokens[self.cur_tok_index].stop + 1 + self.active_range[0]
                else:
                    context.start = self.active_range[0]
                    
                context.stop = self.tokens[self.cur_tok_index + 1].start + self.active_range[0]
                return context
        else:
#         context = Context(name=node['type'], parent=self.cur_parent)
            context = RuleContext(parent=self.cur_parent)
            context.name = node['type'] 
              
            if self.tree is None:
                self.tree = context
                
            self.cur_parent = context
            
            if 'children' in node:        
                children = list(range(len(node['children'])))
            else:
                children = []
        
#         context.text = self.text[context.start:context.stop+1]

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

def create_token_contexts(token_json, active_range=(0,0)):
    tokens = []
    for t in token_json:
        tc = Context()
        tc.name = t['type']
        tc.start = t['start'] + active_range[0]
        tc.stop = t['stop'] + active_range[0]
        tokens.append(tc)

    return tokens

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
#         self.editor.cursorPositionChanged.connect(self.pos_changed)
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

#     def pos_changed(self, line, col):
#         a = self.context.context_at_pos(self.editor.pos)
    
    def parse(self):
#       
#         text = "2+3\n"
        if self.dirty:
            text = self.editor.active_text()
            self.dirty = False
            p = subprocess.Popen(['java', 'pyinterface.Main', 
                                  self.language + '.' + self.language, 
                                  'file_input', '-json', text + '\\n'], stdout=subprocess.PIPE).communicate()[0]
            parse_out = json.loads(p.decode())
            tokens = create_token_contexts(parse_out['tokens'], self.editor.active_range())
            dict_tree = parse_out['tree']
#             print(json.dumps(dict_tree, sort_keys=True, indent=4, separators=(',', ': ')))
            builder = ContextBuilder(tokens, text, self.editor.active_range())
            builder.visit(dict_tree)
            self.tree = builder.tree
            self.tree_modified.emit([self.editor.name, 'ast'], self.tree)
#             a = self.context.context_at_pos(0)
#             pass
        
