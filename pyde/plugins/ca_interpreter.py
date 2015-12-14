from PyQt4.QtCore import QObject
from pyde.ddi import Dependency, ddic

class PyInterpretContentAssist(QObject):
    def __init__(self, 
                 editor : Dependency('view/', lambda e: isinstance(e, ddic['cls/ipython'])),
                 ca : Dependency('content_assist'),
                 win : Dependency('win'),
                 context : Dependency('context')):
        super().__init__()
        self.ca = ca
        self.win = win
        self.editor = editor
        self.context = context
        self.ca.complete.connect(self.complete)
     
    def complete(self, acceptor):
        editor = self.win.active_view()
        context = self.context.context_at_pos(editor.pos)
        cur_ctx = context[-1]
        cur_parent = cur_ctx.parent
        cur_feature = cur_parent.get_child_feature(cur_ctx)
        
        if cur_feature == 'attr':
            calee_ctx = cur_parent.children['calee']
            calee_text = editor.text()[calee_ctx.start:calee_ctx.stop+1]
            obj = eval(calee_text, editor.globals, editor.locals)
            for d in dir(obj):
                acceptor[d] = d
        
        
        print(context)
         
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
         
