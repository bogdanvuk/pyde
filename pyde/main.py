from PyQt4 import QtGui
import sys
from pyde.application import app
from pyde.main_win import MainWindow

# import pyde.editors
# print(dir(pyde.editors))

if __name__ == "__main__":
    app.win = MainWindow()
    app.init_ui()
    
    wspace_path = '/data/projects/pyde/wspace'    
    sys.path.append(wspace_path)
    from desktop import reload_desktop  # @UnresolvedImport
    
    reload_desktop()
    
    from pyde.dflt_keybindings import bind_keys
    bind_keys()
    
    app.win.show()
    sys.exit(app.exec_())
