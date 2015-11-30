from pyde.application import app
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSlot, QObject, pyqtSignal
from PyQt4.Qsci import QsciScintilla
import string
from difflib import SequenceMatcher
import difflib

class ContentAssist(QObject):
    complete = pyqtSignal(dict)
        
    def __init__(self):
        super().__init__()
        self.active_editor = None
        self.active_dict = None
        self.ca_start = 0
        self.active = False
#         app.view_added.connect(self.new_view)
    
#     @pyqtSlot(QWidget)
#     def new_view(self, obj):
#         obj.textChanged.connect(self.text_changed)
    
    def text_modified(self, pos, mtype, text, length, linesAdded, line, foldNow,
                   foldPrev, token, annotationLinesAdded):
        
        if ((mtype & QsciScintilla.SC_MOD_INSERTTEXT) != 0) or \
            ((mtype & QsciScintilla.SC_MOD_DELETETEXT) != 0):
            
            self.show()

    
    def set_start(self, pos):
        self.ca_start = pos
    
    def fill_query(self):
        if self.active:
            common_text = ""
            for k in self.sieve():
                if not common_text:
                    common_text = k
                else:
                    s = SequenceMatcher(None, common_text, k)
                    common_text = common_text[0:s.find_longest_match(0, len(common_text), 0, len(k)).size]
        
        self.active_editor.SendScintilla(QsciScintilla.SCI_DELETERANGE, self.ca_start, self.active_editor.pos)
        self.active_editor.insert(common_text)
        self.active_editor.pos = self.ca_start + len(common_text)
        self.show()
    
    def sieve(self):
        text = self.active_editor.text()[self.ca_start:self.active_editor.pos]
#         for k in difflib.get_close_matches(text, self.active_dict.keys(), n=100, cutoff=0.6):  
        for k in self.active_dict:
            if text in k:
                yield k
    
    def show(self):
        self.active_editor.SendScintilla(QsciScintilla.SCI_AUTOCSHOW,
                                 self.active_editor.pos - self.ca_start, 
                                 ' '.join(sorted(self.sieve())).encode())
        self.active = True

    def activate(self):
        self.active_editor = app.active_widget()
        self.active_editor.SCN_AUTOCSELECTION.connect(self.close_selected)
        self.active_editor.SCN_AUTOCCANCELLED.connect(self.close_canceled)
        self.active_editor.SCN_MODIFIED.connect(self.text_modified)
        
        self.ca_start = self.active_editor.pos
        
        self.active_dict = {}

        self.complete.emit(self.active_dict)
        self.show()

    def close_canceled(self):
        self.active = False

    def close_selected(self, selected, param):
        print('closed')
        self.active = False
#         self.active_editor.SCN_AUTOCSELECTION.disconnect(self.close)
        self.active_editor.SCN_MODIFIED.disconnect(self.text_modified)
        self.active_editor.SendScintilla(QsciScintilla.SCI_AUTOCCANCEL)
        
        cur_pos = self.active_editor.pos
        
        text = self.active_editor.text()
        
        for i in range(cur_pos-1, 0, -1):
            if not (text[i].isalnum() or text[i] == '_'):
                search_word_start_pos = i + 1
                break
        else:
            search_word_start_pos = 0
            
        for i in range(cur_pos, len(text)):
            if not (text[i].isalnum() or text[i] == '_'):
                search_word_end_pos = i
                break
        else:
            search_word_end_pos = len(text)
        
        self.active_editor.SendScintilla(QsciScintilla.SCI_DELETERANGE, search_word_start_pos, search_word_end_pos - search_word_start_pos)
        selected_obj = self.active_dict[selected.decode()]

        if hasattr(selected_obj, 'apply'):
            selected_obj.apply(self.active_editor)
        else:
            self.active_editor.insert(str(selected_obj))
            self.active_editor.pos += len(str(selected_obj))
    
app.register_global("content_assist", ContentAssist())
