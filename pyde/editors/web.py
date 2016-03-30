
from PyQt4.QtWebKit import QWebView, QWebSettings
from PyQt4.QtNetwork import QNetworkProxyFactory
from PyQt4.QtCore import Qt, QUrl, QEvent, QCoreApplication
from PyQt4.QtGui import QKeyEvent
from pyde.ddi import Amendment

class WebWidget(QWebView):

    def __init__(self, view: Amendment('view/*', lambda v: hasattr(v, 'mode') and (v.mode.name == 'web') and (v.widget is None))): #, orig_editor=None):
        self.view = view
        QWebView.__init__(self)
        view.widget = self
        self.load(QUrl(view.filebuf.file_name))
        self.page().setContentEditable(True)
        QNetworkProxyFactory.setUseSystemConfiguration(True);
        QWebSettings.globalSettings().setAttribute(QWebSettings.PluginsEnabled, True);
        QWebSettings.globalSettings().setAttribute(QWebSettings.AutoLoadImages, True);

    def forward_char(self):
        QCoreApplication.sendEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_Right, Qt.NoModifier))

    def backward_char(self):
        QCoreApplication.sendEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_Left, Qt.NoModifier))
        
    def previous_line(self):
        QCoreApplication.sendEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_Up, Qt.NoModifier))
    
    def next_line(self):
        QCoreApplication.sendEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_Down, Qt.NoModifier))

    def forward_page(self):
        self.page().mainFrame().scroll(0, self.height() * 0.9)
#         self.scroll(0, self.height() * 0.9)
        
    def backward_page(self):
        self.page().mainFrame().scroll(0, -self.height() * 0.9)

# import sys
# 
# from PyQt4.QtWebKit import QWebView
# from PyQt4.QtGui import QApplication
# from PyQt4.QtCore import QUrl
# 
# app = QApplication(sys.argv)
# 
# browser = QWebView()
# browser.load(QUrl("http://www.google.com"))
# browser.show()
# 
# app.exec_()
