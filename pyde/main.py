from PyQt4 import QtGui
import sys
from pyde.application import app
from pyde.main_win import MainWindow
from PyQt4.QtCore import QObject
import json
import os

# import pyde.editors
# print(dir(pyde.editors))

if __name__ == "__main__":
#     with open('/home/bvukobratovic/Downloads/grammars-v4-master/python3/parse.js') as data_file:    
#         data = json.load(data_file)

    import subprocess
    os.chdir('/home/bvukobratovic/projects/pyde/grammars')
#     p = subprocess.Popen(['java', '-cp', '.', 'python3.Main', 'python3.Python3', 'file_input', '-json', "app.bla\n"], stdout=subprocess.PIPE).communicate()[0]
#     p = subprocess.Popen(['java', 'python3.Main', 'python3.Python3 file_input -json "app.bla\n"'], stdout=subprocess.PIPE).communicate()[0]
#     p = subprocess.Popen(['echo', 'java', 'python3.Main', 'python3.Python3 file_input -json "app.bla\\n"'], stdout=subprocess.PIPE).communicate()[0]
#     p = subprocess.Popen(['java', 'python3.Main', 'python3.Python3 file_input -json "app.bla\\n"'], stdout=subprocess.PIPE).communicate()[0]
    p = subprocess.Popen(['java', 'python3.Main', 'python3.Python3', 'file_input', '-json', 'app.bla\\n'], stdout=subprocess.PIPE).communicate()[0]
    print(p.decode())
    
    sys.exit(0)
    
    import ast
    
    class v(ast.NodeVisitor):
        def generic_visit(self, node):
            try:
                print(type(node).__name__, ':', (node.lineno, node.col_offset), ':', ast.dump(node))
            except AttributeError:
                print(type(node).__name__)

            ast.NodeVisitor.generic_visit(self, node)
    
    class ContextFinder(ast.NodeVisitor):
        def __init__(self, pos):
            self.context = []
            self.pos = pos
        
        def generic_visit(self, node):
            if hasattr(object, 'pos'):
                if node.pos[0] <= self.pos and self.pos < node.pos[1]:
                    self.context.append(node)
                    

            ast.NodeVisitor.generic_visit(self, node)
    
    def node_iter(node):
        for _, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        yield item
            elif isinstance(value, ast.AST):
                yield value
                
    def tree_iter(tree):
        for node in node_iter(tree):
            yield node
            yield from tree_iter(node)
                
    def scope_at_pos(tree, pos):
        scope = []
        for node in tree_iter(tree):
            if hasattr(node, 'pos'):
                if node.pos[0] <= pos and pos < node.pos[1]:
                    scope.append(node)
                    
        return scope

    class PositionUpdater(object):
        def __init__(self, text):
            self.leaf = None
            self.cur_end = len(text)
            self.lines = text.split('\n')
            self.col_cur_end = []
            for line in self.lines:
                self.col_cur_end.append(len(line))

        def visit(self, node):
            is_leaf = True
            
            if hasattr(node, 'lineno'):
                node.lineno -= 1
                line_offset = sum(self.col_cur_end[:node.lineno]) + node.lineno # compensate for end of line
                node.col_pos = (node.col_offset, self.col_cur_end[node.lineno])
                node.pos = (line_offset + node.col_pos[0], line_offset + node.col_pos[1])
                node.text = self.lines[node.lineno][node.col_pos[0]:node.col_pos[1]]
                
                try:
                    print(type(node).__name__, ':', node.text, ':', (node.lineno, node.col_offset), ':', node.col_pos, ':', node.pos, ':', ast.dump(node))
                except AttributeError:
                    print(type(node).__name__)
            
            
            if hasattr(node, 'lineno') or isinstance(node, ast.mod):      
                node.is_leaf = True
            
                for child in reversed(list(node_iter(node))):
                    if not self.visit(child):
                        node.is_leaf = False

                if node.is_leaf:
                    self.col_cur_end[node.lineno] = node.col_offset - 1
                    
                return False
            else:
                return True
            
                         
            return is_leaf

#     class PositionUpdater(ast.NodeVisitor):
#         def __init__(self, text):
#             self.leaf = None
#             self.cur_end = len(text)
#             self.lines = text.split('\n')
#             self.col_cur_end = []
#             for line in self.lines:
#                 self.col_cur_end.append(len(line))
#         
#         def visit(self, node):
#             if hasattr(node, 'lineno'):
#                 node.lineno -= 1
#                 line_offset = sum(self.col_cur_end[:node.lineno]) + node.lineno # compensate for end of line
#                 node.col_pos = (node.col_offset, self.col_cur_end[node.lineno])
#                 node.pos = (line_offset + node.col_pos[0], line_offset + node.col_pos[1])
#                 node.text = self.lines[node.lineno][node.col_pos[0]:node.col_pos[1]]
#                 
#                 try:
#                     print(type(node).__name__, ':', node.text, ':', (node.lineno, node.col_offset), ':', node.col_pos, ':', node.pos, ':', ast.dump(node))
#                 except AttributeError:
#                     print(type(node).__name__)
#                     
#                 node.is_leaf = self.generic_visit(node)
#                 
#                 if node.is_leaf:
#                     self.col_cur_end[node.lineno] = node.col_offset - 1
#                     
#                 return False
#             elif isinstance(node, ast.mod):
#                 return self.generic_visit(node)
#             else:
#                 return True
# 
#         def generic_visit(self, node):
#             is_leaf = True
#             for node in reversed(list(node_iter(node))):
#                 if not self.visit(node):
#                     is_leaf = False
#              
#             return is_leaf
# 
# #             for field, value in reversed(list(ast.iter_fields(node))):
# #                 if isinstance(value, list):
# #                     for item in reversed(value):
# #                         if isinstance(item, ast.AST):
# #                             if not self.visit(item):
# #                                 is_leaf = False
# #                 elif isinstance(value, ast.AST):
# #                     if not self.visit(value):
# #                         is_leaf = False
# #  
# #             return is_leaf
        
    text = """
file_open(a+      0xff, b).
"""
#     import pyde.pyposast
#     from astmonkey import visitors
#     
#     code = 'x = y + 1'
#     node = pyde.pyposast.parse(text)

    try:    
        a = ast.parse(text, mode='single')
    except SyntaxError as e:
        import traceback
        print(traceback.format_exc())
        pass
    
#     x = PositionUpdater(text)
# #     x = v()
# #     print(list(tree_iter(a)))
#     x.visit(a)
     
#     print(scope_at_pos(a, 12))
     
#     import sys
#      
#     sys.exit(0)
    
    app.win = MainWindow()
    app.init_ui()
    
    wspace_path = '/data/projects/pyde/wspace'    
    sys.path.append(wspace_path)

    from pyde.dflt_plugins import import_plugins
    
    import_plugins()
    
    from pyde.dflt_keybindings import bind_keys
    bind_keys()

#     class MarkActivator(QObject):
#            
#         def new_view(self):
#             print("VIEW ADDED!")
# 
# 
#     app.register_global('proba', MarkActivator())
#     app.view_added.connect(app.globals.mark_activator.new_view)
#     print("CONNECTED")

    from desktop import reload_desktop  # @UnresolvedImport
    reload_desktop()

    app.win.show()
    sys.exit(app.exec_())
