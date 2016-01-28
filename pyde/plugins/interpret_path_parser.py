from pyde.ddi import Dependency
from PyQt4.QtCore import QObject, pyqtSlot
from pyde.plugins.parser import NodeVisitor
from pyde.plugins.ca_interpreter import get_obj_for_ctx
from inspect import getfullargspec
from pyde.actions import FuncArgContentAssist
from PyQt4 import QtCore

class ArglistVisitor(NodeVisitor):
    def __init__(self, editor):
        self.editor = editor
        self.ca_nodes = []
        
    def visit_arglist(self, node):
        func = get_obj_for_ctx(node.parent.callable, self.editor)
        try:
            args, _, _, _, kwonlyargs, _, annotations = getfullargspec(func)
        except TypeError:
            return
        
        for annot_arg, annot in annotations.items():
            if issubclass(annot, FuncArgContentAssist):
                if annot.language == 'linpath':
                    for i, arg in enumerate(args):
                        if arg == annot_arg:
                            self.ca_nodes.append(node.arg[i])
        pass

class InterpretPathParser(QObject):
    def __init__(self, linpath_parser_cls : Dependency('parser/cls/linpath'), python_ast_manager : Dependency('editor_ast_manager/inst/', lambda e: e.mode.name == "ipython")):
        super().__init__()
        self.parser = linpath_parser_cls()
        self.editor = python_ast_manager.editor
        
        self.moveToThread(python_ast_manager.thread())
        if python_ast_manager.thread() != self.thread():
            connection_type=QtCore.Qt.BlockingQueuedConnection
        else:
            connection_type=QtCore.Qt.AutoConnection
#         connection_type=QtCore.Qt.AutoConnection
#         connection_type=QtCore.Qt.BlockingQueuedConnection
            
        python_ast_manager.tree_modified.connect(self.python_ast_changed, type=connection_type)
    
#     @pyqtSlot(object)
    def python_ast_changed(self, tree):
        print('python_ast_changed')
        v = ArglistVisitor(self.editor)
        v.visit(tree)
        for n in v.ca_nodes:
            n.value = self.parser.parse(self.editor.text(), (n.parse_node.slice.start+1, n.parse_node.slice.stop-1))
            n.value.parent = n 
                
        pass