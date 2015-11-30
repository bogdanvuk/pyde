from pyde.application import app, KeyPressNotConsumed
from PyQt4.Qsci import QsciScintilla
import string

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
        if len(text):
            last_char = text[editor.pos-1] 
            if last_char not in string.whitespace:
                return app.globals.content_assist.activate()

#    raise KeyPressNotConsumed
#     app.active_widget().content_assist()
    
def evaluate():
    app.active_widget().evaluate()
    
def open_file(path:str):
    pass

# def open_file():
    
