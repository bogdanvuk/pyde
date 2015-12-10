from pyde.ddi import ddic, Dependency
from pyde.main_win import MainWindow
from pyde.application import App
import sys
from pyde.editors.python import PythonEdit
from pyde.editors.interpret import PyInerpretEditor
from pyde.plugins.context import ContextProvider
from pyde.plugins.parser import Parser
from pyde.plugins.editor_mode import PythonMode

ddic.create_scope('cls')
ddic.provide_on_demand('cls/win', MainWindow, 'win')
ddic.provide('cls/python', PythonEdit)
ddic.provide('cls/ipython', PyInerpretEditor)
ddic.provide_on_demand('cls/context', ContextProvider, 'context')

ddic.create_scope('view')
ddic.create_scope('mode')
ddic.create_scope('mode/inst')
ddic.provide_on_demand('mode/python', PythonMode, 'mode/inst/')

wspace_path = '/data/projects/pyde/'    
sys.path.append(wspace_path)

import wspace.configure  # @UnresolvedImport


