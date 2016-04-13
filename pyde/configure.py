from ddi.ddi import ddic, Dependency
from pyde.main_win import MainWindow
import sys
from pyde.editors.interpret import PyInerpretEditor
from pyde.plugins.parser import Antlr4ParserFactory, Antlr4GenericParser
from pyde.plugins.ast_manager import IPythonEditorAstManager, EditorAstManager
from pyde.plugins.editor_mode import IPythonMode,\
    ViewModeExtensionFactory, ViewModeRegexFactory
from pyde.keyaction import KeyAction, KeyActionDfltCondition
from pyde import actions
from PyQt5.QtCore import Qt
from pyde.plugins.content_assist import ContentAssist, ContentAssistWidget
from pyde.plugins.ca_interpreter import PyInterpretContentAssist
from pyde.plugins.keydispatcher import KeyDispatcher
from pyde.plugins.templating import TemplActuator
from pyde.plugins.lexer import Lexer
from pyde.editor import PydeEditor
from pyde.plugins.interpret_arg_island_lang import IslandLanguageParserFactory
from pyde.plugins.view_list_parser import ViewListParser
from pyde.actions import provide_action_args
from pyde.plugins.statusbar import Statusbar, StatusbarMode, DefStatusProvider
from pyde.plugins.dump_config import DumpConfig
from pyde.pyde_frame import PydeFrame, ChildLayout
from pyde.layout import Layout
from pyde.view import View
from PyQt5 import QtCore
import os
import time
from pyde.plugins.filebuf import Filebuf
from pyde.plugins.ca_vhdl import VhdlContentAssist
from pyde.editors.web import WebWidget, WebViewMode
from pyde.plugins.pydbg import PyDbg

# ddic.create_scope('view')
#ddic.provide('cls/layout', PydeFrame)
ddic.provide_on_demand('cls/win_layout', Layout, 'win_layout')
ddic.provide_on_demand('cls/dump_config', DumpConfig, 'dump_config')
ddic.provide_on_demand('cls/win', MainWindow, 'widget/*')
ddic.provide_on_demand('cls/editor_generic', PydeEditor, 'widget/*')
ddic.provide_on_demand('cls/ipython', PyInerpretEditor, 'widget/*', mask=['cls/editor_generic'])
ddic.provide_on_demand('cls/web', WebWidget, 'widget/*')
ddic.provide_on_demand('cls/statusbar', Statusbar, 'widget/*')
ddic.provide('cls/view', View)

ddic.provide_on_demand('cls/lexer', Lexer, 'lexer/inst/')
ddic.provide_on_demand('cls/templ_actuator', TemplActuator, 'templ_actuator/inst/')
ddic.provide_on_demand('cls/key_dispatcher', KeyDispatcher, 'key_dispatcher')
ddic.provide_on_demand('cls/pydbg', PyDbg, 'debugger/inst/')

ddic.provide_on_demand('mode/cls/python', ViewModeExtensionFactory('python', ['.py']), 'mode/inst/')
ddic.provide_on_demand('mode/cls/ipython', IPythonMode, 'mode/inst/')
ddic.provide_on_demand('mode/cls/statusbar', StatusbarMode, 'mode/inst/')
ddic.provide_on_demand('mode/cls/bash', ViewModeExtensionFactory('bash', ['.sh']), 'mode/inst/')
ddic.provide_on_demand('mode/cls/java', ViewModeExtensionFactory('java', ['.java']), 'mode/inst/')
ddic.provide_on_demand('mode/cls/cpp', ViewModeExtensionFactory('cpp', ['.c', '.cpp', '.cxx', '.h', '.hpp', '.hxx']), 'mode/inst/')
ddic.provide_on_demand('mode/cls/vhdl', ViewModeExtensionFactory('vhdl', ['.vhdl', '.vhd']), 'mode/inst/')
ddic.provide_on_demand('mode/cls/web', WebViewMode, 'mode/inst/')
ddic.provide_on_demand('status_provider/cls/def_status_provider', DefStatusProvider, 'status_provider/inst/')
ddic.provide_on_demand('filebuf/cls/def_filebuf', Filebuf, 'filebuf/inst/')

