from pyde.application import app
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSlot, QObject, pyqtSignal
from PyQt4.Qsci import QsciScintilla
import string

class ContentAssist(QObject):
    complete = pyqtSignal(dict)
        
    def __init__(self):
        super().__init__()
        self.active_editor = None
        self.active_dict = None
        self.ca_start = 0
#         app.view_added.connect(self.new_view)
    
#     @pyqtSlot(QWidget)
#     def new_view(self, obj):
#         obj.textChanged.connect(self.text_changed)
    
    def activate(self):
        self.active_editor = app.active_widget()
        self.active_editor.SCN_AUTOCSELECTION.connect(self.close)
        
        self.ca_start = self.active_editor.pos()
        
        self.active_dict = {}
        self.complete.emit(self.active_dict)
        for key in self.active_dict:
            self.active_editor.content_assist_list.add(key)
            
        self.active_editor.content_assist_list.prepare()
        
        while (not self.active_editor.content_assist_list.isPrepared()):
            pass
        
        self.active_editor.autoCompleteFromAll()
        
#     def close(self):
#         print('CLOS')
    def close(self, selected, param):
        self.active_editor.SCN_AUTOCSELECTION.disconnect(self.close)
        self.active_editor.SendScintilla(QsciScintilla.SCI_AUTOCCANCEL)
        
        cur_pos = self.active_editor.pos()
        
        text = self.active_editor.text()
        
        for i in range(cur_pos-1, 0, -1):
            if text[i] in string.whitespace:
                search_word_start_pos = i + 1
                break
        else:
            search_word_start_pos = 0
            
        for i in range(cur_pos, len(text)):
            if text[i] in string.whitespace:
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
            
        print(text)
        print(param)
    
app.register_global("content_assist", ContentAssist())
