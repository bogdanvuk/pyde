from pyde.ddi import ddic, Dependency
from pyde.main_win import MainWindow
from pyde.application import App
import sys
from pyde.editors.python import PythonEdit
from pyde.editors.interpret import PyInerpretEditor
from pyde.plugins.context import ContextProvider
from pyde.plugins.parser import Parser, Antlr4ParserFactory
from pyde.plugins.editor_mode import PythonMode
from pyde.keyaction import KeyAction, KeyActionDfltCondition
from pyde import actions
from PyQt4.QtCore import Qt
from pyde.plugins.content_assist import ContentAssist
from pyde.plugins.ca_interpreter import PyInterpretContentAssist
from pyde.plugins.keydispatcher import KeyDispatcher
from pyde.plugins.templating import TemplActuator
from pyde.plugins.interpret_path_parser import InterpretPathParser

# ddic.create_scope('view')
ddic.provide_on_demand('cls/win', MainWindow, 'win')
ddic.provide('cls/python', PythonEdit)
ddic.provide('cls/ipython', PyInerpretEditor)
ddic.provide_on_demand('cls/templ_actuator', TemplActuator, 'templ_actuator')
ddic.provide_on_demand('cls/context', ContextProvider, 'context')
ddic.provide_on_demand('cls/key_dispatcher', KeyDispatcher, 'key_dispatcher')
ddic.provide_on_demand('cls/interpret_path_parser', InterpretPathParser, 'interpret_path_parser')

ddic.provide_on_demand('mode/python/cls', PythonMode, 'mode/python/inst/')
ddic.provide('parser/antlr4_generic', Parser)
ddic.provide('parser/cls/linpath', Antlr4ParserFactory('linpath'))
ddic.provide_on_demand('parser/antlr4_generic', inst_feature='parser/inst/', inst_kwargs = {'language': 'python3'}, deps={'mode': Dependency('mode/python/inst/')})
ddic.provide_on_demand('parser/cls/', inst_feature='parser/inst/', inst_kwargs = {'language': 'python3'}, deps={'mode': Dependency('mode/python/inst/')})

ddic.provide_on_demand('cls/content_assist', ContentAssist, 'content_assist')
ddic.provide_on_demand('cls/ca_interpreter', PyInterpretContentAssist, 'ca_interpreter')

ddic.provide('cls/keyaction', KeyAction)
ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/forward_char', 
                       inst_kwargs={'action': actions.dflt_view_action_factory('forward_char'),
                                    'key': Qt.Key_L,
                                    'modifier': Qt.AltModifier})

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/next_line',
                       inst_kwargs={'action': actions.dflt_view_action_factory('next_line'),
                                    'key': Qt.Key_K,
                                    'modifier': Qt.AltModifier,
                                    'condition': actions.dflt_view_condition_factory('next_line')})

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/beginning_of_view',
                       inst_kwargs={'action': actions.dflt_view_action_factory('beginning_of_view'),
                                    'key': Qt.Key_N,
                                    'modifier': Qt.AltModifier,
                                    'condition': actions.dflt_view_condition_factory('beginning_of_view')})

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/end_of_view',
                       inst_kwargs={'action': actions.dflt_view_action_factory('end_of_view'),
                                    'key': Qt.Key_N,
                                    'modifier': Qt.AltModifier + Qt.ShiftModifier,
                                    'condition': actions.dflt_view_condition_factory('end_of_view')})

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/previous_line',
                       inst_kwargs={'action': actions.dflt_view_action_factory('previous_line'),
                                    'key': Qt.Key_I,
                                    'modifier': Qt.AltModifier})

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/backward_char',
                       inst_kwargs={'action': actions.dflt_view_action_factory('backward_char'),
                                    'key': Qt.Key_J,
                                    'modifier': Qt.AltModifier})

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/content_assist_fill_query', 
                       inst_kwargs={'action': actions.content_assist_fill_query,
                                    'key': Qt.Key_Tab,
                                    'uri': '/*/content_assist'})

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/content_assist', 
                       inst_kwargs={'action': actions.content_assist, 
                                    'key': Qt.Key_Tab})

def EvaluateKeyActionCondition(key_action, view, event):
    if view.name != 'content_assist':
        return KeyActionDfltCondition(key_action, view, event)
    else:
        return False

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/evaluate', 
                       inst_kwargs={'action': actions.dflt_view_action_factory('evaluate'),
                                    'key': Qt.Key_Return,
                                    'modifier': Qt.ControlModifier,
                                    'condition': EvaluateKeyActionCondition})

wspace_path = '/data/projects/pyde/'    
sys.path.append(wspace_path)

import wspace.configure  # @UnresolvedImport


