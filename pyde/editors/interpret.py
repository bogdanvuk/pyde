#-------------------------------------------------------------------------
# qsci_simple_pythoneditor.pyw
#
# QScintilla sample with PyQt
#
# Eli Bendersky (eliben@gmail.com)
# This code is in the public domain
#-------------------------------------------------------------------------
import sys

from io import StringIO
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import QsciScintilla, QsciLexerPython
import pyde
from pyde.application import app
from PyQt4 import QtGui, Qsci
from pyde.pyde_widget import PydeWidget
from pyde.editor import PydeEditor
from inspect import signature
import ast
import pyde.pyposast
from pyde.plugins.templating import Template

def patch_ast(tree):
    tree.is_leaf = True
    tree.parent = None
    
    if not hasattr(tree, 'uid'):
        tree.nontext = True
    else:
        tree.nontext = False
        for _, value in ast.iter_fields(tree):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        patch_ast(item)
                        item.parent = tree
                        if not item.nontext:
                            tree.is_leaf = False
            elif isinstance(value, ast.AST):
                patch_ast(value)
                value.parent = tree
                if not value.nontext:
                    tree.is_leaf = False

def node_iter(node):
    for _, value in ast.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    yield item
        elif isinstance(value, ast.AST):
            yield value
            
def tree_iter(tree):
    for node in node_iter(tree):
        yield node
        yield from tree_iter(node)

def higher_pos(pos1, pos2):
    if pos1[0] > pos2[0]:
        return 1
    elif pos1[0] < pos2[0]:
        return 2
    else:
        if pos1[1] > pos2[1]:
            return 1
        elif pos1[1] < pos2[1]:
            return 2
        else:
            return 0
            
def context_at_pos(tree, lineno, col):
    context = []
    for node in tree_iter(tree):
        if not node.nontext:
            if higher_pos((lineno, col), (node.first_line, node.first_col)) in [0, 1] and \
                higher_pos((lineno, col), (node.last_line, node.last_col)) in [0, 2]:
                context.append(node)
#                 while (node.parent is not None):
#                     context.insert(0, node.parent)
#                     node = node.parent
#                 
#                 return context
                
    return context

class PyInterpretParser(QObject):
    
    class PositionUpdater(object):
        def __init__(self, tree, text):
            self.tree = tree
            self.cur_end = len(text)
            self.lines = text.split('\n')
            self.col_cur_end = []
            for line in self.lines:
                self.col_cur_end.append(len(line))

        def patch(self):
            self._patch(self.tree)

        def _patch(self, node):
            
            if hasattr(node, 'lineno'):
                node.lineno -= 1
                line_offset = sum(self.col_cur_end[:node.lineno]) + node.lineno # compensate for end of line
                node.col_pos = (node.col_offset, self.col_cur_end[node.lineno])
                node.pos = (line_offset + node.col_pos[0], line_offset + node.col_pos[1])
                node.text = self.lines[node.lineno][node.col_pos[0]:node.col_pos[1]]
                
                try:
                    print(type(node).__name__, ':', node.text, ':', (node.lineno, node.col_offset), ':', node.col_pos, ':', node.pos, ':', ast.dump(node))
                except AttributeError:
                    print(type(node).__name__)
            
            
            if hasattr(node, 'lineno') or isinstance(node, ast.mod):      
                node.is_leaf = True
            
                for child in reversed(list(node_iter(node))):
                    if not self._patch(child):
                        node.is_leaf = False

                if node.is_leaf:
                    self.col_cur_end[node.lineno] = node.col_offset - 1
                    
                return False
            else:
                return True
            
    def __init__(self, editor):
        super().__init__()
        self.editor = editor
        self.editor.SCN_MODIFIED.connect(self.text_modified)
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
#             text = text.decode()
#             has_nonalnum = any(not (c.isalnum() or c == '_') for c in text)
#             has_alnum = any(c.isalnum() or c == '_' for c in text)
#                 
#             if self.incremental_state == 'connector':
#                 if has_alnum:
#                     self.parse(self.editor.active_text())
#                     self.incremental_state = 'literal'
#             elif self.incremental_state == 'literal':        
#                 if has_nonalnum:
#                     self.parse(self.editor.active_text())
#                     self.incremental_state = 'connector'

    def parse(self, text):
        self.tree = None
        try:
#             self.tree = ast.parse(text, mode='single')
            self.tree = pyde.pyposast.parse(text)
            patch_ast(self.tree)
            self.text = text
#             self.PositionUpdater(self.tree, text).patch()
            self.incremental_state = 'connector'
        except SyntaxError as e:
            print(e)
            try:
                if e.text[e.offset-2] == '.':
                    self.tree = pyde.pyposast.parse(text[])
                    patch_ast(self.tree)
                    self.text = text
            except SyntaxError as e:
                pass
            

            

