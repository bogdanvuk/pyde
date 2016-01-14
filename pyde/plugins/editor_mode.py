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
    
    def __init__(self, editor : Dependency('view/', lambda e: e.name in ['scratch.py', 'interpret'])):
        super().__init__(editor)