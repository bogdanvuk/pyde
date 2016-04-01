from PyQt4.Qt import QObject
from pyde.ddi import Amendment
import os

class Filebuf(QObject):
    
#     @diinit
    def __init__(self, view: Amendment('view/*', lambda v: hasattr(v, 'status_provider'))):
        super().__init__()
        self.view = view
        self.view.filebuf = self
        self.file_hash = None
        self.dirty = None
        
        if hasattr(view, 'file_name'):
            self.file_name = view.file_name
        else:
            self.file_name = None
            
        self.view.status_provider.add_field('dirty', position=0)
                            
    def load(self):
        if self.file_name:
            text = self.read_file(self.file_name)
        else:
            text = ''

        self.file_hash = hash(text)
        self.view.widget.modificationChanged.connect(self.buf_modified)
        return text
    
    def save(self):
        if self.file_name:

            txt = self.view.widget.text()
            # work around glitch in scintilla: always make sure,
            # that the last line is terminated properly
            eol = self.view.widget.getLineSeparator()
            if eol:
                if len(txt) >= len(eol):
                    if txt[-len(eol):] != eol:
                        txt += eol
                else:
                    txt += eol
            
            with open(self.file_name, "w") as f:
                f.write(txt)
                
            self.view.widget.setModified(False)
    
    def buf_modified(self, modified):
        if modified:
            self.view.status_provider.set('dirty', '*')
        else:
            self.view.status_provider.set('dirty', '')
        
        self.dirty = modified
        
    def read_file(self, fn):
        if os.path.exists(fn):
            with open(fn, 'r') as f:
                return f.read()
        else:
            with open(fn, "w"):
                pass
            
            return ''
            
        
