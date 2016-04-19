from ddi.ddi import Dependency, ddic


def reload_config_for_win(win: Dependency('win')):
    ddic.provide('view/', ddic['cls/view'](win,file_name='/data/projects/pyde/pyde/actions.py'))
    ddic.provide('view/', ddic['cls/view'](win,special='interpret'))
    ddic.provide('view/', ddic['cls/view'](win,special='statusbar'))
    ddic.provide('view/', ddic['cls/view'](win,file_name='/data/projects/pyde/wspace/scratch.py'))
    ddic.provide('view/', ddic['cls/view'](win,file_name='/data/projects/pyde/pyde/QsciScintillaCompat.py'))
    ddic.provide('view/', ddic['cls/view'](win,file_name='/home/bvukobratovic/Downloads/and.vhd'))
    ddic.provide('view/', ddic['cls/view'](win,file_name='/home/bvukobratovic/Documents/proba.py'))
    win.widget.resize(1215, 776)
    win.widget.showMaximized()
    from PyQt5.QtCore import Qt
    win.layout.split([], Qt.Vertical)
    win.layout.get_widget([]).setSizes([723, 29])
    win.layout.split([0], Qt.Vertical)
    win.layout.get_widget([0]).setSizes([553, 164])
    win.layout.split([0, 0], Qt.Horizontal)
    win.layout.get_widget([0, 0]).setSizes([597, 594])
    ddic['actions/switch_view'](win.child_by_name('proba.py'), [0, 0, 0])
    ddic['actions/switch_view'](win.child_by_name('QsciScintillaCompat.py'), [0, 0, 1])
    ddic['actions/switch_view'](win.child_by_name('interpret'), [0, 1])
    ddic['actions/switch_view'](win.child_by_name('statusbar'), [1])

