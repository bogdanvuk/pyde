from pyde.application import app
from PyQt4.QtGui import QWidget, QColor
from PyQt4.QtCore import pyqtSlot, QObject, Qt
import re
import string
from PyQt4.Qsci import QsciScintilla
from collections import OrderedDict

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
        return len(self.text)
    
    def update(self, text):
        self.text = text
        
    def shift(self, delta):
        self.pos += delta
        

class TemplContext(object):
    PARSE_RE = re.compile(r'({{|}}|{}|{:[^}]+?}|{\w+?(?:\.\w+?)*}|'
                      r'{\w+?(?:\.\w+?)*:[^}]+?})')
    
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
#                 text = string.Template(text).safe_substitute(**{position.name:param_val})

class TemplActuator(object):

    
    def __init__(self):
        self.templates = {}
        self.indicators = {}

    def insert(self, tmpl, editor):
        
        tmpl_ctx = TemplContext(tmpl, editor.pos)
        if editor in self.indicators:
            editor.clearAllIndicators(self.indicators[editor])

        if tmpl_ctx.positions:
            if editor in self.templates:
                self.quit(editor)
            
            self.templates[editor] = tmpl_ctx
            
            editor.insert(tmpl_ctx.text)
            
            if editor not in self.indicators:
                self.indicators[editor] = editor.indicatorDefine(QsciScintilla.INDIC_BOX, QColor(Qt.black))
            
            i = 10
            for _, p in tmpl_ctx.positions.items():
                i+=1
                editor.setIndicatorRange(self.indicators[editor], p.pos, len(p), i)
            
            self.next()
        else:
            editor.insert(tmpl.text)
    
    def move(self, editor, pos_name):
        tmpl_ctx = self.templates[editor]
        indicator = self.indicators[editor]
        
        transition_points = []
        pos = tmpl_ctx.insert_pos
        length = editor.length()
        end_pos = length
        while pos <= end_pos:
            indic_start = editor.indicatorStart(indicator, pos)
            indic_end = editor.indicatorEnd(indicator, indic_start+1)
            if indic_start == indic_end == 0: # No indicators found.
                break
#             if not transition_points:
#                 transition_points.append(indic_start)
            # Sanity check: scintilla collapses a run of
            # single-char indicators to one indicator, and we would lose
            # boundary info for all but the first indicator in this run.
#             current_run_pos = indic_start
#             family_next = editor.styleAt(current_run_pos)
#             while current_run_pos < indic_end - 1:
#                 family_start = family_next
#                 family_next = editor.styleAt(current_run_pos + 1)
#                 if family_start != family_next:
#                     transition_points.append(current_run_pos + 1)
#                     current_run_pos += 1
#                 else:
#                     break
            
#             if editor.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, indicator, indic_end):
            print(editor.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, indicator, indic_end))
            transition_points.append(indic_end)
            if indic_end >= end_pos:  # Past the end of the region specified.
                break
            pos = indic_end
            if indic_end == end_pos:
                # In case the last indicator ends on the last char, not at the
                # posn after the last character
                pos += 1
        
        print(transition_points)
#         tmpl_ctx.positions[pos_name]
#         editor.anchor = indicator.pos
#         editor.SendScintilla(QsciScintilla.SCI_SETSELECTIONEND, indicator.pos + len(indicator))
        
    
    def prev(self):
        editor = app.active_widget()
        indicator = self.indicators[editor]
        
        position = editor.SendScintilla(QsciScintilla.SCI_GETCURRENTPOS)
        docLen = editor.length()

        isInIndicator = editor.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, indicator,  position)
        posStart = editor.SendScintilla(QsciScintilla.SCI_INDICATORSTART, indicator,  position)
        posEnd = editor.SendScintilla(QsciScintilla.SCI_INDICATOREND, indicator,  position)

        # pre-condition
        if ((posStart == 0) and (posEnd == docLen - 1)):
            return False

        if (posStart <= 0):
            isInIndicator = editor.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, indicator,  docLen - 1)
            posStart = editor.SendScintilla(QsciScintilla.SCI_INDICATORSTART, indicator, docLen - 1)
            
        if (isInIndicator): # try to get out of indicator
            posStart = editor.SendScintilla(QsciScintilla.SCI_INDICATORSTART, indicator, posStart - 1)
            if (posStart <= 0):
                posStart = editor.SendScintilla(QsciScintilla.SCI_INDICATORSTART, indicator, docLen - 1)

        newPos = posStart - 1
        posStart = editor.SendScintilla(QsciScintilla.SCI_INDICATORSTART, indicator, newPos)
        posEnd = editor.SendScintilla(QsciScintilla.SCI_INDICATOREND, indicator, newPos)

        # found
        if (editor.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, indicator, posStart)):
            currentline = editor.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, posEnd);
            editor.SendScintilla(QsciScintilla.SCI_ENSUREVISIBLE, currentline);	 #make sure target line is unfolded
            
            editor.SendScintilla(QsciScintilla.SCI_SETSEL, posEnd, posStart);
            editor.SendScintilla(QsciScintilla.SCI_SCROLLCARET);
            return True;

        return False;
        
    def next(self):
        editor = app.active_widget()
        indicator = self.indicators[editor]
        
        position = editor.SendScintilla(QsciScintilla.SCI_GETCURRENTPOS)
        docLen = editor.length()

        isInIndicator = editor.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, indicator,  position)
        posStart = editor.SendScintilla(QsciScintilla.SCI_INDICATORSTART, indicator,  position)
        posEnd = editor.SendScintilla(QsciScintilla.SCI_INDICATOREND, indicator,  position)

        # pre-condition
        if ((posStart == 0) and (posEnd == docLen - 1)):
            return False

        if (posEnd >= docLen):
            isInIndicator = editor.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, indicator,  0)
            posEnd = editor.SendScintilla(QsciScintilla.SCI_INDICATOREND, indicator, 0)
            
        if (isInIndicator): # try to get out of indicator
            posEnd = editor.SendScintilla(QsciScintilla.SCI_INDICATOREND, indicator, posEnd)

        if (posEnd >= docLen):
            posEnd = editor.SendScintilla(QsciScintilla.SCI_INDICATOREND, indicator, 0)

        newPos = posEnd
        posStart = editor.SendScintilla(QsciScintilla.SCI_INDICATORSTART, indicator, newPos)
        posEnd = editor.SendScintilla(QsciScintilla.SCI_INDICATOREND, indicator, newPos)

        # found
        if (editor.SendScintilla(QsciScintilla.SCI_INDICATORVALUEAT, indicator, posStart)):
            currentline = editor.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, posEnd);
            editor.SendScintilla(QsciScintilla.SCI_ENSUREVISIBLE, currentline);	 #make sure target line is unfolded
            
            editor.SendScintilla(QsciScintilla.SCI_SETSEL, posStart, posEnd);
            editor.SendScintilla(QsciScintilla.SCI_SCROLLCARET);
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
    
app.register_global("templ", TemplActuator())
# app.register_global("templ_contentassist", TemplContentAssist())
