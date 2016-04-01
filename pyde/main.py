
import sys
from pyde.ddi import ddic
from PyQt5 import QtWidgets
import ast
# from pyde.application import app
# from pyde.main_win import MainWindow
# from PyQt5.QtCore import QObject
# import json    
# import os
# from inspect import signature

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
    QPushButton, QApplication)
from PyQt5.QtGui import QFont    


# class Example(QWidget):
#     
#     def __init__(self):
#         super().__init__()
#         
#         self.initUI()
#         
#         
#     def initUI(self):
#         
#         QToolTip.setFont(QFont('SansSerif', 10))
#         
#         self.setToolTip('This is a <b>QWidget</b> widget')
#         
#         btn = QPushButton('Button', self)
#         btn.setToolTip('This is a <b>QPushButton</b> widget')
#         btn.resize(btn.sizeHint())
#         btn.move(50, 50)       
#         
#         self.setGeometry(300, 300, 300, 200)
#         self.setWindowTitle('Tooltips')    
#         self.show()
#         
#         
# if __name__ == '__main__':
#     
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())

def main():
    app = QtWidgets.QApplication(sys.argv)
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

