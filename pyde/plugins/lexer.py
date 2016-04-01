from pyde.ddi import Dependency
from PyQt4.Qt import QFont
from PyQt4 import Qsci

class Lexer:
    mode_lexer_map = {
                      'ipython' : Qsci.QsciLexerPython
                      }
    def __init__(self, widget: Dependency('widget/*', lambda v: hasattr(v.view, 'mode'))):
        view = widget.view
        mode = view.mode
        if mode.name in self.mode_lexer_map:
            lexer_cls = self.mode_lexer_map[mode.name]
        else:
            lexer_name_possibilities = ["QsciLexer" + mode.name, "QsciLexer" + mode.name.title(), "QsciLexer" + mode.name.upper()]
            for lexer_name in lexer_name_possibilities:
                if hasattr(Qsci, lexer_name):
                    lexer_cls = getattr(Qsci, lexer_name, None)
                    break
            else:
                lexer_cls = None
        
        if lexer_cls is not None:    
            font = QFont()
            font.setFamily('DejaVu Sans Mono')
            font.setFixedPitch(True)
            font.setPointSize(10)
        
            lexer = lexer_cls(widget)
            lexer.setDefaultFont(font)
            widget.setLexer(lexer)

        
