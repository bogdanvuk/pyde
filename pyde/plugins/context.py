from PyQt4.QtCore import QObject, pyqtSlot
from pyde.ddi import Dependency
from PyQt4.QtGui import QWidget
from collections import OrderedDict

class URI(list):
    separator = '/'
    
    def __str__(self):
        return self.separator + self.separator.join(self)

class Context(object):
    def __init__(self, parent=None):
        self.parent = parent
#         if parent is not None:
#             self.parent.children[name] = self
        self.children = OrderedDict()
    
    def __str__(self):
        return '{0}: {1}-{2}: {3}'.format(self.name, self.start, self.stop, self.text)
    
    __repr__ = __str__
    
    def __iter__(self):
        return self.children.__iter__()
    
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

        self.visit_all_enter(node)
        ret = visitor(node)
        self.visit_all_exit(node)
        return ret
    
    def visit_all_enter(self, node):
        pass
    
    def visit_all_exit(self, node):
        pass

    def generic_visit(self, node):
        """Called if no explicit visitor function exists for a node."""
        for c in node.children:
            child = node.children[c]
            if isinstance(child, list):
                for elem in child:
                    self.visit(elem)
            else:
                self.visit(child)

class ContextVisitor(NodeVisitor):
 
    class FoundLeafException(Exception):
        pass
     
    def context_at(self, node, pos):
        self.context = URI()
        self.pos = pos
        try:
            self.visit(node)
        except self.FoundLeafException:
            pass
    
    def visit(self, node):
        if self.pos >= node.start and self.pos <= node.stop:
            if not node.children:
                raise self.FoundLeafException
            else:
                for c in node.children:
                    child = node.children[c]
                    self.context.append(c)
                    if isinstance(child, list):
                        for i,elem in enumerate(child):
                            self.context.append(i)
                            self.visit(elem)
                            self.context.pop()
                    else:
                        self.visit(child)
                    
                    self.context.pop()

#     def visit_all_enter(self, node):
#         """Visit a node."""
#         self.context.append(node)
#    
#         if not node.children:
#             if self.pos >= node.start and self.pos <= node.stop:
#                 raise self.FoundLeafException
     
#     def visit_all_exit(self, node):
#         self.context.pop()


class ContextProvider(QObject):
    
    def __init__(self, win : Dependency('win')):
        super().__init__()
        self.root = Context(parent=None)
        for v in win.views:
            self.add_view(v)
             
        win.view_added.connect(self.add_view)
        
        self.win = win

    @pyqtSlot(list, object)
    def update_context(self, uri, c):
        if isinstance(uri[-1], int):
            parent = self.context_at_uri(uri[:-2])
            parent[uri[-2]][uri[-1]] = c
        else:
            parent = self.context_at_uri(uri[:-1])
            parent[uri[-1]] = c
            
        c.parent = parent
        
    @pyqtSlot(QWidget)
    def add_view(self, view):
        self.root[view.name] = Context(self.root)
        self.root[view.name].view = view

    def get_active_view_context(self):
        active_view = self.win.active_view()
        if not active_view:
            return None
        
        active_view_name = active_view.name
        
        if active_view_name not in self.root:
            return None
        else:
            return self.root[active_view_name]

    def context_at_uri(self, uri):
        cur_node = self.root
        for p in uri:
            cur_node = cur_node[p]
        
        return cur_node    

    def active_uri(self):
        c = self.get_active_view_context()
        if c is None:
            return URI()
        else:
            if 'ast' in c:
                cv = ContextVisitor()
                if hasattr(c.view, 'pos'):
                    cv.context_at(c['ast'], c.view.pos)
                    
                return URI([c.view.name] + cv.context)
            else:
                return URI([c.view.name])
#             print(cv.context)
    
    def uri_at_pos(self, pos):
        c = self.get_active_view_context()
        if c is None:
            return URI()
        else:
            cv = ContextVisitor()
            cv.context_at(c, pos)
            return cv.context
#             print(cv.context)

    def del_view(self, view):
        pass