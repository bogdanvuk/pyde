
import sys
from pyde.ddi import ddic
from PyQt4 import QtGui, QtCore
import ast
# from pyde.application import app
# from pyde.main_win import MainWindow
# from PyQt4.QtCore import QObject
# import json    
# import os
# from inspect import signature

def main():
    app = QtGui.QApplication(sys.argv)
    ddic.provide('app', app)
    import pyde.configure
    
    ddic['win'].widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
#     import cProfile
#     cProfile.run('main()', sort='tottime')

#     import time
#     
#     start = time.time()
#     main()
#     end = time.time()
#     print(end - start)

