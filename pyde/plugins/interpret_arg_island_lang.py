from pyde.ddi import Dependency
from PyQt4.QtCore import QObject, pyqtSlot
from pyde.plugins.parser import NodeVisitor
from pyde.plugins.ca_interpreter import get_obj_for_ctx
from inspect import getfullargspec
from pyde.actions import FuncArgContentAssist
from PyQt4 import QtCore

class ArglistVisitor(NodeVisitor):
    def __init__(self, editor, language):
        self.editor = editor
        self.ca_nodes = []
        self.language = language
        
    def visit_arglist(self, node):
        func = get_obj_for_ctx(node.parent.callable, self.editor)
        try:
            args, _, _, _, kwonlyargs, _, annotations = getfullargspec(func)
        except TypeError:
            return
        
        for annot_arg, annot in annotations.items():
            if issubclass(annot, FuncArgContentAssist):
                if annot.language == self.language:
                    for i, arg in enumerate(args):
                        if arg == annot_arg:
                            self.ca_nodes.append(node.arg[i])
        pass

def IslandLanguageParserFactory(language):
    class IslandLanguageParser(QObject):
        def __init__(self, parser_cls : Dependency('parser/cls/' + language), python_ast_manager : Dependency('editor_ast_manager/inst/', lambda e: e.mode.name == "ipython")):
            super().__init__()
            self.parser = parser_cls()
            self.editor = python_ast_manager.editor
            self.islands = []
            self.language = language
            
            self.moveToThread(python_ast_manager.thread())
            if python_ast_manager.thread() != self.thread():
                connection_type=QtCore.Qt.BlockingQueuedConnection
            else:
                connection_type=QtCore.Qt.AutoConnection
    #         connection_type=QtCore.Qt.AutoConnection
    #         connection_type=QtCore.Qt.BlockingQueuedConnection
                
            python_ast_manager.tree_modified.connect(self.python_ast_changed, type=connection_type)
            python_ast_manager.suggestions_created.connect(self.completion_suggestions, type=connection_type)
        
        def completion_suggestions(self, suggestions, text, text_range):
            carret_index = text_range[1]
            for island in self.islands:
                if (island[1].slice.contains(carret_index)) or (island[1].slice.stop == carret_index):
                    suggestions.extend(self.parser.completion_suggestions(text, [island[1].slice.start, carret_index]))
    #     @pyqtSlot(object)
        def python_ast_changed(self, tree):
            v = ArglistVisitor(self.editor, self.language)
            v.visit(tree)
            self.islands = []
            tokens = tree._parse_node.token
            for n in v.ca_nodes:
                self.parser.parse(self.editor.text(), (n.parse_node.slice.start+1, n.parse_node.slice.stop-1))
                self.islands.append((self.parser.tokens, self.parser.parse_tree, self.parser.semantic_tree))
                tokens[n.parse_node.start].island_grammar_root = self.parser.parse_tree 
                    
            pass

    return IslandLanguageParser