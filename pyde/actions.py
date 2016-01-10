from PyQt4.Qsci import QsciScintilla
import string
import os
from pyde.ddi import ddic, diinit, Dependency

def forward_char(view=None):
    if view is None:
        view = ddic['win'].active_view()
        
    view.forward_char()

def dflt_view_action_factory(func_name):
    @diinit
    def dflt_view_action(win : Dependency('win')):
        
        v = win.active_view()
        
        while v.parent is not None:
            if hasattr(v.widget, func_name):
                getattr(v.widget, func_name)()
                return
            
            v = v.parent
            
    return dflt_view_action

@diinit
def next_line(context : Dependency('context')):
#def next_line(context = None):
    
    c = context.active_context()
    
    while c.parent is not None:
        if hasattr(c, 'view'):
            if hasattr(c.view, 'next_line'):
                c.view.next_line()
                return
        
        c = c.parent

def backward_char(view=None):
    if view is None:
        view = ddic['win'].active_view()
        
    view.backward_char()

    
# def backward_char():
#     app.active_widget().backward_char()
#     
# def forward_line():
#     app.active_widget().SendScintilla(QsciScintilla.SCI_LINEDOWN)
# 
# def backward_line():
#     app.active_widget().SendScintilla(QsciScintilla.SCI_LINEUP)
# 
#    
@diinit
def content_assist(win : Dependency('win')):
    view = win.active_view()
#     selected_text = editor.selectedText()
    if view.name == 'content_assist':
        view.widget.fill_query()
    else:
        editor = v
        if view.widget.hasSelectedText():
        editor.pos = editor.SendScintilla(QsciScintilla.SCI_GETSELECTIONEND)
        ddic['content_assist'].activate()
    else:
        text = editor.text()
        if text:
            last_char = text[editor.pos-1] 
            if last_char not in string.whitespace:
                ddic['content_assist'].activate()
        else:
            ddic['content_assist'].activate()

    return True

# def select_content_assist():
#     if ddic['content_assist'].active:
#         ddic['content_assist'].fill_query()
    
 
#    raise KeyPressNotConsumed
#     app.active_widget().content_assist()
#     
def evaluate():
    ddic['win'].active_view().evaluate()
# 
# class Path(object):
#     def __init__(self, path=None):
#         if not path:
#             path = os.getcwd()
#             
#         self.path = path
#     
#     def __repr__(self):
#         return '"' + self.path + '"'
#     
#     def __str__(self):
#         return self.path
# 
# def open_file(path:Path):
#     pass
# 
# app.register_global("evaluate", evaluate)
# app.register_global("forward_char", forward_char)
# app.register_global("backward_char", backward_char)
# app.register_global("open_file", open_file)

# def open_file():
    
