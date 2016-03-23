from pyde.ddi import Dependency, ddic


def reload_config_for_win(win: Dependency('win')):
    ddic.provide('view/actions.py', ddic['cls/view']('actions.py',win,file_name='/data/projects/pyde/pyde/actions.py'))
    ddic.provide('view/interpret', ddic['cls/view']('interpret',win))
    ddic.provide('view/__statusbar__', ddic['cls/view']('__statusbar__',win))
    ddic.provide('view/scratch.py', ddic['cls/view']('scratch.py',win,file_name='/data/projects/pyde/wspace/scratch.py'))
    ddic.provide('view/QsciScintillaCompat.py', ddic['cls/view']('QsciScintillaCompat.py',win,file_name='/data/projects/pyde/pyde/QsciScintillaCompat.py'))
    ddic.provide('view/and.vhd', ddic['cls/view']('and.vhd',win,file_name='/home/bvukobratovic/Downloads/and.vhd'))
    ddic.provide('view/google.com', ddic['cls/view']('google.com',win,file_name='http://www.google.com'))
    win.widget.resize(1215, 776)
    win.widget.showMaximized()
    from PyQt4.QtCore import Qt
    win.layout.split([], Qt.Vertical)
    win.layout.get_widget([]).setSizes([723, 29])
    win.layout.split([0], Qt.Vertical)
    win.layout.get_widget([0]).setSizes([553, 164])
    win.layout.split([0, 0], Qt.Horizontal)
    win.layout.get_widget([0, 0]).setSizes([597, 594])
    ddic['actions/switch_view'](ddic['view/google.com'], [0, 0, 0])
    ddic['actions/switch_view'](ddic['view/and.vhd'], [0, 0, 1])
    ddic['actions/switch_view'](ddic['view/interpret'], [0, 1])
    ddic['actions/switch_view'](ddic['view/__statusbar__'], [1])

