from pyde.application import ddic
from PyQt4.QtGui import QWidget, QColor
from PyQt4.QtCore import pyqtSlot, QObject, Qt
import re
import string
from PyQt4.Qsci import QsciScintilla
from collections import OrderedDict
from inspect import signature
from pyde.ddi import diinit, Dependency
import inspect

class FuncArgContentAssist(QObject):
    language = None

class TemplFunc:
    @diinit
    def __init__(self, func, actuator : Dependency('templ_actuator')):
        self.func = func
        self.sig = signature(func)
        self.actuator = actuator
        params = []
        for _,p in self.sig.parameters.items():
            params.append('{' + str(p).split(':')[0] + '}')
#             params.append(str(p).split(':')[0])
        
        self.text = self.func.__name__ + '(' + ','.join(params) + ')'        
        
    def apply(self, editor):
        if hasattr(editor, 'templating'):
            editor.templating.insert(self)
        else:
            self.editor.insert(self.text)
        
    def param_val(self, key):
        p = self.sig.parameters[key]
        if issubclass(p.annotation, FuncArgContentAssist):
            return p.annotation().init_value
        elif p.default is inspect._empty:
            return key
        else:
            return str(p.default)
        
    def param_pos(self, key, text):
#         p = self.sig.parameters[key]
        p = list(self.sig.parameters.values())[key]
        if issubclass(p.annotation, FuncArgContentAssist):
            return p.annotation().pos(text)
        else:
            return None
        
#         a = self.sig.parameters['path'].annotation
#         if a:
#             if a == str:
#                 return "''"
#             else:
#                 return str(a())
#         else:
#         return key
    #             return str(self.sig.parameters[key])

class TemplParam(object):
    vtype = str
    
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

class TemplPosition:
    def __init__(self, re_match=None):
        if re_match is not None:
            self.text = re_match.group()[1:-1]
            elems = self.text.split('=')
            if len(elems) == 1:
                self.name = self.text
                self.def_val = None
            else:
                self.name, self.def_val = elems

            self.pos = re_match.span()[0] + 1
    
    def __len__(self):
        return len(self.text)
    
    def update(self, text):
        self.text = text
        
    def shift(self, delta):
        self.pos += delta
        

class TemplContext(object):
#     PARSE_RE = re.compile(r'({{|}}|{}|{:[^}]+?}|{\w+?(?:\.\w+?)*}|'
#                       r'{\w+?(?:\.\w+?)*:[^}]+?})')
    PARSE_RE = re.compile(r'({{|}}|{}|{:[^}]+?}|{[\w=]+?(?:\.[\w=]+?)*}|'
                      r'{[\w=]+?(?:\.\[\w=]?)*:[^}]+?})')
    
    def __init__(self, templ, insert_pos):
        self.templ = templ
        self.positions = OrderedDict()
        
        self.text = templ.text
        self.insert_pos = insert_pos
        params_left = True
        while (params_left):
            m = self.PARSE_RE.search(self.text)
            if m is not None:
                if m.group() not in ['{{', '}}', '{']:
                    position = TemplPosition(m)
                    position.shift(insert_pos - 1)
                    self.positions[position.name] = position
                    param_val = self.templ.param_val(position.name)
                    position.update(param_val)
                    self.text = self.text[:m.span()[0]] + param_val +  self.text[m.span()[1]:]
            else:
                params_left = False
                
class TemplActuator:
    indic_val_offset = 10
    
    def __init__(self, view : Dependency('view/')):
        self.indicators = {}
        self.view = view
        self.editor = view.widget
        self.editor.templating = self
        self.tmpl = None
        self.tmpl_ctx = None
        
    def insert(self, tmpl):
        self.tmpl = tmpl
        self.tmpl_ctx = TemplContext(tmpl, self.editor.pos)
        if self.editor in self.indicators:
            self.editor.clearAllIndicators(self.indicators[self.editor])

        if self.tmpl_ctx.positions:
           
            self.editor.insert(self.tmpl_ctx.text)
            
            if self.editor not in self.indicators:
                self.indicators[self.editor] = self.editor.indicatorDefine(QsciScintilla.INDIC_BOX, QColor(Qt.black))
            
            i = self.indic_val_offset
            for _, p in self.tmpl_ctx.positions.items():
                self.editor.setIndicatorRange(self.indicators[self.editor], p.pos, len(p), i)
                i+=1
            
