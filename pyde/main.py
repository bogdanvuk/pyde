from PyQt4 import QtGui
import sys
from pyde import mainwin

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = mainwin.Main()
    main.show()
    sys.exit(app.exec_())
