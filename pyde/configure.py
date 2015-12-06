from pyde.ddi import ddic
from pyde.main_win import MainWindow
from pyde.application import App
import sys

ddic.create_scope('cls')
ddic.provide('cls.app', App)
ddic.provide('cls.win', MainWindow)

wspace_path = '/data/projects/pyde/wspace'    
sys.path.append(wspace_path)

import configure  # @UnresolvedImport


