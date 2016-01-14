from pyde.ddi import Dependency

class InterpretPathParser:
    def __init__(self, linpath_parser_cls : Dependency('parser/cls/linpath'), python_parser : Dependency('parser/inst/')):
        self.parser = linpath_parser_cls()