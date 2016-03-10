from PyQt4.Qt import QObject
from pyde.ddi import Dependency, ddic
import textwrap
import os

class DumpConfig(QObject):
    
    def __init__(self, app: Dependency('app'), wspace_path: Dependency('config/wspace/path')):
        super().__init__(app)
#         app.aboutToQuit.connect(self.dump)
        self.wspace_path = wspace_path

    def dump_config_for(self, feature):
        func = []
        feature_python_name = feature.replace('/', '_') 
        func.append("\ndef reload_config_for_{}({}: Dependency('{}')):".format(feature_python_name, feature_python_name, feature))
        conf = ddic[feature].dump_config("ddic['{}']".format(feature))
        func.append(textwrap.indent(conf, ' '*4))
        
        return '\n'.join(func)
    
    def dump(self):
        with open(os.path.join(self.wspace_path, 'config.py'), 'w') as f:
            f.write('from pyde.ddi import Dependency, ddic\n\n')
            f.write(self.dump_config_for('win_layout'))
            f.write(self.dump_config_for('win'))
            f.write('\n\n')
