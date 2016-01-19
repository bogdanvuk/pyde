from PyQt4.QtCore import QObject
from pyde.ddi import Dependency
import grammars
import os
import subprocess
from PyQt4.Qsci import QsciScintilla
import json
import time
from PyQt4 import QtCore, QtGui
from pyde.plugins.context import Context, ContextSlice

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

class SequenceMatchError(Exception):
    pass

class NodeVisitor(object):

    def visit(self, node):
        """Visit a node."""
        if node.type:
            method = 'visit_' + node.type
            visitor = getattr(self, method, self.generic_visit)
        else:
            visitor = self.generic_visit

        self.visit_all_enter(node)
        ret = visitor(node)
        self.visit_all_exit(node)
        return ret
    
    def visit_all_enter(self, node):
        pass
    
    def visit_all_exit(self, node):
        pass

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        for c in node.features:
            child = node.features[c]
            if isinstance(child, list):
                for elem in child:
                    self.visit(elem)
            else:
                self.visit(child)

class ContextVisitor(NodeVisitor):

    class FoundLeafException(Exception):
        pass

    def __init__(self, root):
        self.root = root
 
    def context_at(self, pos):
        self.context = None
        self.pos = pos
        try:
            self.visit(self.root)
        except self.FoundLeafException:
            return self.context
    
    def visit(self, node):

        if node.slice.contains(self.pos):
            if not node.features:
                self.context = node
                raise self.FoundLeafException
            else:
                for c in node.features:
                    child = node.features[c]
                    if isinstance(child, list):
                        for i,elem in enumerate(child):
                            self.visit(elem)
                    else:
                        self.visit(child)

class ParserRuleContext(list):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        
    @property
    def slice(self):
        i_start = None
        for i,c in enumerate(self):
            start_slice = c.slice
            if start_slice is not None:
                i_start = i
                break
        else:
            return None

        for i, c in reversed(list(enumerate(self))):
            if i == i_start:
                end_slice = start_slice
                break
            else:
                end_slice = c.slice
                if end_slice is not None:
                    break
        else:
            return None
        
        return ContextSlice(start_slice.start, end_slice.stop)
        
class RuleContext(Context):
    type = 'parser_rule'

    @property
    def slice(self):
        return self.rule.slice

class ParseTreeBuilder:
    def __init__(self, tokens, active_range):
        self.cur_parent = None
        self.tree = None
        self.tokens = tokens
        self.cur_tok_index = -1
        self.active_range = active_range

    def visit(self, node):
        if node['type'] == 'tokref':
            return self.visit_token(node)
        else:
            return self.visit_rule(node)

    def visit_token(self, node):
        index = node['index']
        if index >= 0:
            self.cur_tok_index = index
            self.tokens[index].parent = self.cur_parent
            return self.tokens[index]
        else:
            t = node['toktype']
            if self.cur_tok_index >= 0: 
                start = self.tokens[self.cur_tok_index].slice.stop # + self.active_range[0]
            else:
                start = self.active_range[0]
                
            stop = self.tokens[self.cur_tok_index + 1].slice.start + 1 # + self.active_range[0]
            s = ContextSlice(start, stop)
            return Token(t,s)

    def visit_rule(self, node):
        #         context = Context(name=node['type'], parent=self.cur_parent)
        rule = ParserRuleContext(self.cur_parent)
        rule.type = node['type']
#         rule.editor = self.editor
        
        if self.tree is None:
            self.tree = rule
            
        self.cur_parent = rule
        
        if 'children' in node:        
            children = list(range(len(node['children'])))
        else:
            children = []
        
        for c in children:
            child = node['children'][c]
            rule.append(self.visit(child))
        
        rule.fields = {}
        for field_name in node['_fields']:
            rule.fields[field_name] = node[field_name] 

        self.cur_parent = rule.parent
            
        return rule

class ContextBuilder(object):

    def __init__(self, parse_tree):
        self.tree = None
        self.cur_parent = None
        self.parse_tree = parse_tree

    def visit(self, node):
        if isinstance(node, Token):
            return self.visit_token(node)
        else:
            return self.visit_rule(node)

    def visit_token(self, token):
        context = RuleContext(self.cur_parent)
        context.type = token.type
        context.rule = token
        return context

    def visit_rule(self, node):
        #         context = Context(name=node['type'], parent=self.cur_parent)
        context = RuleContext(self.cur_parent)
        context.type = node.type
          
        if self.tree is None:
            self.tree = context

        self.cur_parent = context
        
        if node.fields:
            for field_name in node.fields:
                field = node.fields[field_name]
                if isinstance(field, int):
                    child = node[field]
                    context[field_name] = self.visit(child)
                elif isinstance(field, list):
                    field_val = []
                    for elem in field:
                        child = node[elem]
                        field_val.append(self.visit(child))
                        
                    context[field_name] = field_val
    
        self.cur_parent = context.parent
        context.rule = node
        
        if context.parent:
            if len(node) == 1:
                if not node.fields:
                    child = node[0]
                    return self.visit(child)
#                     free_children[0].parent = self.cur_parent
#                     return free_children[0]
#             elif len(children) > 1:
#                 if not node['_fields']:
#                     for n in free_children:
#                         context[n.name] = n
        
        context.rule.context = context
        return context

class Token:
    
    def __init__(self, t, s):
        self.type = t
        self.slice = s
    
    def __repr__(self):
        return "{}: {}".format(self.type, self.slice.eval())
      
    def __str__(self):
        return self.slice.eval()

def create_tokens(token_json, active_range):
#     active_range = editor.active_range()
    tokens = []
    for tj in token_json:
        t = tj['type']
        s = ContextSlice(tj['start'] + active_range[0], tj['stop'] + active_range[0] + 1)
        tokens.append(Token(t,s))

    return tokens

class Antlr4GenericParser:
    
    def __init__(self, language, start_rule):
        self.language = language
        self.start_rule = start_rule
    
    def parse(self, text, text_range):
        text = text[text_range[0]: text_range[1]]
        self.dirty = False
        p = subprocess.Popen(['java', 'pyinterface.Main', 
                              self.language + '.' + self.language, 
                              self.start_rule, '-json', text + '\n'], stdout=subprocess.PIPE).communicate()[0]
        parse_out = json.loads(p.decode())
        tokens = create_tokens(parse_out['tokens'], text_range)
        dict_tree = parse_out['tree']
#             print(json.dumps(dict_tree, sort_keys=True, indent=4, separators=(',', ': ')))
        parse_builder = ParseTreeBuilder(tokens, text_range)
        parse_builder.visit(dict_tree)
        self.parse_tree = parse_builder.tree
        builder = ContextBuilder(tokens)
        builder.visit(self.parse_tree)
        self.tree = builder.tree
        return self.tree

class EditorAstManager(QObject):
    
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
        cmd(self.editor, self.ast)
        print('end ast.read_only')

    def parse(self):
        if self.dirty:
            self.dirty = False
            self.ast = self.parser.parse(self.editor.text(), self.editor.active_range())
            self.tree_modified.emit(self.ast)

class IPythonEditorAstManager(EditorAstManager):

    def parse(self):
        if self.dirty:
            self.dirty = False
            self.ast = self.parser.parse(self.editor.text(), self.editor.cmd_range())
            self.tree_modified.emit(self.ast)
        
def Antlr4ParserFactory(lang_name, start_rule):
    class Antlr4Parser(Antlr4GenericParser):
        def __init__(self):
            super().__init__(language=lang_name, start_rule=start_rule)
        
    return Antlr4Parser