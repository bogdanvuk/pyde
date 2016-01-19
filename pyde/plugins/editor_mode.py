from pyde.ddi import Dependency

class EditorMode:
    def __init__(self, editor):
        self.editor = editor
#         if not hasattr(editor, 'modes'):
#             editor.modes = []
#         
#         editor.modes.append(self)
        
class PythonMode(EditorMode):
    name = 'python'
    
    def __init__(self, editor : Dependency('view/', lambda e: e.name.endswith('.py'))):
        super().__init__(editor)
        
class IPythonMode(EditorMode):
    name = 'ipython'
    
    def __init__(self, editor : Dependency('view/', lambda e: e.name in ['interpret'])):
        super().__init__(editor)
