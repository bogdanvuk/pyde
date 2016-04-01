from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QObject, Qt, QSize
from pyde.ddi import Amendment
from PyQt5.QtWidgets import QSizePolicy

def test(win):
    return win.widget is not None

class Layout(QObject):
    
#    def __init__(self, win: Amendment('win', test)):
    def __init__(self, win : Amendment('win', lambda w: w.widget is not None)):
        super().__init__()
        win.layout = self
        
        self.centralwidget = QtWidgets.QWidget(win.widget)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        win.widget.setCentralWidget(self.centralwidget)

        self.widget = QtWidgets.QSplitter(Qt.Vertical)
        self.widget.addWidget(QtWidgets.QStackedWidget())
#         self.widget = QtWidgets.QStackedWidget()
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        
        self.recent = []
        self.layout = []
        self.win = win
                
    def setup(self, layout):
        pass
    
    def _get_layout_rec(self, layout, loc):
        if loc:
            cur = loc[0]
            rest = loc[1:]
            if rest:
                return self._get_layout_rec(layout[cur], rest)
            else:
                return layout[cur]
        else:
            return layout
    
    def get_layout(self, loc):
        return self._get_layout_rec(self.layout, loc)
    
    def get_widget(self, loc):
        w = self.widget
        for l in loc:
            w = w.widget(l)
            
        return w
# 
#     def _search_locs_rec(self, layout, loc):
#         if len(layout) == 2:
#             for i in range(2):
#                 yield from self._search_locs_rec(layout[i], loc + [i])
#         elif len(layout) == 1:
#             yield (loc, layout[0])
#             
#     def search_locs(self, loc=[]):
#         layout = self.get_layout(loc)
#         yield from self._search_locs_rec(layout, loc)

    def _search_locs_rec(self, widget, loc):
        if isinstance(widget, QtWidgets.QSplitter):
            for i in range(2):
                yield from self._search_locs_rec(widget.widget(i), loc + [i])
        elif isinstance(widget, QtWidgets.QStackedWidget):
            yield (loc, widget.widget(0))
            
    def search_locs(self, loc=[]):
        widget = self.get_widget(loc)
        yield from self._search_locs_rec(widget, loc)
        
    def _iter_layout_rec(self, widget, loc):
        yield (loc, widget)
        if isinstance(widget, QtWidgets.QSplitter):
            for i in range(2):
                yield from self._iter_layout_rec(widget.widget(i), loc + [i])
        elif isinstance(widget, QtWidgets.QStackedWidget):
            yield (loc, widget.widget(0))
            
    def iter_layout(self, loc=[]):
        widget = self.get_widget(loc)
        yield from self._iter_layout_rec(widget, loc)

    def place(self, view, loc=[0]):
        
#         place_layout = self.get_layout(loc)
# #         view.last_location = loc
#         place_layout.clear()
#         place_layout.append(view)
        
        splitter = self.get_widget(loc[:-1])
        stack = splitter.widget(loc[-1])
        cur_widget = stack.currentWidget()
        if cur_widget:
            stack.removeWidget(cur_widget)
            cur_widget.loc = None
            cur_widget.last_loc = loc 
        
        if getattr(view.widget, 'loc', None):
            widget = view.clone_widget()
        else:
            widget = view.widget
            
        stack.insertWidget(0, widget)
        stack.setCurrentWidget(widget)
        widget.loc = loc
        if not hasattr(widget, 'last_loc'):
            widget.last_loc = loc
        
        widget.show()
        widget.setFocus()
    
    def split(self, loc, orientation=Qt.Vertical, ratio=(1,1)):
        if loc:
            parent_splitter = self.get_widget(loc[:-1])
            stacked = parent_splitter.widget(loc[-1])
            sizes = parent_splitter.sizes()

            child_splitter = QtWidgets.QSplitter(orientation)
            child_splitter.setSizePolicy(stacked.sizePolicy())
            child_splitter.addWidget(stacked)
                
            child_splitter.addWidget(QtWidgets.QStackedWidget())
            
            parent_splitter.insertWidget(loc[-1], child_splitter)

#             split_layout = self.get_layout(loc)
#             split_view = split_layout[0]
#             split_layout.clear()
#             split_layout.extend([[split_view], []])
            if stacked.count():
                stacked.widget(0).loc = loc + [0]
                self.place(stacked.widget(0).view, loc + [1])
                stacked.widget(0).setFocus()
            
            parent_splitter.setSizes(sizes)
            
        else:
            child_splitter = self.widget
            child_splitter.setOrientation(orientation)
            child_splitter.addWidget(QtWidgets.QStackedWidget())
            self.layout = [[], []]
            
        if orientation == Qt.Horizontal:
            size0 = child_splitter.width()*ratio[0]/(sum(ratio))
            child_splitter.setSizes([size0, child_splitter.width() - size0])
        else:
            size0 = child_splitter.height()*ratio[0]/(sum(ratio))
            child_splitter.setSizes([size0, child_splitter.height() - size0])

#         for i in range(2):
#             child_splitter.setStretchFactor(i, ratio[i])
    def merge(self, loc):
        parent_splitter = self.get_widget(loc[:-2])
        splitter = parent_splitter.widget(loc[-2])
        stacked = splitter.widget(loc[-1])
        
        sizes = parent_splitter.sizes()
        
        parent_splitter.insertWidget(loc[-2], stacked)
        splitter.hide()
        if loc[-2] == 0:
            parent_splitter.insertWidget(1, parent_splitter.widget(2))
        
        stacked.widget(0).loc = loc[:-1]

#         self.place(stacked.widget(0).view, loc + [1])
        
        parent_splitter.setSizes(sizes)
        
        stacked.widget(0).setFocus()
    
    def dump_config(self, var_name):
        config = []
        config.append('from PyQt5.QtCore import Qt')
        for loc, widget in self.iter_layout():
            if isinstance(widget, QtWidgets.QSplitter):
                config.append('{}.split({}, {})'.format(var_name, loc, 'Qt.Vertical' if widget.orientation() == Qt.Vertical else 'Qt.Horizontal'))
                config.append('{}.get_widget({}).setSizes({})'.format(var_name, loc, widget.sizes()))
            elif isinstance(widget, QtWidgets.QStackedWidget):
                config.append("ddic['actions/switch_view']({}.child_by_name('{}'), {})".format(var_name.rpartition('.')[0], widget.widget(0).view.name, loc))
#         
#         config.append('from pyde.pyde_frame import ChildLayout, Layout')
#         config.append('{}.set_layout({})'.format(var_name, self._dump_config_rec(self.layout)))
        return '\n'.join(config)
