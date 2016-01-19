from PyQt4.Qsci import QsciScintilla
import string
import os
from pyde.ddi import ddic, diinit, Dependency
from pyde.keyaction import KeyActionDfltCondition
from PyQt4.QtCore import QObject
from functools import wraps, partial
from inspect import getfullargspec, getargspec, signature
from pyde.plugins.templating import TemplFunc, FuncArgContentAssist

def all2kwargs(func, *args, **kwargs):
    arg_names, _, defaults, _, _, _, _ = getfullargspec(func)

    params = kwargs
    
    if defaults:
        # Add all the arguments that have a default value to the kwargs
        for name, val in zip(reversed(arg_names), reversed(defaults)):
            if name not in params:
                params[name] = val

    for name, val in zip(arg_names, args):
        params[name] = val

    unset = [a for a in arg_names if a not in params]
    
    return params, unset

def template2interpet(func):
    def wrapper(*args, **kwargs):
        
        kwargs, unset = all2kwargs(func, *args, **kwargs)
        return func(**kwargs)
    
    arg_names, _, defaults, _, _, _, _ = getfullargspec(func)

    no_default = {}
    if defaults:
        for a in arg_names[:len(arg_names) - len(defaults)]:
            no_default[a] = None
        
#     sig = signature(func)
#     params = []
#     for p in sig.parameters.values():
#         if p.default is sig.empty:
#             p = p.replace(name = p.name, kind = p.kind, default = None, annotation=p.annotation)
#             
#         params.append(p)
#               
#     sig = sig.replace(parameters=tuple(params))
    w = wraps(wrapper)(partial(func,**no_default))
    
    return w

def dflt_view_condition_factory(func_name):
    def dflt_view_condition(key_action, active_view, event):
#     return (fnmatch.fnmatch(uri2str(active_view.uri), key_action.view_uri) and
        if KeyActionDfltCondition(key_action, active_view, event) and \
            hasattr(active_view.widget, func_name):
            return True
    
    return dflt_view_condition

class LinpathContentAssist(FuncArgContentAssist):
    language = 'linpath'
    
#     def __init__(self, 
#                  ca : Dependency('content_assist'),
#                  win : Dependency('win')):
#         super().__init__()
#         self.ca = ca
#         self.win = win
#         self.ca.complete.connect(self.complete)
    @property
    def init_value(self):
        return "'" + os.getcwd() + "/'" 
    
    def pos(self, text):
        return len(text) - 1
    
    def complete(self, acceptor):
        pass

@diinit
def execute_action(win : Dependency('win'), active_view = None):
    interpret = win.view['interpret'].widget
    interpret.execute_view_action(win.active_view())

@diinit
def file_open(path : LinpathContentAssist, win : Dependency('win')):
    active_view = win.active_view()
    
    new_view = ddic['cls/editor_generic'](os.path.basename(path), parent_view=win)
    win.place_view(new_view, 
                   active_view.widget.last_location)

#     new_view.
    active_view.widget.setText(open(path).read())

# def switch_view(view: ):

@diinit
def file_open_kbd(win : Dependency('win'), execute_action : Dependency('keyactions/execute_action'), active_view = None):
    interpret = win.view['interpret'].widget
    execute_action.action(win, active_view)
    TemplFunc(file_open).apply(interpret)

# file_open()

def dflt_view_action_factory(func_name):
    @diinit
    def dflt_view_action(win : Dependency('win'), active_view = None):
        if active_view is None:
            active_view = win.active_view()

        if hasattr(active_view.widget, func_name):
            getattr(active_view.widget, func_name)()
            return
           
    dflt_view_action.__name__ = func_name
    return dflt_view_action

@diinit
def next_line(context : Dependency('context')):
#def next_line(context = None):
    
    c = context.active_context()
    
    while c.parent is not None:
        if hasattr(c, 'view'):
            if hasattr(c.view, 'next_line'):
                c.view.next_line()
                return
        
        c = c.parent

def backward_char(view=None):
    if view is None:
        view = ddic['win'].active_view()
        
    view.backward_char()

    
# def backward_char():
#     app.active_widget().backward_char()
#     
# def forward_line():
#     app.active_widget().SendScintilla(QsciScintilla.SCI_LINEDOWN)
# 
# def backward_line():
#     app.active_widget().SendScintilla(QsciScintilla.SCI_LINEUP)
# 
#
# @diinit
def content_assist_fill_query(active_view):
    active_view.widget.fill_query()
    
@diinit
def content_assist(win : Dependency('win'), ca : Dependency('content_assist'), active_view = None):
    if active_view is None:
        active_view = win.active_view()
        
    text = active_view.widget.text()
    if text:
        last_char = text[active_view.widget.pos-1] 
        if (last_char not in string.whitespace) or (last_char == '\n'):
            ca.activate(active_view)
            return True
    else:
        ca.activate(active_view)
        return True

    return False

# def select_content_assist():
#     if ddic['content_assist'].active:
#         ddic['content_assist'].fill_query()
    
 
#    raise KeyPressNotConsumed
#     app.active_widget().content_assist()
#     
def evaluate():
    ddic['win'].active_view().evaluate()
# 
# class Path(object):
#     def __init__(self, path=None):
#         if not path:
#             path = os.getcwd()
#             
#         self.path = path
#     
#     def __repr__(self):
#         return '"' + self.path + '"'
#     
#     def __str__(self):
#         return self.path
# 
# def open_file(path:Path):
#     pass
# 
# app.register_global("evaluate", evaluate)
# app.register_global("forward_char", forward_char)
# app.register_global("backward_char", backward_char)
# app.register_global("open_file", open_file)

# def open_file():
    
