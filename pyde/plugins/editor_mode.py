from pyde.ddi import Dependency
import os

class EditorMode:
    def __init__(self, editor):
        self.editor = editor
#         if not hasattr(editor, 'modes'):
#             editor.modes = []
#         
#         editor.modes.append(self)

def EditorModeExtensionFactory(mode_name, extensions):
    class EditorMode:
        name = mode_name
        def __init__(self, editor : Dependency('winview/', lambda e: os.path.splitext(getattr(e, 'file_name', ''))[1] in extensions)):
            self.editor = editor

    return EditorMode

class PythonMode(EditorMode):
    name = 'python'
    
    def __init__(self, editor : Dependency('winview/', lambda e: e.name.endswith('.py'))):
        super().__init__(editor)
        
class IPythonMode(EditorMode):
    name = 'ipython'
    
    def __init__(self, editor : Dependency('winview/', lambda e: e.name in ['interpret'])):
        super().__init__(editor)
