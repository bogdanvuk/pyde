from pyde.ddi import Dependency, ddic


def reload_config_for_win(win: Dependency('win')):
    ddic.provide('view/actions.py', ddic['cls/view']('actions.py',win,file_name='/data/projects/pyde/pyde/actions.py'))
    ddic.provide('view/interpret', ddic['cls/view']('interpret',win))
    ddic.provide('view/scratch.py', ddic['cls/view']('scratch.py',win,file_name='/data/projects/pyde/wspace/scratch.py'))
    ddic.provide('view/QsciScintillaCompat.py', ddic['cls/view']('QsciScintillaCompat.py',win,file_name='/data/projects/pyde/pyde/QsciScintillaCompat.py'))
    win.widget.resize(706, 641)
    from PyQt4.QtCore import Qt
    win.layout.split([], Qt.Vertical)
    win.layout.get_widget([]).setSizes([495, 98])
    win.layout.split([0], Qt.Horizontal)
    win.layout.get_widget([0]).setSizes([342, 342])
    ddic['actions/switch_view'](ddic['view/QsciScintillaCompat.py'], [0, 0])
    win.layout.split([0, 1], Qt.Vertical)
    win.layout.get_widget([0, 1]).setSizes([246, 245])
    ddic['actions/switch_view'](ddic['view/QsciScintillaCompat.py'], [0, 1, 0])
    ddic['actions/switch_view'](ddic['view/actions.py'], [0, 1, 1])
    ddic['actions/switch_view'](ddic['view/interpret'], [1])

