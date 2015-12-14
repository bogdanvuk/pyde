from pyde.ddi import ddic, Dependency
from pyde.main_win import MainWindow
from pyde.application import App
import sys
from pyde.editors.python import PythonEdit
from pyde.editors.interpret import PyInerpretEditor
from pyde.plugins.context import ContextProvider
from pyde.plugins.parser import Parser
from pyde.plugins.editor_mode import PythonMode
from pyde.keyaction import KeyAction
from pyde import actions
from PyQt4.QtCore import Qt
from pyde.plugins.content_assist import ContentAssist
from pyde.plugins.ca_interpreter import PyInterpretContentAssist

ddic.create_scope('view')
ddic.provide_on_demand('cls/win', MainWindow, 'win')
ddic.provide('cls/python', PythonEdit)
ddic.provide('cls/ipython', PyInerpretEditor)
ddic.provide_on_demand('cls/context', ContextProvider, 'context')

ddic.provide_on_demand('mode/python/cls', PythonMode, 'mode/python/inst/')
ddic.provide('parser/antlr4_generic', Parser)
ddic.provide_on_demand('parser/antlr4_generic', inst_feature='parser/inst/', inst_kwargs = {'language': 'python3'}, deps={'mode': Dependency('mode/python/inst/')})

ddic.provide_on_demand('cls/content_assist', ContentAssist, 'content_assist')
ddic.provide_on_demand('cls/ca_interpreter', PyInterpretContentAssist, 'ca_interpreter')

ddic.provide('keyactions/cls', KeyAction)
ddic.provide_on_demand('keyactions/cls', inst_feature='keyactions/forward_char', 
                       inst_kwargs={'action': actions.forward_char, 
                                    'key': Qt.Key_L, 
                                    'modifier': Qt.AltModifier}, 
                       deps={'view':Dependency('view/')})

ddic.provide_on_demand('keyactions/cls', inst_feature='keyactions/backward_char', 
                       inst_kwargs={'action': actions.backward_char, 
                                    'key': Qt.Key_J, 
                                    'modifier': Qt.AltModifier}, 
                       deps={'view':Dependency('view/')})

ddic.provide_on_demand('keyactions/cls', inst_feature='keyactions/content_assist', 
                       inst_kwargs={'action': actions.content_assist, 
                                    'key': Qt.Key_Tab}, 
                       deps={'view':Dependency('view/')})

ddic.provide_on_demand('keyactions/cls', inst_feature='keyactions/evaluate', 
                       inst_kwargs={'action': actions.evaluate, 
                                    'key': Qt.Key_Return}, 
                       deps={'view':Dependency('view/')})

wspace_path = '/data/projects/pyde/'    
sys.path.append(wspace_path)

import wspace.configure  # @UnresolvedImport


