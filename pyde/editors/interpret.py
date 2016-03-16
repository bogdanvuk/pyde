#-------------------------------------------------------------------------
# qsci_simple_pythoneditor.pyw
#
# QScintilla sample with PyQt
#
# Eli Bendersky (eliben@gmail.com)
# This code is in the public domain
#-------------------------------------------------------------------------
import sys

from PyQt4.Qsci import QsciScintilla, QsciLexerPython
from pyde.editor import PydeEditor
from PyQt4.QtGui import QFont, QFontMetrics, QColor
from pyde.ddi import ddic, Amendment

# class ContextVisitor(NodeVisitor):
# 
#     class FoundLeafException(Exception):
#         pass
#     
#     def context_at(self, node, pos, tokens):
#         self.context = []
#         self.pos = pos
#         self.tokens = tokens
#         try:
#             self.visit(node)
#         except self.FoundLeafException:
#             pass
#     
#     def visit_all_enter(self, node):
#         """Visit a node."""
#         self.context.append(node)
#   
#         if not node['children']:
#             tok_start = self.tokens[node['start']]['start']
#             tok_stop = self.tokens[node['stop']]['stop']
#             if self.pos >= tok_start and self.pos <= tok_stop:
#                 raise self.FoundLeafException
#     
#     def visit_all_exit(self, node):
#         self.context.pop()
        

# class PyInterpretParser(QObject):
#     
#     def __init__(self, editor):
#         super().__init__()
#         self.editor = editor
# #         self.editor.SCN_MODIFIED.connect(self.text_modified)
#         self.incremental_state = 'connector'
#         self.tree = None
#         os.environ['CLASSPATH'] += ':/home/bvukobratovic/projects/pyde/grammars'
#     
#     def leaf_node_at(self, pos):
#         if self.tree is not None:
#             return self.context_at_pos(self, pos)[-1]
#         else:
#             return None 
#     
#     def context_at_pos(self, lineno, col):
#         if self.tree is not None:
#             return context_at_pos(self.tree, lineno, col)
#         else:
#             return None 
# 
#     def text_modified(self, pos, mtype, text, length, linesAdded, line, foldNow,
#                    foldPrev, token, annotationLinesAdded):
#         
#         if ((mtype & QsciScintilla.SC_MOD_INSERTTEXT) != 0) or \
#             ((mtype & QsciScintilla.SC_MOD_DELETETEXT) != 0):
#             self.parse(self.editor.active_text())
# 
#     def parse(self, text):
# #         os.chdir('/home/bvukobratovic/projects/pyde/grammars/python3')
#         print(text)
#         p = subprocess.Popen(['java', 'python3.Main', 'python3.Python3', 'file_input', '-json', text + '\\n'], stdout=subprocess.PIPE).communicate()[0]
#         self.tree = json.loads(p.decode())
# 
# class PyInterpretContentAssist(QObject):
#     def __init__(self):
#         super().__init__()
#         app.globals.content_assist.complete.connect(self.complete)
#     
#     def complete(self, acceptor):
#         editor = app.active_widget()
#         context = editor.cur_context()
#         
# #         for i,c in enumerate(reversed(context)):
# #             if not isinstance(c, (ast.Attribute, ast.Name, ast.Call, ast.Subscript)):
# #                 obj = eval(compile(ast.Expression(context[i+1]), '(none)', 'eval'))
#         if (not context) or (context[-1]['ctype'] == 'file_input') or (context[-1]['ctype'] == 'atom'):
# 
#             if context and context[-1]['ctype'] == 'atom':
#                 tokens = editor.parser.tree['tokens']
#                 app.globals.content_assist.set_start(tokens[context[-1]['start']]['start'])
#             
#             for name, obj in app.globals.items():
# #                 try:
# #                     sig = signature(obj)
# #                 except:
# #                     sig = ''
#                 if callable(obj):
#                     acceptor[name] = TemplFunc(obj) #name + str(sig)
#                 else:
#                     acceptor[name] = name
#                 
#         elif context[-1]['ctype'] == 'trailer':
#             try:
#                 tokens = editor.parser.tree['tokens']
#                 tok_start = context[-2]['start']
#                 tok_stop = context[-2]['stop']
#                 
#                 if tokens[tok_stop]['type'] == "NAME":
#                     app.globals.content_assist.set_start(tokens[tok_stop]['start'])
#                     tok_stop -= 2
#                 elif tokens[tok_stop]['type'] == "DOT":
#                     tok_stop -= 1
#                 
#                 tok_start = tokens[tok_start]['start'] + editor.prompt_begin    
#                 tok_stop = tokens[tok_stop]['stop'] + editor.prompt_begin
#                 text = editor.text()[tok_start:tok_stop+1]
#                 
#                 obj = eval(text, app.globals, editor.locals)
#                 for d in dir(obj):
#                     acceptor[d] = d        
#             except:
#                 pass
# 
#         acceptor['proba_templ'] = Template(text='proba {p0} i {p1} bla')
#         
        
