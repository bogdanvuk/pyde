from ddi.ddi import Dependency, ddic, Amendment
import pexpect
import sys

from PyQt5.Qsci import QsciScintilla
from pyde.editor import PydeEditor
from PyQt5.QtGui import QFont, QFontMetrics, QColor
from pyde.actions import switch_view
from PyQt5 import QtCore
import re
import os

class PyDbg:
    def __init__(self, widget: Dependency('widget/*', lambda w: hasattr(w.view, 'mode') and (w.view.mode.name == "python"))):
        widget.debug = self #self.__get__(self, widget.__class__)
        self.widget = widget
        
    def __call__(self):
        view = ddic['cls/view'](self.widget.view.parent, debug_file=self.widget.view.file_name)
        ddic.provide('view/', view)
        switch_view(view, self.widget.loc)

class PdbAsync(QtCore.QObject):

    response = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()

    def __init__(self, fn):
        super().__init__()
        self.fn = fn
        self.qthread = QtCore.QThread()
        self.moveToThread(self.qthread)

        self.p = pexpect.spawnu('pdb3 {}'.format(self.fn))
        self.p.setecho(False)
        self.p.expect('\(Pdb\)', timeout=1)
        
        self.finished.connect(self.qthread.quit)
        
        self.qthread.start()
        
    def cmd(self, text):
        try:
            self.p.sendline(text)
            self.p.expect('\(Pdb\)', timeout=1)
            self.response.emit(self.p.before)
        except pexpect.TIMEOUT:
            pass
        except pexpect.EOF:
            self.finished.emit()

class PyDbgInterpretEditor(PydeEditor):
    pdbrequest = QtCore.pyqtSignal(str)
    
    def __init__(self, view: Amendment('view/*', lambda v: all([hasattr(v, a) for a in ['mode', 'status_provider']]) and (v.mode.name == 'dbgpy') and (v.widget is None))): #, orig_editor=None):
        if view.widget is None:
            pass
        else:
            pass
        
        super().__init__(view)

        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)
        self.SendScintilla(QsciScintilla.SCI_SETVSCROLLBAR, 0)
        self.SendScintilla(QsciScintilla.SCI_AUTOCSETTYPESEPARATOR, 1)
        
        self.markerDefine(QsciScintilla.RightArrow,
            self.ARROW_MARKER_NUM)

        self.prompt_begin = 0
        self.focus_view = None
        self.interactive = False
        self.pdb = PdbAsync(self.view.debug_file)
        self.pdb.response.connect(self.pdbresp, type=QtCore.Qt.QueuedConnection)
        self.pdbrequest.connect(self.pdb.cmd, type=QtCore.Qt.QueuedConnection);
        self.set_dbg_pos_indic()
        
    @property
    def prompt_begin(self):
        return self._prompt_begin
    
    @prompt_begin.setter
    def prompt_begin(self, value):
        if hasattr(self, '_prompt_begin'):
            self.markerDeleteAll(self.ARROW_MARKER_NUM)
            
        self._prompt_begin = value
        self.markerAdd(self.lineIndexFromPosition(self._prompt_begin)[0], self.ARROW_MARKER_NUM)

    def cmd_range(self):
        return (self.prompt_begin, self.length())
    
    def cmd_text(self):
        return self.text()[self.prompt_begin:self.length()]

    def cancel(self):
        self.SendScintilla(QsciScintilla.SCI_DELETERANGE, self.prompt_begin, self.length() - self.prompt_begin)

    def pdbresp(self, text):
        self.pdbcmd_callback(text)
    
    def _output(self, text):
        self.insert(text)
        self.insert('\n')
        self.pos = self.length()
        self.prompt_begin = self.length()
        self.direct_cmd = False

    def _set_dbg_pos_indic(self, text):
        re_frame_source = r'\s?> ([^(]+)\((\d)\)(.+$)'
        re_cur_frame_source = r'^' + re_frame_source 
        m = re.search(re_cur_frame_source, text, flags=re.MULTILINE)
        if m:
            fn = m.groups()[0]
            line = int(m.groups()[1]) - 1
            v = self.view.parent.child_by_name(os.path.basename(fn))
            if v:
                v.widget.markerDeleteAll(v.widget.DBG_POS_MARKER_NUM)
                v.widget.markerAdd(line, v.widget.DBG_POS_MARKER_NUM)
                v.widget.SendScintilla(QsciScintilla.SCI_GOTOLINE, line)
                v.set_focus()

    def set_dbg_pos_indic(self):
        self.pdbcmd('w', self._set_dbg_pos_indic)

    def pdbcmd(self, cmd, callback):
        self.pdbcmd_callback = callback
        self.pdbrequest.emit(cmd)

    def debug_step(self):
        self.pdbcmd('n', self._set_dbg_pos_indic)

    def evaluate(self):
        cmd = self.cmd_text()
        self.insert('\n')
        self.direct_cmd = True
        self.pos = self.length()
        self.pdbcmd(cmd, self._output)

        
#         try:
#         self.p.send(cmd)
#         self.p.expect('(Pdb)')
#             
# 
#             ret = eval(cmd, self.globals, self.locals)
#             if ret is not None:
#                 ret_str = '\n' + str(ret) + '\n'
#             else:
#                 ret_str = '\n'
         
#         self.insert(self.p.before)
# #         except SyntaxError:
# #             exec(cmd, self.globals, self.locals)
# #             self.insert('\n')
# #         except:
# #             self.insert('\n{0}: {1}\n'.format(sys.exc_info()[0].__name__, sys.exc_info()[1]))
# 
#         self.pos = self.length()
#         self.prompt_begin = self.length()
