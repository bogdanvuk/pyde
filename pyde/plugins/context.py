from PyQt4.QtCore import QObject, pyqtSlot
from pyde.ddi import Dependency
from PyQt4.QtGui import QWidget

class Context(object):
    def __init__(self, name=None, parent=None):
        self.parent = parent
        if parent is not None:
            self.parent.children[name] = self
        self.name = name
        self.children = {}
    
#     def find(self, path):
#         
    
    def __getitem__(self, item):
        return self.children[item]

    def __setitem__(self, item, val):
        self.children[item] = val

class NodeVisitor(object):

    def visit(self, node):
        """Visit a node."""
        if node.name:
            method = 'visit_' + node.name
            visitor = getattr(self, method, self.generic_visit)
        else:
            visitor = self.generic_visit
        
        return visitor(node)
    
    def visit_all_enter(self, node):
        pass
    
    def visit_all_exit(self, node):
        pass

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        for c in node.children:
            child = node.children[c]
            self.visit_all_enter(child)
            self.visit(child)
            self.visit_all_exit(child)

class ContextVisitor(NodeVisitor):
 
    class FoundLeafException(Exception):
        pass
     
    def context_at(self, node, pos):
        self.context = []
        self.pos = pos
        try:
            self.visit(node)
        except self.FoundLeafException:
            pass
     
    def visit_all_enter(self, node):
        """Visit a node."""
        self.context.append(node)
   
        if not node.children:
            if self.pos >= node.start and self.pos <= node.stop:
                raise self.FoundLeafException
     
    def visit_all_exit(self, node):
        self.context.pop()


class ContextProvider(QObject):
    
    def __init__(self, win : Dependency('win')):
        super().__init__()
        self.root = Context('root', parent=None)
        for v in win.views:
            self.add_view(v)
            
        win.view_added.connect(self.add_view)
        
        self.win = win

    @pyqtSlot(list, object)
    def update_context(self, root_path, tree):
        cur_node = self.root
        for p in root_path[:-1]:
            cur_node = cur_node[p]
        
#         del cur_node[root_path[-1]]
        cur_node[root_path[-1]] = tree
        
    @pyqtSlot(QWidget)
    def add_view(self, view):
        Context(view.name, self.root)
    
    def context_at_pos(self, pos):
        cv = ContextVisitor()
        active_view_name = self.win.active_view().name
        cv.context_at(self.root[active_view_name], pos)
        print(cv.context)

    def del_view(self, view):
        pass