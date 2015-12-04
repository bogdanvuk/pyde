from pyde.application import app, KeyPressNotConsumed
from PyQt4.Qsci import QsciScintilla
import string
import os

def forward_char():
    app.active_widget().forward_char()
    
def backward_char():
    app.active_widget().backward_char()
    
def forward_line():
    app.active_widget().SendScintilla(QsciScintilla.SCI_LINEDOWN)

def backward_line():
    app.active_widget().SendScintilla(QsciScintilla.SCI_LINEUP)

   
def content_assist():
    editor = app.active_widget()
#     selected_text = editor.selectedText()
    if app.globals.content_assist.active:
        app.globals.content_assist.fill_query()
    elif editor.hasSelectedText():
        editor.pos = editor.SendScintilla(QsciScintilla.SCI_GETSELECTIONEND)
        return app.globals.content_assist.activate()
    else:
        text = editor.text()
        if text:
            last_char = text[editor.pos-1] 
            if last_char not in string.whitespace:
                return app.globals.content_assist.activate()
        else:
            return app.globals.content_assist.activate()

#    raise KeyPressNotConsumed
#     app.active_widget().content_assist()
    
def evaluate():
    app.active_widget().evaluate()

class Path(object):
    def __init__(self, path=None):
        if not path:
            path = os.getcwd()
            
        self.path = path
    
    def __repr__(self):
        return '"' + self.path + '"'
    
    def __str__(self):
        return self.path

def open_file(path:Path):
    pass

app.register_global("evaluate", evaluate)
app.register_global("forward_char", forward_char)
app.register_global("backward_char", backward_char)
app.register_global("open_file", open_file)

# def open_file():
    