ddic.provide('parser/antlr4_generic', Antlr4GenericParser)
ddic.provide('parser/cls/python', Antlr4ParserFactory('python3', 'file_input'))
ddic.provide('parser/cls/ipython', Antlr4ParserFactory('python3', 'file_input'))
ddic.provide('parser/cls/linpath', Antlr4ParserFactory('linpath', 'main'))
ddic.provide('parser/cls/vhdl', Antlr4ParserFactory('vhdl', 'design_file'))
ddic.provide('parser/cls/view_list', ViewListParser)
ddic.provide_on_demand('parser/cls/interpret_path_parser', IslandLanguageParserFactory('linpath'), 'parser/interpret_path_parser/inst')
ddic.provide_on_demand('parser/cls/interpret_view_list_parser', IslandLanguageParserFactory('view_list'), 'parser/interpret_view_list_parser/inst')
#ddic.provide_on_demand('cls/editor_ast_manager', EditorAstManager, inst_feature='editor_ast_manager/inst/', deps={'mode': Dependency('mode/inst/', lambda e: e.name != "ipython")})
ddic.provide_on_demand('cls/ipython_editor_ast_manager', IPythonEditorAstManager, inst_feature='editor_ast_manager/inst/', deps={'view': Dependency('view/*', lambda e: e.mode.name == "ipython")})
ddic.provide_on_demand('cls/vhdl_editor_ast_manager', EditorAstManager, inst_feature='editor_ast_manager/inst/', deps={'view': Dependency('view/*', lambda e: e.mode.name == "vhdl")})

#ddic.provide_on_demand('parser/antlr4_generic', inst_feature='parser/inst/', inst_kwargs = {'language': 'python3'}, deps={'mode': Dependency('mode/python/inst/')})
# ddic.provide_on_demand('parser/cls/', inst_feature='parser/inst/', inst_kwargs = {'language': 'python3'}, deps={'mode': Dependency('mode/python/inst/')})

ddic.provide_on_demand('cls/content_assist', ContentAssist, 'content_assist')
ddic.provide_on_demand('cls/content_assist_widget', ContentAssistWidget, 'ca_widget/')
ddic.provide_on_demand('cls/ca_interpreter', PyInterpretContentAssist, 'ca_interpreter')
ddic.provide_on_demand('cls/ca_vhdl', VhdlContentAssist, 'ca_vhdl')

ddic.provide('cls/keyaction', KeyAction)

ddic.provide('actions/search', actions.search)
ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/search', 
                       inst_kwargs={'action': actions.execute_action_template_shortcut(actions.search, interactive=True),
                                    'key': Qt.Key_Y,
                                    'modifier': Qt.AltModifier})


ddic.provide('actions/file_open', actions.file_open)
ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/file_open', 
                       inst_kwargs={'action': actions.execute_action_template_shortcut(actions.file_open),
                                    'key': Qt.Key_O,
                                    'modifier': Qt.ControlModifier})

ddic.provide('actions/url_open', actions.url_open)
ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/url_open', 
                       inst_kwargs={'action': actions.execute_action_template_shortcut(actions.url_open),
                                    'key': Qt.Key_O,
                                    'modifier': Qt.ControlModifier + Qt.ShiftModifier})

ddic.provide('actions/web_search', actions.web_search)
ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/web_search', 
                       inst_kwargs={'action': actions.execute_action_template_shortcut(actions.web_search),
                                    'key': Qt.Key_F,
                                    'modifier': Qt.ControlModifier})


ddic.provide('actions/file_save', actions.file_save)
ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/file_save', 
                       inst_kwargs={'action': actions.file_save,
                                    'key': Qt.Key_S,
                                    'modifier': Qt.ControlModifier})

ddic.provide('actions/switch_view', actions.switch_view)
ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/switch_view', 
                       inst_kwargs={'action': actions.execute_action_template_shortcut(actions.switch_view),
                                    'key': Qt.Key_E,
                                    'modifier': Qt.ControlModifier})

