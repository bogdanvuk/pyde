from pyde.ddi import Dependency, Amendment
import os
import re
import weakref

class ViewMode:
    def __init__(self, view):
        self._view = weakref.ref(view)
        self.view.mode = self

    @property
    def view(self):
        return self._view()
        
#         if not hasattr(editor, 'modes'):
#             editor.modes = []
#         
#         editor.modes.append(self)

class FileNameViewMode(ViewMode):

    def view_short_name(self):
        return os.path.basename(self.view.file_name)
    
def ViewModeRegexFactory(mode_name, re_str):
    class CustomViewMode(FileNameViewMode):
        name = mode_name
        def __init__(self, view : Amendment('view/*', lambda e: re.match(re_str, getattr(e, 'file_name', '')))):
            super().__init__(view)

    return CustomViewMode


def ViewModeExtensionFactory(mode_name, extensions):
    class CustomViewMode(FileNameViewMode):
        name = mode_name
        def __init__(self, view : Amendment('view/*', lambda e: os.path.splitext(getattr(e, 'file_name', ''))[1] in extensions)):
            super().__init__(view)

    return CustomViewMode

class IPythonMode(ViewMode):
    name = 'ipython'
    
    def __init__(self, view : Amendment('view/*', lambda v: getattr(v, 'special', '') == 'interpret')):
        super().__init__(view)

    def view_short_name(self):
        return 'interpret'
    