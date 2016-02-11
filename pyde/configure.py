from pyde.ddi import ddic, Dependency
from pyde.main_win import MainWindow
from pyde.application import App
import sys
from pyde.editors.python import PythonEdit
from pyde.editors.interpret import PyInerpretEditor
from pyde.plugins.context import ContextProvider
from pyde.plugins.parser import Antlr4ParserFactory, Antlr4GenericParser
from pyde.plugins.ast_manager import EditorAstManager, IPythonEditorAstManager
from pyde.plugins.editor_mode import PythonMode, IPythonMode,\
    EditorModeExtensionFactory
from pyde.keyaction import KeyAction, KeyActionDfltCondition
from pyde import actions
from PyQt4.QtCore import Qt
from pyde.plugins.content_assist import ContentAssist
from pyde.plugins.ca_interpreter import PyInterpretContentAssist
from pyde.plugins.keydispatcher import KeyDispatcher
from pyde.plugins.templating import TemplActuator
from pyde.plugins.interpret_path_parser import InterpretPathParser
from pyde.plugins.lexer import Lexer
from pyde.editor import PydeEditor
from pyde.plugins.interpret_arg_island_lang import IslandLanguageParserFactory
from pyde.plugins.view_list_parser import ViewListParser
from pyde.actions import provide_action_args
from pyde.plugins.statusbar import StatusBar

# ddic.create_scope('view')
ddic.provide_on_demand('cls/win', MainWindow, 'win')
ddic.provide_on_demand('cls/statusbar', StatusBar, 'statusbar')
ddic.provide('cls/editor_generic', PydeEditor)
ddic.provide('cls/ipython', PyInerpretEditor)


ddic.provide_on_demand('cls/lexer', Lexer, 'lexer/inst/')
ddic.provide_on_demand('cls/templ_actuator', TemplActuator, 'templ_actuator/inst/')
ddic.provide_on_demand('cls/context', ContextProvider, 'context')
ddic.provide_on_demand('cls/key_dispatcher', KeyDispatcher, 'key_dispatcher')

ddic.provide_on_demand('mode/cls/python', PythonMode, 'mode/inst/')
ddic.provide_on_demand('mode/cls/ipython', IPythonMode, 'mode/inst/')
ddic.provide_on_demand('mode/cls/bash', EditorModeExtensionFactory('bash', ['.sh']), 'mode/inst/')
ddic.provide_on_demand('mode/cls/java', EditorModeExtensionFactory('java', ['.java']), 'mode/inst/')
ddic.provide_on_demand('mode/cls/cpp', EditorModeExtensionFactory('cpp', ['.c', '.cpp', '.cxx', '.h', '.hpp', '.hxx']), 'mode/inst/')
ddic.provide_on_demand('mode/cls/vhdl', EditorModeExtensionFactory('vhdl', ['.vhdl', '.vhd']), 'mode/inst/')

ddic.provide('parser/antlr4_generic', Antlr4GenericParser)
ddic.provide('parser/cls/linpath', Antlr4ParserFactory('linpath', 'main'))
ddic.provide('parser/cls/view_list', ViewListParser)
ddic.provide_on_demand('parser/cls/interpret_path_parser', IslandLanguageParserFactory('linpath'), 'parser/interpret_path_parser/inst')
ddic.provide_on_demand('parser/cls/interpret_view_list_parser', IslandLanguageParserFactory('view_list'), 'parser/interpret_view_list_parser/inst')
#ddic.provide_on_demand('cls/editor_ast_manager', EditorAstManager, inst_feature='editor_ast_manager/inst/', deps={'mode': Dependency('mode/inst/', lambda e: e.name != "ipython")})
ddic.provide_on_demand('cls/ipython_editor_ast_manager', IPythonEditorAstManager, inst_feature='editor_ast_manager/inst/', deps={'mode': Dependency('mode/inst/', lambda e: e.name == "ipython")})
#ddic.provide_on_demand('parser/antlr4_generic', inst_feature='parser/inst/', inst_kwargs = {'language': 'python3'}, deps={'mode': Dependency('mode/python/inst/')})
# ddic.provide_on_demand('parser/cls/', inst_feature='parser/inst/', inst_kwargs = {'language': 'python3'}, deps={'mode': Dependency('mode/python/inst/')})

ddic.provide_on_demand('cls/content_assist', ContentAssist, 'content_assist')
ddic.provide_on_demand('cls/ca_interpreter', PyInterpretContentAssist, 'ca_interpreter')

ddic.provide('cls/keyaction', KeyAction)

ddic.provide('actions/file_open', actions.file_open)
ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/file_open', 
                       inst_kwargs={'action': actions.execute_action_template_shortcut(actions.file_open),
                                    'key': Qt.Key_O,
                                    'modifier': Qt.ControlModifier})

ddic.provide('actions/switch_view', actions.switch_view)
ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/switch_view', 
                       inst_kwargs={'action': actions.execute_action_template_shortcut(actions.switch_view),
                                    'key': Qt.Key_E,
                                    'modifier': Qt.ControlModifier})

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/execute_action', 
                       inst_kwargs={'action': actions.execute_action,
                                    'key': Qt.Key_A,
                                    'modifier': Qt.AltModifier})

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

ddic.provide_on_demand(**provide_action_args('end_of_view', Qt.Key_N, Qt.AltModifier + Qt.ShiftModifier))

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/previous_line',
                       inst_kwargs={'action': actions.dflt_view_action_factory('previous_line'),
                                    'key': Qt.Key_I,
                                    'modifier': Qt.AltModifier})

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/backward_char',
                       inst_kwargs={'action': actions.dflt_view_action_factory('backward_char'),
                                    'key': Qt.Key_J,
                                    'modifier': Qt.AltModifier})
ddic.provide_on_demand(**provide_action_args('end_of_line', Qt.Key_H, Qt.AltModifier + Qt.ShiftModifier))
ddic.provide_on_demand(**provide_action_args('beginning_of_line', Qt.Key_H, Qt.AltModifier))

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/content_assist_fill_query', 
                       inst_kwargs={'action': actions.content_assist_fill_query,
                                    'key': Qt.Key_Tab,
                                    'uri': '/*/content_assist'})

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/content_assist', 
                       inst_kwargs={'action': actions.content_assist, 
                                    'key': Qt.Key_Tab})

def EvaluateKeyActionCondition(key_action, view, event):
    if view.name == 'content_assist':
        view.widget.select()

    return KeyActionDfltCondition(key_action, view, event)

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/evaluate', 
                       inst_kwargs={'action': actions.evaluate, #dflt_view_action_factory('evaluate'),
                                    'key': Qt.Key_Return,
                                    'modifier': Qt.ControlModifier,
                                    'condition': actions.dflt_view_condition_factory('evaluate'), #EvaluateKeyActionCondition 
                                    })

wspace_path = '/data/projects/pyde/'    
sys.path.append(wspace_path)

import wspace.configure  # @UnresolvedImport


