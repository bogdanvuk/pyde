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
