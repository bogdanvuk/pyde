from pyde.ddi import Dependency
from PyQt4.QtCore import QObject
from pyde.plugins.parser import NodeVisitor
from pyde.plugins.ca_interpreter import get_obj_for_ctx
from inspect import getfullargspec
from pyde.actions import FuncArgContentAssist

class ArglistVisitor(NodeVisitor):
    def __init__(self, editor):
        self.editor = editor
        self.ca_nodes = []
        
    def visit_arglist(self, node):
        func = get_obj_for_ctx(node.parent['calee'], self.editor)
        args, _, _, _, kwonlyargs, _, annotations = getfullargspec(func)
        
        for annot_arg, annot in annotations.items():
            if issubclass(annot, FuncArgContentAssist):
                if annot.language == 'linpath':
                    for i, arg in enumerate(args):
                        if arg == annot_arg:
                            self.ca_nodes.append(node['arg'][i])
        pass

class InterpretPathParser(QObject):
    def __init__(self, linpath_parser_cls : Dependency('parser/cls/linpath'), python_ast_manager : Dependency('editor_ast_manager/python/inst/')):
        super().__init__()
        self.parser = linpath_parser_cls()
        self.editor = python_ast_manager.editor 
        python_ast_manager.tree_modified.connect(self.python_ast_changed)
        
    def python_ast_changed(self, tree):
        v = ArglistVisitor(self.editor)
        v.visit(tree)
        for n in v.ca_nodes:
            if 'value' in n:
                val = n['value']
            
            if val.type == 'STRING_LITERAL':
                val['path'] = self.parser.parse(self.editor.text(), (val.slice.start+1, val.slice.stop-1))
                
        pass