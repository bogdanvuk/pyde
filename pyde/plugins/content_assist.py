from PyQt4.QtCore import QObject, pyqtSignal
from PyQt4.Qsci import QsciScintilla
from difflib import SequenceMatcher
from pyde.ddi import Dependency, diinit
from pyde.plugins.context import Context, ViewContext
from pyde.view import View
from PyQt4 import QtCore
import sys
import gc
from pyde.plugins.parser import ContextVisitor

class ContentAssistContext(ViewContext):
    @property
    def slice(self):
        return self.parent.slice


class ContentAssist(QObject):
    complete = pyqtSignal(dict)
        
    def __init__(self, win : Dependency('win'), context : Dependency('context')):
        super().__init__()
        self.editor = None
        self.ca_start = 0
        self.active = False
        self.win = win
        self.context = context
#         app.view_added.connect(self.new_view)
    
#     @pyqtSlot(QWidget)
#     def new_view(self, obj):
#         obj.textChanged.connect(self.text_changed)
    
    
    def deactivate(self):
        self.ca_widget = None
        pass

    def activate(self, editor):
        print('activated')
        
        ca_items = {}

        self.complete.emit(ca_items)
        
        if ca_items:
            self.ca_widget = ContentAssistWidget(editor, ca_items)
            
    def select(self):
        print('selected')
        selected = self.editor.SendScintilla(QsciScintilla.SCI_AUTOCGETCURRENT)
        self.close_selected(selected, None)
    
class GetCurContextCmd:
    def __call__(self, editor, ast):
        cv = ContextVisitor(ast)
        self.cur_ctx = cv.context_at(editor.anchor-1)
    
class ContentAssistWidget(QtCore.QObject):
    
    read_ast = QtCore.pyqtSignal(object)
    
    @diinit
    def __init__(self, editor, items, ca : Dependency('content_assist')):
        super().__init__()
        self.editor = editor.widget
        self.items = items
        self.name = 'content_assist'
        self.view = View(self, editor)
        self.ca = ca
#         if view.widget.hasSelectedText():
#         editor.pos = editor.SendScintilla(QsciScintilla.SCI_GETSELECTIONEND)
#         ddic['content_assist'].activate()
#         self.ca_start = editor.widget.pos
        self.editor.SCN_AUTOCSELECTION.connect(self.close_selected)
        self.editor.SCN_AUTOCCANCELLED.connect(self.close_canceled)
        self.editor.SCN_AUTOCCHARDELETED.connect(self.close_char_deleted)
        self.editor.SCN_MODIFIED.connect(self.text_modified)
        self.editor.SendScintilla(QsciScintilla.SCI_AUTOCSETAUTOHIDE, False)
        self.cur_ctx_cmd = GetCurContextCmd()

        self.read_ast.connect(self.editor.ast.read_only, type=QtCore.Qt.BlockingQueuedConnection)
        self.read_ast.emit(self.cur_ctx_cmd)
        self.read_ast.disconnect()
        
        if self.cur_ctx_cmd.cur_ctx is None:
            self.ca_start = self.editor.anchor
        elif self.cur_ctx_cmd.cur_ctx.type == 'NAME':
            self.ca_start = self.cur_ctx_cmd.cur_ctx.slice.start
        else:
            self.ca_start = self.cur_ctx_cmd.cur_ctx.slice.stop
            
        self.show()

    def previous_line(self):
        self.editor.SendScintilla(QsciScintilla.SCI_LINEUP)

    def next_line(self):
        self.editor.SendScintilla(QsciScintilla.SCI_LINEDOWN)

    def show(self):
        print('show: ' + self.editor.text()[self.ca_start:self.editor.pos])
        print('show list: ', ' '.join(sorted(self.sieve())))
        self.editor.SendScintilla(QsciScintilla.SCI_AUTOCSHOW,
                                 self.editor.pos - self.ca_start, 
                                 ' '.join(sorted(self.sieve())).encode())

    def text_modified(self, pos, mtype, text, length, linesAdded, line, foldNow,
                   foldPrev, token, annotationLinesAdded):
        
        if ((mtype & QsciScintilla.SC_MOD_INSERTTEXT) != 0):
            print('modified')
            self.show()

    def close_selected(self, selected, param):
        print('close_selected')
        self.close()
#         self.editor.SCN_AUTOCSELECTION.disconnect(self.close)
#         self.editor.SCN_MODIFIED.disconnect(self.text_modified)
#         self.editor.SendScintilla(QsciScintilla.SCI_AUTOCCANCEL)
        
        cur_pos = self.editor.pos
        
        text = self.editor.text()
        
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
        
        self.editor.SendScintilla(QsciScintilla.SCI_DELETERANGE, search_word_start_pos, search_word_end_pos - search_word_start_pos)
        selected_obj = self.items[selected.decode()]

        if hasattr(selected_obj, 'apply'):
            selected_obj.apply(self.editor)
        else:
            self.editor.insert(str(selected_obj))
            self.editor.pos += len(str(selected_obj))
        
        
        
    def close_char_deleted(self):
        print('close_char_deleted')
        self.show()
        
    def close_canceled(self):
        print('canceled')
#         self.editor.SCN_MODIFIED.disconnect(self.text_modified)
        self.close()
        
    def close(self):
        self.editor.SCN_AUTOCSELECTION.disconnect(self.close_selected)
        self.editor.SCN_AUTOCCANCELLED.disconnect(self.close_canceled)
        self.editor.SCN_AUTOCCHARDELETED.disconnect(self.close_char_deleted)
        self.editor.SCN_MODIFIED.disconnect(self.text_modified)
        self.editor.SendScintilla(QsciScintilla.SCI_AUTOCCANCEL)
        
        self.ca.deactivate()
        self.view.delete()

    def fill_query(self):
        text = self.editor.text()[self.ca_start:self.editor.pos]
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
            self.editor.SendScintilla(QsciScintilla.SCI_DELETERANGE, self.ca_start, self.editor.pos - self.ca_start)
            self.editor.insert(common_text)
            self.editor.pos = self.ca_start + len(common_text)
        self.show()
    
    def sieve(self):
        text = self.editor.text()[self.ca_start:self.editor.pos]
#         for k in difflib.get_close_matches(text, self.items.keys(), n=100, cutoff=0.6):  
        for k in self.items:

            if (not text) or (text in k):
                yield k

    
# app.register_global("content_assist", ContentAssist())
