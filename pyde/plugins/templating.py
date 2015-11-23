from pyde.application import app
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSlot, QObject
import re
import string

class Template(object):
   
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        
    def apply(self, editor):
        app.globals.templ.insert(self, editor)
        
    def param_val(self, key):
        return key
#         self.params[key]

class TemplParam(object):
    vtype = str
    
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class ExampleTemplate(Template):
    text = 'Proba {p0} tremplate {p1}'
    params = {'p0':TemplParam(vtype=str), 'p1':TemplParam(vtype=str)}
        

class TemplPosition(object):
    def __init__(self, re_match=None):
        if re_match is not None:
            self.text = re_match.group()[1:-1]
            self.name = self.text
            self.pos = re_match.span()[0] + 1
    
    def __len__(self):
        len(self.text)
    
    def update(self, text):
        self.text = text
        
    def shift(self, delta):
        self.pos += delta
        

class TemplContext(object):
    PARSE_RE = re.compile(r'({{|}}|{}|{:[^}]+?}|{\w+?(?:\.\w+?)*}|'
                      r'{\w+?(?:\.\w+?)*:[^}]+?})')
    
    def __init__(self, templ):
        self.templ = templ
        self.positions = {}
        
        text = templ.text
        params_left = True
        while (params_left):
            m = self.PARSE_RE.search(text)
            if m is not None:
                if m.group() not in ['{{', '}}', '{']:
                    position = TemplPosition(m)
                    self.positions[position.name] = position
                    param_val = self.templ.param_val(position.name)
                    position.update(param_val)
                    text = text[:m.span()[0]] + param_val +  text[m.span()[1]:]
            else:
                params_left = False
#                 text = string.Template(text).safe_substitute(**{position.name:param_val})

class TemplActuator(object):

    
    def __init__(self):
        self.templates = {}
    
    def insert(self, tmpl, editor):
        
        tmpl_ctx = TemplContext(tmpl)
        
        if tmpl_ctx.positions:
            if editor in self.templates:
                self.quit(editor)
            
            self.templates[editor] = tmpl_ctx
            
            pass
        else:
            editor.insert(tmpl.text)
        
    def quit(self, editor=None):
        pass
    
class TemplContentAssist(QObject):
    
    def __init__(self):
        super().__init__()
        app.globals.content_assist.complete.connect(self.complete)
    
    def complete(self, acceptor):
        acceptor['proba_templ'] = ExampleTemplate()
    
app.register_global("templ", TemplActuator())
app.register_global("templ_contentassist", TemplContentAssist())
