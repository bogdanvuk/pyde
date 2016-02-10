from PyQt4.QtCore import QObject, pyqtSignal
from PyQt4.Qsci import QsciScintilla
from difflib import SequenceMatcher
from pyde.ddi import Dependency, diinit
from pyde.plugins.context import Context, ViewContext
from pyde.view import View
from PyQt4 import QtCore
import sys
import gc
#from pyde.plugins.parser import ContextVisitor

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
    
class GetCaStartCmd:
    def __call__(self, editor, ast):
#        cv = ContextVisitor(ast)
        cur_ctx = ast.tokens.token_at_pos(editor.anchor-1)
        if cur_ctx is None:
            self.ca_start = editor.anchor
        elif cur_ctx.type == 'NAME':
            self.ca_start = cur_ctx.slice.start
        else:
            self.ca_start = cur_ctx.slice.stop

def find_longest_match_at_start(s1, s2):
    ret = ''
    for c1, c2 in zip(s1, s2):
        if c1==c2:
            ret += c1
        else:
            break
        
    return ret
    
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
        self.editor.SCN_AUTOCCANCELLED.connect(self.close)
        self.editor.SCN_AUTOCCHARDELETED.connect(self.close_char_deleted)
        self.editor.SCN_CHARADDED.connect(self.show)
        self.editor.SCN_FOCUSOUT.connect(self.close)
#        self.editor.SCN_CHARADDED.connect(self.show)
#         self.editor.SCN_MODIFIED.connect(self.text_modified)
        self.editor.SendScintilla(QsciScintilla.SCI_AUTOCSETAUTOHIDE, False)
#        self.editor.SendScintilla(QsciScintilla.SCI_SETMODEVENTMASK, (QsciScintilla.SC_MOD_INSERTTEXT | QsciScintilla.SC_MOD_DELETETEXT))
        self.editor.SendScintilla(QsciScintilla.SCI_AUTOCSETCANCELATSTART, False)
        self.ca_start_cmd = GetCaStartCmd()

#         self.read_ast.connect(self.editor.ast.read_only, type=QtCore.Qt.BlockingQueuedConnection)
#         self.read_ast.emit(self.ca_start_cmd)
#         self.read_ast.disconnect()
#         
#         self.ca_start = self.ca_start_cmd.ca_start
# #         print()
# #         
# #         if self.cur_ctx_cmd.cur_ctx is None:
# #             self.ca_start = self.editor.anchor
# #         elif self.cur_ctx_cmd.cur_ctx.type == 'NAME':
# #             self.ca_start = self.cur_ctx_cmd.cur_ctx.slice.start
# #         else:
# #             self.ca_start = self.cur_ctx_cmd.cur_ctx.slice.stop
#             
        self.show()

    def previous_line(self):
        self.editor.SendScintilla(QsciScintilla.SCI_LINEUP)

    def next_line(self):
        self.editor.SendScintilla(QsciScintilla.SCI_LINEDOWN)

    def show(self):
#         print('show: ' + self.editor.text()[self.ca_start:self.editor.pos])
#         print('show list: ', ' '.join(sorted(self.sieve())))
        self.ca_list_starting_with = sorted(self.sieve_starting_with())
        self.ca_list_anywhere = sorted(self.sieve_anywhere())
        self.ca_list = self.ca_list_starting_with + self.ca_list_anywhere
        min_pos = self.editor.pos
        for _,i in self.items.items():
            if i.start_pos < min_pos:
                min_pos = i.start_pos
                 
        if self.ca_list:
            self.editor.SendScintilla(QsciScintilla.SCI_AUTOCSHOW,
                                     self.editor.pos - min_pos, 
                                     (' '.join(self.ca_list)).encode())
            self.editor.SendScintilla(QsciScintilla.SCI_AUTOCSELECT,
                          1,
                          self.ca_list[0].encode())
#             self.editor.SendScintilla(QsciScintilla.SCI_VCHOME)

#         elif len(self.ca_list) == 1:
#             self.close_selected(self.ca_list[0].encode(), None)
        else:
            self.close_canceled()
#         for name in self.ca_list:

    def text_modified(self, pos, mtype, text, length, linesAdded, line, foldNow,
                   foldPrev, token, annotationLinesAdded):
         
        print("Event: ", '%02x'%mtype)
        print("Text: ", text)
