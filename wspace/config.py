from pyde.ddi import Dependency, ddic


def reload_config_for_win(win: Dependency('win')):
    ddic.provide('view/actions.py', ddic['cls/view']('actions.py',win,file_name='/data/projects/pyde/pyde/actions.py'))
    ddic.provide('view/interpret', ddic['cls/view']('interpret',win))
    ddic.provide('view/__statusbar__', ddic['cls/view']('__statusbar__',win))
    ddic.provide('view/scratch.py', ddic['cls/view']('scratch.py',win,file_name='/data/projects/pyde/wspace/scratch.py'))
    ddic.provide('view/QsciScintillaCompat.py', ddic['cls/view']('QsciScintillaCompat.py',win,file_name='/data/projects/pyde/pyde/QsciScintillaCompat.py'))
    ddic.provide('view/trimac_receive_rtl.vhd', ddic['cls/view']('trimac_receive_rtl.vhd',win,file_name='/home/bvukobratovic/Downloads/trimac_receive_rtl.vhd'))
    win.widget.resize(718, 748)
    from PyQt4.QtCore import Qt
    win.layout.split([], Qt.Vertical)
    win.layout.get_widget([]).setSizes([706, 20])
    win.layout.split([0], Qt.Vertical)
    win.layout.get_widget([0]).setSizes([542, 160])
    win.layout.split([0, 0], Qt.Horizontal)
    win.layout.get_widget([0, 0]).setSizes([349, 347])
    ddic['actions/switch_view'](ddic['view/actions.py'], [0, 0, 0])
    ddic['actions/switch_view'](ddic['view/trimac_receive_rtl.vhd'], [0, 0, 1])
    ddic['actions/switch_view'](ddic['view/interpret'], [0, 1])
    ddic['actions/switch_view'](ddic['view/__statusbar__'], [1])

