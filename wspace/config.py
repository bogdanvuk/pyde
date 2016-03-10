from pyde.ddi import Dependency, ddic

def reload_config_for_win_layout(win_layout: Dependency('win_layout')):
    from PyQt4.QtCore import Qt
#     from pyde.pyde_frame import ChildLayout, Layout
    win_layout.split([], Qt.Vertical, (5,1))
#     ddic['win_layout'].set_layout(Layout(Qt.Vertical, [ChildLayout(5,None),ChildLayout(1,None)]))
def reload_config_for_win(win: Dependency('win')):
    ddic.provide('view/actions.py', ddic['cls/view']('actions.py',ddic['win'],file_name='/data/projects/pyde/pyde/actions.py'))
    ddic.provide('view/interpret', ddic['cls/view']('interpret',ddic['win']))
    ddic.provide('view/scratch.py', ddic['cls/view']('scratch.py',ddic['win'],file_name='/data/projects/pyde/wspace/scratch.py'))
    ddic.provide('view/QsciScintillaCompat.py', ddic['cls/view']('QsciScintillaCompat.py',ddic['win'],file_name='/data/projects/pyde/pyde/QsciScintillaCompat.py'))
    ddic['win'].widget.resize(706, 641)
    ddic['win'].layout.place(ddic['view/actions.py'], [0])
    ddic['view/actions.py'].widget.pos = 493
    ddic['view/actions.py'].widget.anchor = 493
    ddic['win'].layout.place(ddic['view/interpret'], [1])
    ddic['view/interpret'].widget.pos = 0
    ddic['view/interpret'].widget.anchor = 0
    
#     from PyQt4.QtCore import Qt
#     win.layout.split([0], Qt.Horizontal)
#     win.layout.split([0, 1], Qt.Vertical)
#     win.layout.split([0, 1, 0], Qt.Horizontal)

