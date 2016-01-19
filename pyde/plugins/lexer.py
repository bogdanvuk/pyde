from pyde.ddi import Dependency
from PyQt4.Qsci import QsciLexerPython
from PyQt4.Qt import QFont

class Lexer:
    def __init__(self, mode : Dependency('mode/inst/')):
        font = QFont()
        font.setFamily('DejaVu Sans Mono')
        font.setFixedPitch(True)
        font.setPointSize(10)

        lexer = QsciLexerPython(mode.editor.widget)
        lexer.setDefaultFont(font)
        mode.editor.widget.setLexer(lexer)

        
