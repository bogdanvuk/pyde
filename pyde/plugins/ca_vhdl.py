from PyQt4.QtCore import QObject, pyqtSignal, Qt
from pyde.ddi import Dependency
from pyde.plugins.templating import TemplFunc
from collections import namedtuple
from pyde.plugins.parser import parser_node_child_by_feature

Completion = namedtuple('Completion', 'template start_pos')

class CompleteCommand:
    
    def complete_expression_value(self, editor, node, feature, parse_node):
        for name,_ in editor.view.ast.parser.iter_index_by_type(['interface_port_declaration']):
            self.acceptor[name] = Completion(name, parse_node.slice.start) #node.value._parse_node.slice.start)
#         
        pass


class VhdlContentAssist(QObject):
    
    read_ast = pyqtSignal(object)
    complete_sig = pyqtSignal(object)
    
    def __init__(self, 
                 view : Dependency('view/', lambda e: e.mode.name == "vhdl"),
                 ca : Dependency('content_assist'),
                 win : Dependency('win')):
        super().__init__()
        self.ca = ca
        self.win = win
        self.view = view
        self.complete_cmd = CompleteCommand()
        if self.ca.thread() != self.thread():
            connection_type=Qt.BlockingQueuedConnection
        else:
            connection_type=Qt.AutoConnection

        self.ca.complete.connect(self.complete, type=connection_type)
     
    def complete(self, acceptor):
        if self.win.active_view() == self.view:
            self.complete_cmd.acceptor = acceptor
            
            self.complete_sig.connect(self.view.ast.completion_suggestions, type=Qt.BlockingQueuedConnection)
            self.complete_sig.emit(self.complete_cmd)
            self.complete_sig.disconnect()
