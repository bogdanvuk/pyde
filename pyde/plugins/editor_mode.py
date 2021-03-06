from pyde.ddi import Dependency, Amendment
import os
import re

class ViewMode:
    def __init__(self, view):
        self.view = view
        self.view.mode = self
#         if not hasattr(editor, 'modes'):
#             editor.modes = []
#         
#         editor.modes.append(self)

def ViewModeRegexFactory(mode_name, re_str):
    class CustomViewMode(ViewMode):
        name = mode_name
        def __init__(self, view : Amendment('view/', lambda e: re.match(re_str, getattr(e, 'file_name', '')))):
            super().__init__(view)

    return CustomViewMode


def ViewModeExtensionFactory(mode_name, extensions):
    class CustomViewMode(ViewMode):
        name = mode_name
        def __init__(self, view : Amendment('view/', lambda e: os.path.splitext(getattr(e, 'file_name', ''))[1] in extensions)):
            super().__init__(view)

    return CustomViewMode

class IPythonMode(ViewMode):
    name = 'ipython'
    
    def __init__(self, view : Amendment('view/', lambda v: v.name == 'interpret')):
        super().__init__(view)
