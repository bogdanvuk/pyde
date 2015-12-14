from PyQt4.Qsci import QsciScintilla
import string
import os
from pyde.ddi import ddic

def forward_char(view=None):
    if view is None:
        view = ddic['win'].active_view()
        
    view.forward_char()

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
def content_assist():
    editor = ddic['win'].active_view()
#     selected_text = editor.selectedText()
    if ddic['content_assist'].active:
        ddic['content_assist'].fill_query()
    elif editor.hasSelectedText():
        editor.pos = editor.SendScintilla(QsciScintilla.SCI_GETSELECTIONEND)
        return ddic['content_assist'].activate()
    else:
        text = editor.text()
        if text:
            last_char = text[editor.pos-1] 
            if last_char not in string.whitespace:
                return ddic['content_assist'].activate()
        else:
            return ddic['content_assist'].activate()
 
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
    