#             self.editor.setIndicatorRange(self.indicators[self.editor], p.pos, len(p), i)
            
            self.next()
        else:
            self.editor.insert(tmpl.text)
            self.resolve()
    
    def resolve(self):
        self.tmpl = None
        self.tmpl_ctx = None
        self.editor.clearAllIndicators(self.indicators[self.editor])
    
    def move(self, pos_name):
        indicator = self.indicators[self.editor]
        
        transition_points = []
        pos = self.tmpl_ctx.insert_pos
        length = self.editor.length()
        end_pos = length
        while pos <= end_pos:
            indic_start = self.editor.indicatorStart(indicator, pos)
            indic_end = self.editor.indicatorEnd(indicator, indic_start+1)
            if indic_start == indic_end == 0: # No indicators found.
                break
            
            transition_points.append(indic_end)
            if indic_end >= end_pos:  # Past the end of the region specified.
                break
            pos = indic_end
            if indic_end == end_pos:
                # In case the last indicator ends on the last char, not at the
                # posn after the last character
                pos += 1
    
    def prev(self):
        indicator = self.indicators[self.editor]
        
        position = self.editor.SendScintilla(QsciScintilla.SCI_GETCURRENTPOS)
        docLen = self.editor.length()

        isInIndicator = self.editor.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, indicator,  position)
        posStart = self.editor.SendScintilla(QsciScintilla.SCI_INDICATORSTART, indicator,  position)
        posEnd = self.editor.SendScintilla(QsciScintilla.SCI_INDICATOREND, indicator,  position)

        # pre-condition
        if ((posStart == 0) and (posEnd == docLen - 1)):
            return False

        if (posStart <= 0):
            isInIndicator = self.editor.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, indicator,  docLen - 1)
            posStart = self.editor.SendScintilla(QsciScintilla.SCI_INDICATORSTART, indicator, docLen - 1)
            
        if (isInIndicator): # try to get out of indicator
            posStart = self.editor.SendScintilla(QsciScintilla.SCI_INDICATORSTART, indicator, posStart - 1)
            if (posStart <= 0):
                posStart = self.editor.SendScintilla(QsciScintilla.SCI_INDICATORSTART, indicator, docLen - 1)

        newPos = posStart - 1
        posStart = self.editor.SendScintilla(QsciScintilla.SCI_INDICATORSTART, indicator, newPos)
        posEnd = self.editor.SendScintilla(QsciScintilla.SCI_INDICATOREND, indicator, newPos)

        # found
        if (self.editor.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, indicator, posStart)):
            currentline = self.editor.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, posEnd);
            self.editor.SendScintilla(QsciScintilla.SCI_ENSUREVISIBLE, currentline);	 #make sure target line is unfolded
            
            indic_val = self.editor.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, indicator, posStart)
            pos = self.tmpl.param_pos(indic_val - self.indic_val_offset, self.editor.text()[posStart: posEnd])
            if pos is None:
                self.editor.SendScintilla(QsciScintilla.SCI_SETSEL, posEnd, posStart);
            else:
                self.editor.pos = posStart + pos
                
            self.editor.SendScintilla(QsciScintilla.SCI_SCROLLCARET);
                
            return True;

        return False;
        
    def next(self):
        indicator = self.indicators[self.editor]
        
        position = self.editor.SendScintilla(QsciScintilla.SCI_GETCURRENTPOS)
        docLen = self.editor.length()

        isInIndicator = self.editor.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, indicator,  position)
        posStart = self.editor.SendScintilla(QsciScintilla.SCI_INDICATORSTART, indicator,  position)
        posEnd = self.editor.SendScintilla(QsciScintilla.SCI_INDICATOREND, indicator,  position)

        # pre-condition
        if ((posStart == 0) and (posEnd == docLen - 1)):
            return False

        if (posEnd >= docLen):
            isInIndicator = self.editor.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, indicator,  0)
            posEnd = self.editor.SendScintilla(QsciScintilla.SCI_INDICATOREND, indicator, 0)
            
        if (isInIndicator): # try to get out of indicator
            posEnd = self.editor.SendScintilla(QsciScintilla.SCI_INDICATOREND, indicator, posEnd)

        if (posEnd >= docLen):
            posEnd = self.editor.SendScintilla(QsciScintilla.SCI_INDICATOREND, indicator, 0)

        newPos = posEnd
        posStart = self.editor.SendScintilla(QsciScintilla.SCI_INDICATORSTART, indicator, newPos)
        posEnd = self.editor.SendScintilla(QsciScintilla.SCI_INDICATOREND, indicator, newPos)

        # found
        if (self.editor.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, indicator, posStart)):
            currentline = self.editor.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, posEnd);
            self.editor.SendScintilla(QsciScintilla.SCI_ENSUREVISIBLE, currentline);	 #make sure target line is unfolded
            
            indic_val = self.editor.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, indicator, posStart)
            pos = self.tmpl.param_pos(indic_val - self.indic_val_offset, self.editor.text()[posStart: posEnd])
            if pos is None:
                self.editor.SendScintilla(QsciScintilla.SCI_SETSEL, posEnd, posStart);
            else:
                self.editor.pos = posStart + pos
                
            self.editor.SendScintilla(QsciScintilla.SCI_SCROLLCARET);
            
            return True;

        return False;

        #self.move(app.views[0], '')
#         tmpl_ctx = self.templates[editor]
        
#         
#         for p in tmpl_ctx.positions:
            
        
    def quit(self, editor=None):
        pass
    
# class TemplContentAssist(QObject):
#     
#     def __init__(self):
#         super().__init__()
#         app.globals.content_assist.complete.connect(self.complete)
#     
#     def complete(self, acceptor):
#         acceptor['proba_templ'] = ExampleTemplate()
    
# app.register_global("templ", TemplActuator())
# app.register_global("templ_contentassist", TemplContentAssist())
