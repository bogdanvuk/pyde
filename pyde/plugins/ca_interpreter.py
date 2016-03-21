from PyQt4.QtCore import QObject
from pyde.ddi import Dependency
#from pyde.plugins.parser import ContextVisitor, NodeVisitor
from pyde.plugins.templating import TemplFunc
from inspect import getfullargspec
import os
from PyQt4 import QtCore
from collections import namedtuple

def get_ctx_text(ctx, editor):
    return editor.text()[ctx.slice.start:ctx.slice.stop]
    
def get_obj_for_ctx(ctx, editor):
    return eval(ctx._parse_node.text, editor.globals, editor.locals)

Completion = namedtuple('Completion', 'template start_pos')

class CompleteCommand:
    
    def accept_global(self, editor, parse_node):
        if parse_node is not None:
            start = parse_node.slice.start
        else:
            start = editor.anchor
        
        for g in editor.globals:
            if callable(editor.globals[g]):
                self.acceptor[g] = Completion(TemplFunc(editor.globals[g]), start)
            else:
                self.acceptor[g] = Completion(g, start)
            
            for l in editor.locals:
                self.acceptor[l] = Completion(l, start)

    
    def complete_main_path(self, editor, node, feature, parse_node):
        pass
    
    def complete_part_name(self, editor, node, feature, parse_node):
        pass
    
    def complete_view_name_value(self, editor, node, feature, parse_node):
        if parse_node is not None:
            start = parse_node.slice.start
        else:
            start = editor.anchor
                
        for k in editor.view.parent.child:
            if k in self.acceptor:
                pass
            else:
                self.acceptor[k.name] = Completion(k.name, start)
    
    def complete_path_part(self, editor, node, feature, parse_node):
        parts = [p.parse_node.text for p in node.part][:feature[1]]
        path = '/'
        if parts:
            path += os.path.join(*parts)
#         if feature[1] == len(node.part):
#             path = node.parse_node.text[:-1]
#             
        for f in os.listdir(path):
            if os.path.isdir(os.path.join(path, f)):
                f += '/'
            
            if parse_node is not None:
                start = parse_node.slice.start
            else:
                start = editor.anchor
                
            self.acceptor[f] = Completion(f, start)

        pass
    
    def complete_expr(self, editor, node, parse_node):
        self.accept_global(editor, parse_node)
    
    def complete_expr_attr(self, editor, node, feature, parse_node):
        obj_text = node.object.parse_node.text
        obj = eval(obj_text, editor.globals, editor.locals)
        if parse_node is not None:
            start = parse_node.slice.start
        else:
            start = editor.pos

        for d in dir(obj):
            self.acceptor[d] = Completion(d, start)
        
        pass

class PyInterpretContentAssist(QObject):
    
    read_ast = QtCore.pyqtSignal(object)
    complete_sig = QtCore.pyqtSignal(object)
    
    def __init__(self, 
                 view : Dependency('view/', lambda e: e.mode.name == "ipython"),
                 ca : Dependency('content_assist'),
                 win : Dependency('win')):
        super().__init__()
        self.ca = ca
        self.win = win
        self.view = view
        self.complete_cmd = CompleteCommand()
        if self.ca.thread() != self.thread():
            connection_type=QtCore.Qt.BlockingQueuedConnection
        else:
            connection_type=QtCore.Qt.AutoConnection

        self.ca.complete.connect(self.complete, type=connection_type)
     
    def complete(self, acceptor):
        if self.win.active_view() == self.view:
            self.complete_cmd.acceptor = acceptor
            
            self.complete_sig.connect(self.view.ast.completion_suggestions, type=QtCore.Qt.BlockingQueuedConnection)
            self.complete_sig.emit(self.complete_cmd)
            self.complete_sig.disconnect()