class PyInerpretEditor(PydeEditor):
    ARROW_MARKER_NUM = 8

    def __init__(self, view: Amendment('view/', lambda v: hasattr(v, 'mode') and (v.mode.name == 'ipython') and (v.widget is None))):
        super().__init__(view)

        # Set the default font
        font = QFont()
        font.setFamily('DejaVu Sans Mono')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
#        self.parser = Parser(self, 'python3')
#         self.ca = PyInterpretContentAssist()
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
        
        self.globals = {}
        self.globals['ddic'] = ddic
        for a in ddic['actions']:
            self.globals[a] = ddic['actions'][a]
            
        self.locals = {}
        self.markerDefine(QsciScintilla.RightArrow,
            self.ARROW_MARKER_NUM)
#         self.setMarkerBackgroundColor(QColor("#ee1111"),
#             self.ARROW_MARKER_NUM)

        self.prompt_begin = 0

        self.focus_view = None
        
    @property
    def prompt_begin(self):
        return self._prompt_begin
    
    @prompt_begin.setter
    def prompt_begin(self, value):
        if hasattr(self, '_prompt_begin'):
            self.markerDelete(self.lineIndexFromPosition(self._prompt_begin)[0], self.ARROW_MARKER_NUM)
            
        self._prompt_begin = value
        self.markerAdd(self.lineIndexFromPosition(self._prompt_begin)[0], self.ARROW_MARKER_NUM)

#     def active_text(self):
# #         start, stop = self.active_range()
#         return super().text()[self.prompt_begin:self.length()]
    
#     def active_range(self):
#         return (self.prompt_begin, self.length())

    def cycle_frame(self, old):
        return False

    def cmd_range(self):
        return (self.prompt_begin, self.length())
    
    def cmd_text(self):
        return self.text()[self.prompt_begin:self.length()]

    def execute_view_action(self, view):
        self.focus_view = view
        self.view.set_focus()
#         ddic['actions/switch_view'](self.view, self.view.last_location)

    def cancel(self):
        self.SendScintilla(QsciScintilla.SCI_DELETERANGE, self.prompt_begin, self.length() - self.prompt_begin)
        if self.focus_view is not None:
            ddic['actions/switch_view'](self.focus_view, self.focus_view.widget.loc)

    def evaluate(self):
        if self.focus_view is not None:
            ddic['actions/switch_view'](self.focus_view, self.focus_view.widget.loc)
            self.focus_view = None

        cmd = self.cmd_text()
        
        self.pos = self.length()
        
        try:
             
            ret = eval(cmd, self.globals, self.locals)
            if ret is not None:
                ret_str = '\n' + str(ret) + '\n'
            else:
                ret_str = '\n'
                 
#                 stdout_text = buffer.getvalue()
#                 if stdout_text:
#                     ret_str += stdout_text
             
            self.insert(ret_str)
        except SyntaxError:
            exec(cmd, self.globals, self.locals)
            self.insert('\n')
        except:
            self.insert('\n{0}: {1}\n'.format(sys.exc_info()[0].__name__, sys.exc_info()[1]))
        
#             sys.stdout = sys.__stdout__
#             self.setCursorPosition(self.lines(), 0)
        self.pos = self.length()
        self.prompt_begin = self.length()
