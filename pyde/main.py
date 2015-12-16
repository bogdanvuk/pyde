
import sys
from pyde.ddi import ddic
from PyQt4 import QtGui
import ast
from pyde.plugins.context import URI
# from pyde.application import app
# from pyde.main_win import MainWindow
# from PyQt4.QtCore import QObject
# import json    
# import os
# from inspect import signature

if __name__ == "__main__":
#     t = ast.parse('f(a,b,c,d)')
    
    app = QtGui.QApplication(sys.argv)
    import pyde.configure
    
#     wspace_path = '/data/projects/pyde/wspace'    
#     sys.path.append(wspace_path)
# 
#     from pyde.dflt_plugins import import_plugins
#     
#     import_plugins()
#     
#     from pyde.dflt_keybindings import bind_keys
#     bind_keys()
# 
#     from desktop import reload_desktop  # @UnresolvedImport
#     reload_desktop()
# 
#     app.win.show()
    ddic['win'].show()
    sys.exit(app.exec_())
