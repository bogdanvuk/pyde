from pyde.ddi import ddic
from pyde.main_win import MainWindow
from pyde.application import App
import sys
from pyde.editors.python import PythonEdit
from pyde.editors.interpret import PyInerpretEditor

ddic.create_scope('cls')
ddic.provide('cls.app', App)
ddic.provide('cls.win', MainWindow)
ddic.provide('cls.python', PythonEdit)
ddic.provide('cls.ipython', PyInerpretEditor)

wspace_path = '/data/projects/pyde/'    
sys.path.append(wspace_path)

import wspace.configure  # @UnresolvedImport


