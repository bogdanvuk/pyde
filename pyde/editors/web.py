
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView, QWebPage
from PyQt5.QtNetwork import QNetworkProxyFactory
from PyQt5.QtCore import Qt, QUrl, QEvent, QCoreApplication
from PyQt5.QtGui import QKeyEvent
from pyde.ddi import Amendment
from pyde.plugins.editor_mode import ViewMode

class WebViewMode(ViewMode):
    name = 'web'
    
    def __init__(self, view : Amendment('view/*', lambda v: hasattr(v, 'url'))):
        super().__init__(view)
    
    def view_short_name(self):
        return self.view.url
    
class WebWidget(QWebView):

    def __init__(self, view: Amendment('view/*', lambda v: hasattr(v, 'mode') and (v.mode.name == 'web') and (v.widget is None))): #, orig_editor=None):
        self.view = view
        if view.widget is not None:
            super().__init__()
        else:
            super().__init__(view.parent.widget)
            view.widget = self
            self.view.status_provider.add_field('title', position=0, formatting='"{}" ')

        self.urlChanged.connect(self.url_changed)
        self.titleChanged.connect(self.title_changed)
            
        self.load(QUrl(view.url))
        self.page().setContentEditable(True)
        QNetworkProxyFactory.setUseSystemConfiguration(True);
        QWebSettings.globalSettings().setAttribute(QWebSettings.PluginsEnabled, True);
        QWebSettings.globalSettings().setAttribute(QWebSettings.AutoLoadImages, True);

    def url_changed(self, url):
        self.view.url = url.toString()
        self.view.status_provider.set('view', self.view.name)
        for w in self.view._widget:
            if w.url() != url:
                w.load(url)

    def clone(self):
        return self.__class__(view=self.view)
    
    def title_changed(self, title):
        self.view.status_provider.set('title', title)
    
    def refresh(self):
        self.triggerPageAction(QWebPage.Reload)

    def forward_char(self):
        self.triggerPageAction(QWebPage.MoveToNextChar)
#         QCoreApplication.sendEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_Right, Qt.NoModifier))

    def backward_char(self):
        QCoreApplication.sendEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_Left, Qt.NoModifier))
        
    def previous_line(self):
        QCoreApplication.sendEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_Up, Qt.NoModifier))
    
    def next_line(self):
        QCoreApplication.sendEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_Down, Qt.NoModifier))

    def next_item(self):
        QCoreApplication.sendEvent(self, QKeyEvent(QEvent.KeyRelease, Qt.Key_Tab, Qt.NoModifier))
#         self.event(QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, Qt.NoModifier))
#         QCoreApplication.sendEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, Qt.NoModifier))

    def previous_item(self):
        QCoreApplication.sendEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, Qt.ShiftModifier))

    def forward_page(self):
        self.page().mainFrame().scroll(0, self.height() * 0.9)
#         self.scroll(0, self.height() * 0.9)
        
    def backward_page(self):
        self.page().mainFrame().scroll(0, -self.height() * 0.9)

# import sys
# 
# from PyQt5.QtWebKit import QWebView
# from PyQt5.QtGui import QApplication
# from PyQt5.QtCore import QUrl
# 
# app = QApplication(sys.argv)
# 
# browser = QWebView()
# browser.load(QUrl("http://www.google.com"))
# browser.show()
# 
# app.exec_()