ddic.provide('actions/close_view', actions.close_view)
ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/close_view', 
                       inst_kwargs={'action': actions.close_view,
                                    'key': Qt.Key_W,
                                    'modifier': Qt.ControlModifier})

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/cycle_frame', 
                       inst_kwargs={'action': actions.cycle_frame,
                                    'key': Qt.Key_S,
                                    'modifier': Qt.AltModifier})

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/split_frame_vertical', 
                       inst_kwargs={'action': actions.split_frame_vertical,
                                    'key': Qt.Key_4,
                                    'modifier': Qt.AltModifier})

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/split_frame_horizontal', 
                       inst_kwargs={'action': actions.split_frame_horizontal,
                                    'key': Qt.Key_Dollar,
                                    'modifier': Qt.AltModifier + Qt.ShiftModifier})

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/merge_frame', 
                       inst_kwargs={'action': actions.merge_frame,
                                    'key': Qt.Key_2,
                                    'modifier': Qt.AltModifier})

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

ddic.provide_on_demand(**provide_action_args('debug', Qt.Key_F11))
ddic.provide_on_demand(**provide_action_args('refresh', Qt.Key_F5))
ddic.provide_on_demand(**provide_action_args('next_item', Qt.Key_L, Qt.ControlModifier))
ddic.provide_on_demand(**provide_action_args('previous_item', Qt.Key_J, Qt.ControlModifier))
ddic.provide_on_demand(**provide_action_args('end_of_line', Qt.Key_H, Qt.AltModifier + Qt.ShiftModifier))
ddic.provide_on_demand(**provide_action_args('beginning_of_line', Qt.Key_H, Qt.AltModifier))
ddic.provide_on_demand(**provide_action_args('forward_word', Qt.Key_O, Qt.AltModifier))
ddic.provide_on_demand(**provide_action_args('backward_word', Qt.Key_U, Qt.AltModifier))
ddic.provide_on_demand(**provide_action_args('forward_page', Qt.Key_K, Qt.AltModifier + Qt.ShiftModifier))
ddic.provide_on_demand(**provide_action_args('backward_page', Qt.Key_I, Qt.AltModifier + Qt.ShiftModifier))
ddic.provide_on_demand(**provide_action_args('del_forward_char', Qt.Key_F, Qt.AltModifier))
ddic.provide_on_demand(**provide_action_args('del_backward_char', Qt.Key_D, Qt.AltModifier))


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

ddic.provide_on_demand(**provide_action_args('cancel', Qt.Key_G, Qt.ControlModifier))

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/evaluate', 
                       inst_kwargs={'action': actions.evaluate, #dflt_view_action_factory('evaluate'),
                                    'key': Qt.Key_Return,
                                    'modifier': Qt.ControlModifier,
                                    'condition': actions.dflt_view_condition_factory('evaluate'), #EvaluateKeyActionCondition 
                                    })

ddic.provide_on_demand('cls/keyaction', inst_feature='keyactions/evaluate_repeat', 
                       inst_kwargs={'action': actions.evaluate_repeat, #dflt_view_action_factory('evaluate'),
                                    'key': Qt.Key_R,
                                    'modifier': Qt.ControlModifier,
                                    'condition': actions.dflt_view_condition_factory('evaluate'), #EvaluateKeyActionCondition 
                                    })


ddic.provide('config/wspace/path', '/data/projects/pyde/wspace')

sys.path.append('/data/projects/pyde/wspace')

from wspace import config
import inspect
  
def is_mod_function(mod, func):
    return inspect.isfunction(func) and inspect.getmodule(func) == mod
  
def module_functions(mod):
    for _, func in mod.__dict__.items():
        if is_mod_function(mod, func):
            yield func
  
for f in module_functions(config):
    ddic.provide_on_demand('config/wspace/' + f.__name__, f)
 
# ddic.provide('win_layout', ddic['cls/layout']())
ddic.provide('win', ddic['cls/view'](special='win'))

pass