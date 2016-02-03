from PyQt4.QtCore import QObject
from pyde.ddi import Dependency, ddic
#from pyde.plugins.parser import ContextVisitor, NodeVisitor
from pyde.plugins.templating import TemplFunc
from inspect import getfullargspec
import os
from PyQt4 import QtCore

def get_ctx_text(ctx, editor):
    return editor.text()[ctx.slice.start:ctx.slice.stop]
    
def get_obj_for_ctx(ctx, editor):
    return eval(ctx.parse_node.text, editor.globals, editor.locals)

class PathVisitor(object):
 
    def visit(self, node):
        """Visit a node."""
        if node.type:
            method = 'visit_' + node.type
            visitor = getattr(self, method, self.generic_visit)
        else:
            visitor = self.generic_visit

        if node.parent is not None:
            cur_feature = node.get_feature_in_parent()[0]
            method = 'visit_' + node.parent.type + '_' + cur_feature
            if hasattr(self, method):
                getattr(self, method)(node)

        ret = visitor(node)
                 
        return ret
     
    def generic_visit(self, node):
        if node.parent is not None:
            self.visit(node.parent)
        
class ContentAssistVisitor(PathVisitor):
    def __init__(self, editor, acceptor):
        self.editor = editor
        self.acceptor = acceptor
        
    def visit_expr_attr(self, node):
        calee_ctx = node.parent['calee']
        calee_text = self.editor.text()[calee_ctx.slice.start:calee_ctx.slice.stop]
        obj = eval(calee_text, self.editor.globals, self.editor.locals)
        for d in dir(obj):
            self.acceptor[d] = d

    def visit_rel_path_path(self):
        pass

class CompleteCommand:
    
    def accept_global(self, editor):
        for g in editor.globals:
            if callable(editor.globals[g]):
                self.acceptor[g] = TemplFunc(editor.globals[g])
            else:
                self.acceptor[g] = g
            
            for l in editor.locals:
                self.acceptor[l] = l

    
    def complete_main_path(self, editor, node):
        pass
    
    def complete_expr(self, editor, node):
        self.accept_global(editor)
    
    def complete_expr_attr(self, editor, node):
        pass
    #     def __call__(self, editor, ast):
#         cv = ContextVisitor(ast)
#         cur_ctx = cv.context_at(editor.pos-1)
#         
#         if cur_ctx.type in cur_ctx.keywords:
#             cur_ctx = cv.context_at(editor.pos)
#             
#             if cur_ctx.type in cur_ctx.keywords:
#                 return
# 
#         if cur_ctx is None:
#             self.accept_global(editor)
#         else:
#             v = ContentAssistVisitor(editor, self.acceptor)
#             v.visit(cur_ctx)
#             print('else')
#             cur_parent = cur_ctx.parent
#             cur_feature = cur_ctx.get_feature_in_parent()
#             
#             rel_path_ctx = get_ctx_parent_of_type(cur_ctx, 'rel_path')
#             if rel_path_ctx is not None:
#                 
#                 part_ctx = get_ctx_parent_of_type(cur_ctx, 'part')
#                 
#                 part_feature = part_ctx.get_feature_in_parent()
#                 last_segment = part_feature[1]
#                 if cur_ctx.type == 'PATHSEP':
#                     last_segment += 1
#                 
#                 path = []
#                 for i in range(last_segment):
#                     path.append(get_ctx_text(rel_path_ctx['part'][i], editor))
#                 
#                 path = '/' + ''.join(path)
#                 print(path)
#                 for f in os.listdir(path):
#                     if os.path.isdir(os.path.join(path,f)):
#                         f = f + '/'
#                         
#                     self.acceptor[f] = f
#             elif cur_ctx.type == 'NAME' and cur_parent.type == 'expr' and cur_feature[0] == 'value':
#                 self.accept_global(editor)
#             elif cur_ctx.type == 'argument':
#                 expr = get_ctx_parent_of_type(cur_ctx, 'expr')
#                 obj = get_obj_for_ctx(expr['calee'], editor)
#                 pass
#             elif cur_feature[0] == 'attr':
#                 print('attr')
#                 calee_ctx = cur_parent['calee']
#                 calee_text = editor.text()[calee_ctx.slice.start:calee_ctx.slice.stop]
#                 obj = eval(calee_text, editor.globals, editor.locals)
#                 for d in dir(obj):
#                     self.acceptor[d] = d
#             else:
#                 print('else')
#                 pass