class PyInterpretContentAssist(QObject):
    def __init__(self):
        super().__init__()
        app.globals.content_assist.complete.connect(self.complete)
    
    def complete(self, acceptor):
        editor = app.active_widget()
        context = editor.cur_context()
        
#         for i,c in enumerate(reversed(context)):
#             if not isinstance(c, (ast.Attribute, ast.Name, ast.Call, ast.Subscript)):
#                 obj = eval(compile(ast.Expression(context[i+1]), '(none)', 'eval'))
        if context:
            if isinstance(context[-1], ast.Expression):
                for name, obj in app.globals.items():
                    try:
                        sig = signature(obj)
                    except:
                        sig = ''
                        
                    acceptor[name] = name + str(sig)
            elif isinstance(context[-1], ast.Attribute):
                try:
                    obj = eval(compile(ast.Expression(context[-1].value), '(none)', 'eval'))
                    for d in dir(obj):
                        acceptor[d] = d        
                except:
                    pass
    
            acceptor['proba_templ'] = Template(text='proba {p0} i {p1} bla')
        
        
class PyInerpretEditor(PydeEditor):
    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None):
        super(PyInerpretEditor, self).__init__(parent)

        # Set the default font
        font = QFont()
        font.setFamily('DejaVu Sans Mono')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.parser = PyInterpretParser(self)
        self.ca = PyInterpretContentAssist()
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
        
        self.setMinimumSize(fontmetrics.width("00000"), fontmetrics.height()+4)
        
#         self.globals = {}
#         self.globals['app'] = pyde.application.app
#         from pyde import actions
#         
#         for a in dir(actions):
#             if not a.startswith('__'):
#                 obj = getattr(actions, a)
#                 if callable(obj):
#                     self.globals[a] = obj
         
        self.locals = {}
        self.prompt_begin = 0
        
        lexer = QsciLexerPython(self)
        
#         self.c = QtGui.QCompleter(['"helaaa"', 'helabb', 'helccc', 'world'])
#         self.c.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
#         self.c.setWidget(self)
# 
        self.setAutoCompletionThreshold(0)
#         self.setAutoCompletionShowSingle(True)
        self.setAutoCompletionSource(Qsci.QsciScintilla.AcsAPIs)
        
        lexer.setDefaultFont(font)
        
        self.setLexer(lexer)
        self.content_assist_list = Qsci.QsciAPIs(self.lexer())
        self.autoCompleteFromAll()
         
#         self.prepare_assist_globals()
        
#         self.SCN_AUTOCSELECTION.connect(self.autoc_end)

    def cur_context(self):
        lineno, col = self.getCursorPosition()
        active_range_start_line, _ = self.lineIndexFromPosition(self.prompt_begin)
        return self.parser.context_at_pos(lineno - active_range_start_line + 1, col - 1)

    def active_range(self):
        return (self.prompt_begin, self.length())

    def active_text(self):
        start, stop = self.active_range()
        return self.text()[start:stop]

    def evaluate(self):
        if self.SendScintilla(QsciScintilla.SCI_AUTOCACTIVE):
            self.SendScintilla(QsciScintilla.SCI_AUTOCCOMPLETE)
        else:
            cmd = self.active_text()
            
#             buffer = StringIO()
#             sys.stdout = buffer
            
            self.pos = self.length()
            
            try:
                 
                ret = eval(cmd, app.globals, self.locals)
                if ret is not None:
                    ret_str = '\n' + str(ret) + '\n'
                else:
                    ret_str = '\n'
                     
#                 stdout_text = buffer.getvalue()
#                 if stdout_text:
#                     ret_str += stdout_text
                 
                self.insert(ret_str)
            except SyntaxError:
                exec(cmd, app.globals, self.locals)
                self.insert('\n')
            except:
                self.insert('\n{0}: {1}\n'.format(sys.exc_info()[0].__name__, sys.exc_info()[1]))
            
#             sys.stdout = sys.__stdout__
#             self.setCursorPosition(self.lines(), 0)
            self.pos = self.length()
            self.prompt_begin = self.length()

    def autoc_end(self):
        print("ENDED!")

    def prepare_assist_globals(self):
        for name, obj in app.globals.items():
            try:
                sig = signature(obj)
            except:
                sig = ''
                
            self.content_assist_list.add(name + str(sig))

        self.content_assist_list.add('backward/bla/abla')
        self.content_assist_list.add('backward_chab')
        self.content_assist_list.add('backward_chbb')
            
        self.content_assist_list.prepare()
    
    def content_assist(self):
#        self.SendScintilla(QsciScintilla.SCI_AUTOCSHOW, 4, '"helaaa" helabb helccc world'.encode())
#         self.c.complete()
        self.prepare_assist_globals()
        self.autoCompleteFromAll()
