from pyde.application import app

def forward_char():
    app.active_widget().forward_char()
    
def backward_char():
    app.active_widget().backward_char()
    
def content_assist():
    app.active_widget().content_assist()
    
def evaluate():
    app.active_widget().evaluate()
    
def open_file(path:str):
    pass

# def open_file():
    
