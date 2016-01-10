from PyQt4.QtCore import QObject, pyqtSignal
from PyQt4.Qsci import QsciScintilla
from difflib import SequenceMatcher
from pyde.ddi import Dependency
from pyde.plugins.context import Context, ViewContext

class ContentAssistContext(ViewContext):
    @property
    def slice(self):
        return self.parent.slice


class ContentAssist(QObject):
    complete = pyqtSignal(dict)
        
    def __init__(self, win : Dependency('win'), context : Dependency('context')):
        super().__init__()
        self.active_editor = None
        self.active_dict = None
        self.ca_start = 0
        self.active = False
        self.win = win
        self.context = context
#         app.view_added.connect(self.new_view)
    
#     @pyqtSlot(QWidget)
#     def new_view(self, obj):
#         obj.textChanged.connect(self.text_changed)
    
    def text_modified(self, pos, mtype, text, length, linesAdded, line, foldNow,
                   foldPrev, token, annotationLinesAdded):
        
        if ((mtype & QsciScintilla.SC_MOD_INSERTTEXT) != 0):
            print('modified')
            self.show()

    
    def set_start(self, pos):
        self.ca_start = pos
    
    def fill_query(self):
        if self.active:
            text = self.active_editor.text()[self.ca_start:self.active_editor.pos]
            common_text = ""

            for k in sorted(self.sieve()):
                if common_text:
                    s = SequenceMatcher(None, common_text, k)
                    match = s.find_longest_match(0, len(common_text), 0, len(k))
                    if text or (match.b == 0):
                        common_text = k[match.b:match.b + match.size]
                        if not common_text:
                            break
                else:
                    common_text = k

        if common_text:
            self.active_editor.SendScintilla(QsciScintilla.SCI_DELETERANGE, self.ca_start, self.active_editor.pos - self.ca_start)
            self.active_editor.insert(common_text)
            self.active_editor.pos = self.ca_start + len(common_text)
        self.show()
    
    def sieve(self):
        text = self.active_editor.text()[self.ca_start:self.active_editor.pos+1]
#         for k in difflib.get_close_matches(text, self.active_dict.keys(), n=100, cutoff=0.6):  
        for k in self.active_dict:

            if (not text) or (text in k):
                yield k
    
    def show(self):
        print('show: ' + self.active_editor.text()[self.ca_start:self.active_editor.pos+1])
        print('show list: ', ' '.join(sorted(self.sieve())))
        self.active_editor.SendScintilla(QsciScintilla.SCI_AUTOCSHOW,
                                 self.active_editor.pos - self.ca_start, 
                                 ' '.join(sorted(self.sieve())).encode())
        self.active = True

    def activate(self):
        print('activated')
        self.active_editor = self.win.active_view()
        self.active_editor.SCN_AUTOCSELECTION.connect(self.close_selected)
        self.active_editor.SCN_AUTOCCANCELLED.connect(self.close_canceled)
        self.active_editor.SCN_AUTOCCHARDELETED.connect(self.close_char_deleted)
        self.active_editor.SCN_MODIFIED.connect(self.text_modified)
        self.active_editor.SendScintilla(QsciScintilla.SCI_AUTOCSETAUTOHIDE, False)
        
        self.ca_start = self.active_editor.pos
        
        self.active_dict = {}

        self.complete.emit(self.active_dict)
        
        cur_ctx = self.context.active_context()
        self.context.update_context(cur_ctx.uri + ['content_assist'], ContentAssistContext(self))
        
        if self.active_dict:
            self.show()

    def previous_line(self):
        self.active_editor.SendScintilla(QsciScintilla.SCI_LINEUP)

    def next_line(self):
        self.active_editor.SendScintilla(QsciScintilla.SCI_LINEDOWN)

    def close_char_deleted(self):
        print('close_char_deleted')
        self.show()
        
    def close_canceled(self):
        print('canceled')
#         self.active_editor.SCN_MODIFIED.disconnect(self.text_modified)
        self.active = False

    def select(self):
        print('selected')
        selected = self.active_editor.SendScintilla(QsciScintilla.SCI_AUTOCGETCURRENT)
        self.close_selected(selected, None)

    def close_selected(self, selected, param):
        print('close_selected')
        self.active = False
#         self.active_editor.SCN_AUTOCSELECTION.disconnect(self.close)
        self.active_editor.SCN_MODIFIED.disconnect(self.text_modified)
#         self.active_editor.SendScintilla(QsciScintilla.SCI_AUTOCCANCEL)
        
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
    
# app.register_global("content_assist", ContentAssist())
