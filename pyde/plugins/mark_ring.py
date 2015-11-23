from pyde.application import app
from collections import namedtuple
from collections import deque

Mark = namedtuple('Mark', ['editor', 'line', 'pos'])

class MarkAction(object):
    
    class MarkRing(deque):

        def prev(self):
            super().rotate()
            return self[-1]
            
        def cur(self):
            return self[-1]

    class MarkStack(list):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.pos = -1
        
        def append(self, obj):
            while(self.pos < len(self) - 1):
                super().pop()
            
            super().append(obj)
            self.pos = len(self) - 1
            
        def prev(self):
            mark = self[self.pos]
            self.pos -= 1
            return mark
        
        def next(self):
            mark = self[self.pos + 1]
            self.pos += 1
            return mark
            
        def pop(self):
            super().pop()
            self.pos -= 1
    
        def cur(self):
            return self[self.pos]
   
    def __init__(self):
        self.sets = {}
        self.sets['global'] = MarkAction.MarkStack()
        self.sets['global'].editor = None
    
    def add_set(self, name, editor=None, set_class = MarkAction.MarkRing):
        self.sets[name] = set_class()
        self.sets[name].editor = editor
    
    def new(self, set_name='global'):
        editor = app.active_widget()
        if (self.sets[set_name].editor is None) or (self.sets[set_name].editor == editor): 
            line, pos = editor.getCursorPosition()
            self.sets[set_name].append(Mark(editor, line, pos))
            print(self.sets[set_name])
            print(self.sets[set_name].pos)
            print("ADD")
    
    def prev(self, ring='global'):
        try:
            mark = self.sets[ring].prev()
            mark.editor.setCursorPosition(mark.line, mark.pos)
            mark.editor.setFocus()
            print(self.sets[ring])
            print(self.sets[ring].pos)
            print("PREV")
        except IndexError:
            pass
        
    def next(self, set_name='global'):
        try:
            mark = self.sets[set_name].next()
            mark.editor.setCursorPosition(mark.line, mark.pos)
            mark.editor.setFocus()
            print(self.sets[set_name])
            print(self.sets[set_name].pos)
            print("NEXT")
        except IndexError:
            pass
        
    
    def pop(self, set_name='global'):
        mark = self.sets[set_name].pop()
        print(self.sets[set_name])
        print(self.sets[set_name].pos)
        print("POP")
        return mark
    
    def cur(self, set_name='global'):
        return self.sets[set_name].cur()
        
app.register_global("mark", MarkAction())