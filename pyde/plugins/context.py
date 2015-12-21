from PyQt4.QtCore import QObject, pyqtSlot
from pyde.ddi import Dependency
from PyQt4.QtGui import QWidget
from collections import OrderedDict

uri_separator = '/'

class SequenceMatchError(Exception):
    pass

class BoundedSlice:
    def __init__(self, seq, start, stop=None):
        self.seq = seq
        
        if stop is None:
            stop = start
        
        self.stop = stop
        self.start = start
  
    def contains(self, subslice):
        if self.seq != subslice.seq:
            raise SequenceMatchError
        else:
            return (self.start <= subslice.start) and (self.stop > subslice.stop)
    
    def eval(self):
        return self.seq[self.start:self.stop]

class RootContextSlice:
    def __init__(self, features):
        self.features = features 
    
    def contains(self, subslice):
        if subslice.seq is not None:
            raise SequenceMatchError
        else:
            return subslice.start in self.features

def uri2str(self, separator = '/'):
    return separator + separator.join(map(str, self))

class Context(object):
    type = 'default'
    
    def __init__(self, parent=None):
        self.parent = parent
#         if parent is not None:
#             self.parent.features[name] = self
        self.features = {} #OrderedDict()
    
    def __str__(self):
        return uri2str(self.uri)
#         return '{0}: {1}-{2}: {3}'.format(self.name, self.start, self.stop, self.text)
    
    __repr__ = __str__
    
    @property
    def uri(self):
        if self.parent:
            uri = self.parent.uri + list(self.get_feature_in_parent())
        else:
            uri = []
            
        return uri
    
    def get_feature_in_parent(self):
        return self.parent.get_feature_for_child(self)

    def get_feature_for_child(self, child):
        for name, feature in self.features.items():
            if isinstance(feature, list):
                for i, cl in enumerate(feature):
                    if cl == child:
                        return (name, i)
            else:
                if feature == child:
                    return (name,)
        return None

    
    def __iter__(self):
        return self.features.__iter__()
    
    def __getitem__(self, item):
        return self.features[item]

    def __setitem__(self, item, val):
        self.features[item] = val

class RootContext(Context):
    type = 'root'
    def __init__(self):
        super().__init__(None)
        self.slice = RootContextSlice(self.features)

class ViewContext(Context):
    type = 'view'
        
    def __init__(self, view, parent=None):
        self.view = view
        super().__init__(parent)
    
    @property
    def slice(self):
        return BoundedSlice(self.view, self.view.active_range()[0], self.view.active_range()[1] + 1)
      
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
        for c in node.features:
            child = node.features[c]
            if isinstance(child, list):
                for elem in child:
                    self.visit(elem)
            else:
                self.visit(child)

class ContextVisitor(NodeVisitor):

    class FoundLeafException(Exception):
        pass

    def __init__(self, root):
        self.root = root
 
    def context_at(self, posseq):
        self.context = None
        self.posseq = posseq
        self.cur_pos = 0
        self.pos_contained = [0]*len(posseq)
        try:
            self.visit(self.root)
        except self.FoundLeafException:
            return self.context
        
        return None
    
    def visit(self, node):
        contains = False
        contains_checked = False
        while not contains_checked:
            try:
                contains = node.slice.contains(self.posseq[self.cur_pos])
                contains_checked = True
            except SequenceMatchError:
                if self.pos_contained[self.cur_pos]:
                    self.cur_pos += 1
                    self.pos_contained[self.cur_pos] = 0
                    if self.cur_pos == len(self.posseq):
                        raise self.FoundLeafException
                else:
                    contains_checked = True
                
        if contains:
            self.pos_contained[self.cur_pos] += 1
            if not node.features:
                self.context = node
                raise self.FoundLeafException
            else:
                for c in node.features:
                    child = node.features[c]
                    if isinstance(child, list):
                        for i,elem in enumerate(child):
                            self.visit(elem)
                    else:
                        self.visit(child)
                        
        if self.pos_contained[self.cur_pos]:
            self.pos_contained[self.cur_pos] -= 1
        else:
            self.cur_pos -= 1

#     def visit_all_enter(self, node):
#         """Visit a node."""
#         self.context.append(node)
#    
#         if not node.features:
#             if self.pos >= node.start and self.pos <= node.stop:
#                 raise self.FoundLeafException
     
#     def visit_all_exit(self, node):
#         self.context.pop()


class ContextProvider(QObject):
    
    def __init__(self, win : Dependency('win')):
        super().__init__()
        self.root = RootContext()
        
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
        self.root[view.name] = ViewContext(view, self.root)

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

    def active_context(self):
        active_view = self.win.active_view()

        if not active_view:
            return self.root
        else:
            view_name = active_view.name
#             try:
            cv = ContextVisitor(self.root)
            return cv.context_at([BoundedSlice(None, view_name), 
                                  BoundedSlice(active_view,active_view.pos)])
#             except:
#                 return self.root[view_name]
    
    def context_at_pos(self, pos):
        c = self.get_active_view_context()
        if c is None:
            return self.root
        else:
            cv = ContextVisitor(self.root)
            return cv.context_at(c, pos)
#             print(cv.context)

    def del_view(self, view):
        pass