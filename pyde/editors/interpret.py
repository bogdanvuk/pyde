#-------------------------------------------------------------------------
# qsci_simple_pythoneditor.pyw
#
# QScintilla sample with PyQt
#
# Eli Bendersky (eliben@gmail.com)
# This code is in the public domain
#-------------------------------------------------------------------------
import sys
from io import StringIO
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import QsciScintilla, QsciLexerPython
import pyde
from pyde.application import app
from PyQt4 import QtGui, Qsci
from pyde.pyde_widget import PydeWidget
from pyde.editor import PydeEditor
from inspect import signature

class PyInerpretEditor(PydeEditor):
    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None):
        super(PyInerpretEditor, self).__init__(parent)

        # Set the default font
        font = QFont()
        font.setFamily('DejaVu Sans Mono')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        fontmetrics = QFontMetrics(font)

        # Brace matching: enable for a brace immediately before or after
        # the current position
        #
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))

        # Set Python lexer
        # Set style for Python comments (style number 1) to a fixed-width
        # courier.
        #
#         self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'DejaVu Sans Mono'.encode())
        

        # Don't want to see the horizontal scrollbar at all
        # Use raw message to Scintilla here (all messages are documented
        # here: http://www.scintilla.org/ScintillaDoc.html)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)
        self.SendScintilla(QsciScintilla.SCI_SETVSCROLLBAR, 0)
        
        self.setMinimumSize(fontmetrics.width("00000"), fontmetrics.height()+4)
        
#         self.globals = {}
#         self.globals['app'] = pyde.application.app
#         from pyde import actions
#         
#         for a in dir(actions):
#             if not a.startswith('__'):
#                 obj = getattr(actions, a)
#                 if callable(obj):
#                     self.globals[a] = obj
         
        self.locals = {}
        self.prompt_begin_line = 0
        
        lexer = QsciLexerPython(self)
        
#         self.c = QtGui.QCompleter(['"helaaa"', 'helabb', 'helccc', 'world'])
#         self.c.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
#         self.c.setWidget(self)
# 
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionShowSingle(True)
        self.setAutoCompletionSource(Qsci.QsciScintilla.AcsAPIs)
        
        lexer.setDefaultFont(font)
        
        self.setLexer(lexer)
        self.content_assist_list = Qsci.QsciAPIs(self.lexer())
        self.autoCompleteFromAll()
         
        self.prepare_assist_globals()
        
        self.SCN_AUTOCSELECTION.connect(self.autoc_end)

    def evaluate(self):
        if self.SendScintilla(QsciScintilla.SCI_AUTOCACTIVE):
            self.SendScintilla(QsciScintilla.SCI_AUTOCCOMPLETE)
        else:
            current_line = self.getCursorPosition()[0]
            text_lines = []
            for i in range(self.prompt_begin_line,current_line+1):
                text_lines.append(self.text(i))
             
            cmd = '\n'.join(text_lines)
            
            buffer = StringIO()
            sys.stdout = buffer
            
            try:
                 
                ret = eval(cmd, app.globals, self.locals)
                if ret is not None:
                    ret_str = '\n' + str(ret) + '\n'
                else:
                    ret_str = '\n'
                     
                stdout_text = buffer.getvalue()
                if stdout_text:
                    ret_str += stdout_text
                 
                self.insert(ret_str)
            except SyntaxError:
                exec(cmd, app.globals, self.locals)
                self.insert('\n')
            except:
                self.insert('\n{0}: {1}\n'.format(sys.exc_info()[0].__name__, sys.exc_info()[1]))
            
            sys.stdout = sys.__stdout__
            self.setCursorPosition(self.lines(), 0)
            self.prompt_begin_line = self.lines() - 1

    def autoc_end(self):
        print("ENDED!")

    def prepare_assist_globals(self):
        for name, obj in app.globals.items():
            try:
                sig = signature(obj)
            except:
                sig = ''
                
            self.content_assist_list.add(name + str(sig))

        self.content_assist_list.add('backward/bla/abla')
        self.content_assist_list.add('backward_chab')
        self.content_assist_list.add('backward_chbb')
            
        self.content_assist_list.prepare()
    
    def content_assist(self):
#        self.SendScintilla(QsciScintilla.SCI_AUTOCSHOW, 4, '"helaaa" helabb helccc world'.encode())
#         self.c.complete()
        self.prepare_assist_globals()
        self.autoCompleteFromAll()
