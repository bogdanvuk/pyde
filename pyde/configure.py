from pyde.ddi import ddic, Dependency
from pyde.main_win import MainWindow
from pyde.application import App
import sys
from pyde.editors.interpret import PyInerpretEditor
from pyde.plugins.context import ContextProvider
from pyde.plugins.parser import Parser
from pyde.editor import PydeEditor

ddic.create_scope('cls')
ddic.provide_on_demand('cls.win', MainWindow, 'win')
ddic.provide('cls.python', PydeEditor)
ddic.provide('cls.ipython', PyInerpretEditor)
ddic.provide_on_demand('cls.context', ContextProvider, 'context')

def python_mode(editor : Dependency('editor.')):
    if editor.name in ['*scratch.py*', '*interpret*']:
        editor.mode.append('python')

wspace_path = '/data/projects/pyde/'    
sys.path.append(wspace_path)

import wspace.configure  # @UnresolvedImport


