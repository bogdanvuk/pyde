from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject, Qt
from pyde.ddi import Amendment

def test(win):
    return win.widget is not None

class Layout(QObject):
    
#    def __init__(self, win: Amendment('win', test)):
    def __init__(self, win : Amendment('win', lambda w: w.widget is not None)):
        super().__init__()
        win.layout = self
        
        self.centralwidget = QtGui.QWidget(win.widget)
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        win.widget.setCentralWidget(self.centralwidget)

        self.widget = QtGui.QSplitter(Qt.Vertical)
        self.widget.addWidget(QtGui.QStackedWidget())
#         self.widget = QtGui.QStackedWidget()
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        
        self.recent = []
        self.layout = []
        self.win = win
                
    def setup(self, layout):
        pass
    
    def _get_layout_rec(self, layout, loc):
        cur = loc[0]
        rest = loc[1:]
        if rest:
            return self._get_layout_rec(layout[cur], rest)
        else:
            return layout[cur]
    
    def get_layout(self, loc):
        return self._get_layout_rec(self.layout, loc)
    
    def get_widget(self, loc):
        w = self.widget
        for l in loc:
            w = w.widget(l)
            
        return w

    def place(self, view, loc=[0]):
        w = self.get_widget(loc[:-1])
        place_layout = self.get_layout(loc)
        view.last_location = loc
        place_layout.clear()
        place_layout.append(view)
        w.widget(loc[-1]).insertWidget(0, view.widget)
        w.widget(loc[-1]).setCurrentWidget(view.widget)
    
    def split(self, loc, orientation=Qt.Vertical, ratio=(1,1)):
        if loc:
            parent_splitter = self.get_widget(loc[:-1])
            stacked = parent_splitter.widget(loc[-1])
            child_splitter = QtGui.QSplitter(orientation)
            parent_splitter.insertWidget(loc[-1], child_splitter)
            child_splitter.addWidget(stacked)
            child_splitter.addWidget(QtGui.QStackedWidget())
            
            split_layout = self.get_layout(loc)
            split_view = split_layout[0]
            split_layout.clear()
            split_layout.extend([[split_view], []])
            
            clone = split_view.clone()
            self.place(clone, loc + [1])
            
        else:
            child_splitter = self.widget
            child_splitter.setOrientation(orientation)
            child_splitter.addWidget(QtGui.QStackedWidget())
            self.layout = [[], []]
            
        for i in range(2):
            child_splitter.setStretchFactor(i, ratio[i])
        
#         
#         w.setOrientation(orientation)
#         w.addWidget = QtGui.QStackedWidget()
#         
#         s = QtGui.QSplitter(Qt.Horizontal)
#         w.addWidget(s)
#         w = QtGui.QStackedWidget()
#         s.addWidget(w)
        
        
    
class FrameWidget(QtGui.QSplitter):
    
    def __init__(self, layout=None, parent=None):
        if layout is None:
            orientation = QtCore.Qt.Vertical
        else:
            orientation = layout.orientation  
        
        QtGui.QSplitter.__init__(self, orientation, parent)

        if layout is not None:
            self.set_layout(layout)

    def set_layout(self, layout):
        self.remove_layout()
        self.setOrientation(layout.orientation)
        self.layout = layout
        self.frames = [None]*len(layout.children)
        self.assigned_views = [None]*len(layout.children)
        for i,c in enumerate(layout.children):
            if hasattr(c.layout, 'children'):
                child_frame = PydeFrame(c, self)
                self.addWidget(child_frame)
                self.frames[i] = child_frame
            else:
                self.addWidget(QtGui.QStackedWidget(self))
                
            self.setStretchFactor(i,c.stretch)
                
    def remove_layout(self):
        for i in range(self.count()):
            self.widget(i).hide()

    def add_view(self, view, location):
        loc = location[0]
        location = location[1:]
        if location:
            self.widget.add_view(view, location)
        elif self.assigned_views[loc] != view:
            self.assigned_views[loc] = view
            self.widget(loc).insertWidget(0, view.widget)
            self.widget(loc).setCurrentWidget(view.widget)
    
    
    def _dump_config_rec(self, layout):
        
        child_config = []
        for c in layout.children:
            if hasattr(c.layout, 'children'):
                ret = self._dump_config_rec(c.layout)
            else:
                ret = 'None'
                
            child_config.append('ChildLayout({},{})'.format(c.stretch, ret))

        orientation = ['Qt.Vertical', 'Qt.Vertical'][layout.orientation - 1]
        return 'Layout({}, [{}])'.format(orientation, ','.join(child_config))
    
    def dump_config(self, var_name):
        config = []
        config.append('from PyQt4.QtCore import Qt')
        config.append('from pyde.pyde_frame import ChildLayout, Layout')
        config.append('{}.set_layout({})'.format(var_name, self._dump_config_rec(self.layout)))
        return '\n'.join(config)