#         if ((mtype & QsciScintilla.SC_MOD_CHANGESTYLE) != 0):
#             if self.modified:
#                 self.show()
#                 
#             self.modified = False
#             
#         elif ((mtype & QsciScintilla.SC_MOD_INSERTTEXT) != 0):
#             print('modified')
#             self.modified = True
#             self.show()
#         elif ((mtype & QsciScintilla.SC_MOD_DELETETEXT) != 0):
#             self.show()

    def close_selected(self, selected, param):
        print('close_selected')
        self.close()
       
        cur_pos = self.editor.pos
        
        ca_selected = self.items[selected.decode()]
        self.editor.SendScintilla(QsciScintilla.SCI_DELETERANGE, ca_selected.start_pos, cur_pos - ca_selected.start_pos)
        self.editor.pos = ca_selected.start_pos
        template = ca_selected.template
        if hasattr(template, 'apply'):
            template.apply(self.editor)
        else:
            self.editor.insert(str(ca_selected.template))
            self.editor.pos += len(str(ca_selected.template))
        
    def close_char_deleted(self):
        print('close_char_deleted')
        self.show()
        
    def close(self):
        self.editor.SCN_AUTOCSELECTION.disconnect(self.close_selected)
        self.editor.SCN_AUTOCCANCELLED.disconnect(self.close_canceled)
        self.editor.SCN_AUTOCCHARDELETED.disconnect(self.close_char_deleted)
        self.editor.SCN_CHARADDED.disconnect(self.show)
        self.editor.SCN_FOCUSOUT.disconnect(self.close)
#         self.editor.SCN_MODIFIED.disconnect(self.text_modified)
        self.editor.SendScintilla(QsciScintilla.SCI_AUTOCCANCEL)
        
        self.ca.deactivate()
        self.view.delete()

    def find_longest_common_sequence(self, l, anywhere=False):
        common_text = ""
        insert_text = ""
        for c in l:
            text = self.editor.text()[self.items[c].start_pos:self.editor.pos]
            if text:
                c = ''.join(c.partition(text)[1:])
                
            if common_text:
                if anywhere and (not text):
                    s = SequenceMatcher(None, common_text, c)
                    match = s.find_longest_match(0, len(common_text), 0, len(c))
                    common_text = c[match.b:match.b + match.size]
                else:
                    common_text = find_longest_match_at_start(common_text, c)            
            else:
                common_text = c
            
            insert_text = common_text[len(text):]
            if not common_text:
                break
    
                
        return common_text, insert_text

#     def find_longest_common_sequence(self, l):
#         common_text = ""
#         
#         for c in l:
#             text = self.editor.text()[self.items[c].start_pos:self.editor.pos]
#             if common_text:
#                 s = SequenceMatcher(None, common_text, c)
#                 match = s.find_longest_match(0, len(common_text), 0, len(c))
#                 if text or (match.b == 0):
#                     common_text = c[match.b:match.b + match.size]
#                     insert_text = common_text[self.editor.pos - self.items[c].start_pos:]
#                     if not common_text:
#                         break
#             else:
#                 common_text = c
#                 insert_text = common_text[self.editor.pos - self.items[c].start_pos:]
# 
#         return common_text, insert_text
    
    def fill_query(self):

        common_text = ""
        if len(self.ca_list) == 1:
            self.close_selected(self.ca_list[0].encode(), None)
            return
        elif self.ca_list_starting_with:
            common_text, insert_text = self.find_longest_common_sequence(self.ca_list_starting_with)
        else:
            common_text, insert_text = self.find_longest_common_sequence(self.ca_list_anywhere)

        if common_text:
#             self.editor.SendScintilla(QsciScintilla.SCI_DELETERANGE, self.ca_start, self.editor.pos - self.ca_start)
            self.editor.insert(insert_text)
            self.editor.pos += len(insert_text)
            
        self.show()

    def sieve(self):
        text = self.editor.text() #[self.ca_start:self.editor.pos]
        cur_pos = self.editor.pos
#         for k in difflib.get_close_matches(text, self.items.keys(), n=100, cutoff=0.6):  
        for name, ca_item in self.items.items():
            ca_text = text[ca_item.start_pos:cur_pos]
            if (not ca_text) or (ca_text in name):
                yield name
    
    def sieve_starting_with(self):
        text = self.editor.text() #[self.ca_start:self.editor.pos]
        cur_pos = self.editor.pos
#         for k in difflib.get_close_matches(text, self.items.keys(), n=100, cutoff=0.6):  
        for name, ca_item in self.items.items():
            ca_text = text[ca_item.start_pos:cur_pos]
            if (not ca_text) or (name.startswith(ca_text)):
                yield name

    def sieve_anywhere(self):
        text = self.editor.text() #[self.ca_start:self.editor.pos]
        cur_pos = self.editor.pos
#         for k in difflib.get_close_matches(text, self.items.keys(), n=100, cutoff=0.6):  
        for name, ca_item in self.items.items():
            ca_text = text[ca_item.start_pos:cur_pos]
            if (ca_text in name) and (not name.startswith(ca_text)):
                yield name


    
# app.register_global("content_assist", ContentAssist())
