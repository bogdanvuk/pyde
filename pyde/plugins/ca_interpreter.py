from PyQt4.QtCore import QObject
from pyde.ddi import Dependency, ddic
from pyde.plugins.parser import ContextVisitor
from pyde.plugins.templating import TemplFunc
from inspect import getfullargspec
import os

def get_ctx_text(ctx, editor):
    return editor.text()[ctx.slice.start:ctx.slice.stop]
    
def get_obj_for_ctx(ctx, editor):
    text = get_ctx_text(ctx, editor)
    return eval(text, editor.globals, editor.locals)

def get_ctx_parent_of_type(ctx, parent_type):
    while ctx.parent is not None:
        if ctx.parent.type == parent_type:
            return ctx.parent
    
        ctx = ctx.parent
        
    return None

class PyInterpretContentAssist(QObject):
    def __init__(self, 
                 editor : Dependency('view/', lambda e: isinstance(e.widget, ddic['cls/ipython'])),
                 ca : Dependency('content_assist'),
                 win : Dependency('win')):
        super().__init__()
        self.ca = ca
        self.win = win
        self.editor = editor
        self.ca.complete.connect(self.complete)
     
    def complete(self, acceptor):
        view = self.win.active_view()
        editor = view.widget
        if hasattr(editor, 'ast'):
            cv = ContextVisitor(editor.ast)
            cur_ctx = cv.context_at(editor.anchor)
        else:
            cur_ctx = None

        if cur_ctx is None:
            print('cur_ctx = view')
            for g in editor.globals:
                if callable(editor.globals[g]):
                    acceptor[g] = TemplFunc(editor.globals[g])
                else:
                    acceptor[g] = g
                
            for l in editor.locals:
                acceptor[l] = l
        else:
            print('else')
            cur_parent = cur_ctx.parent
            cur_feature = cur_ctx.get_feature_in_parent()
            
            main_path_ctx = get_ctx_parent_of_type(cur_ctx, 'main')
            if main_path_ctx is not None:
                path = []
                for i in range(cur_feature[1]):
                    path.append(get_ctx_text(cur_parent['step'][i], editor))
                
                path = '/' + '/'.join(path)
                for f in os.listdir(path):
                    acceptor[f] = f
            else:
                  
                if cur_ctx.type == 'argument':
                    expr = get_ctx_parent_of_type(cur_ctx, 'expr')
                    obj = get_obj_for_ctx(expr['calee'], editor)
                    pass
                elif cur_feature[0] == 'attr':
                    print('attr')
                    calee_ctx = cur_parent['calee']
                    calee_text = editor.text()[calee_ctx.slice.start:calee_ctx.slice.stop]
                    obj = eval(calee_text, editor.globals, editor.locals)
                    for d in dir(obj):
                        acceptor[d] = d
                else:
                    print('else')
                    pass
        
        print('WHAT?')
        print(cur_ctx)
         
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
         
