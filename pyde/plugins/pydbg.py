from ddi.ddi import Dependency
import pexpect

class PyDbg:
    def __init__(self, widget: Dependency('widget/*', lambda w: hasattr(w.view, 'mode') and (w.view.mode.name == "python"))):
        widget.debug = self #self.__get__(self, widget.__class__)
        self.widget = widget
        
    def __call__(self):
        self.p = pexpect.spawnu('pdb {}'.format(self.widget.view.file_name))
        self.p.expect('(Pdb)')
        self.p.send('q')