class PyInterpretContentAssist(QObject):
    
    read_ast = QtCore.pyqtSignal(object)
    complete_sig = QtCore.pyqtSignal(object)
    
    def __init__(self, 
                 editor : Dependency('view/', lambda e: isinstance(e.widget, ddic['cls/ipython'])),
                 ca : Dependency('content_assist'),
                 win : Dependency('win')):
        super().__init__()
        self.ca = ca
        self.win = win
        self.editor = editor
        self.complete_cmd = CompleteCommand()
        if self.ca.thread() != self.thread():
            connection_type=QtCore.Qt.BlockingQueuedConnection
        else:
            connection_type=QtCore.Qt.AutoConnection

        self.ca.complete.connect(self.complete, type=connection_type)
     
    def complete(self, acceptor):
        view = self.win.active_view()
        editor = view.widget
        self.complete_cmd.acceptor = acceptor
        
#         self.read_ast.connect(editor.ast.read_only, type=QtCore.Qt.BlockingQueuedConnection)
#         self.read_ast.emit(self.complete_cmd)
#         self.read_ast.disconnect()
        self.complete_sig.connect(editor.ast.completion_suggestions, type=QtCore.Qt.BlockingQueuedConnection)
        self.complete_sig.emit(self.complete_cmd)
        self.complete_sig.disconnect()

#         editor.ast.read_only(self.complete_cmd)
#         if hasattr(editor, 'ast'):
#             editor.ast.read_ast()
#             cv = ContextVisitor(editor.ast)
#             cur_ctx = cv.context_at(editor.anchor)
#         else:
#             cur_ctx = None
# 
#         if cur_ctx is None:
#             print('cur_ctx = view')
#             for g in editor.globals:
#                 if callable(editor.globals[g]):
#                     acceptor[g] = TemplFunc(editor.globals[g])
#                 else:
#                     acceptor[g] = g
#                 
#             for l in editor.locals:
#                 acceptor[l] = l
#         else:
#             print('else')
#             cur_parent = cur_ctx.parent
#             cur_feature = cur_ctx.get_feature_in_parent()
#             
#             main_path_ctx = get_ctx_parent_of_type(cur_ctx, 'main')
#             if main_path_ctx is not None:
#                 path = []
#                 for i in range(cur_feature[1]):
#                     path.append(get_ctx_text(cur_parent['step'][i], editor))
#                 
#                 path = '/' + '/'.join(path)
#                 for f in os.listdir(path):
#                     acceptor[f] = f
#             else:
#                   
#                 if cur_ctx.type == 'argument':
#                     expr = get_ctx_parent_of_type(cur_ctx, 'expr')
#                     obj = get_obj_for_ctx(expr['calee'], editor)
#                     pass
#                 elif cur_feature[0] == 'attr':
#                     print('attr')
#                     calee_ctx = cur_parent['calee']
#                     calee_text = editor.text()[calee_ctx.slice.start:calee_ctx.slice.stop]
#                     obj = eval(calee_text, editor.globals, editor.locals)
#                     for d in dir(obj):
#                         acceptor[d] = d
#                 else:
#                     print('else')
#                     pass
#         
#         print('WHAT?')
#         print(cur_ctx)
         
#         for i,c in enumerate(reversed(context)):
#             if not isinstance(c, (ast.Attribute, ast.Name, ast.Call, ast.Subscript)):
#                 obj = eval(compile(ast.Expression(context[i+1]), '(none)', 'eval'))
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
         
