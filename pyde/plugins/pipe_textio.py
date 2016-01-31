import pexpect
import grammars
import os
import difflib

class PipeTextIO:
    def __init__(self, executable, cmd_line=[]):
        self.executable = executable
        self.cmd_line = cmd_line
        self.child = None   
    
    def connect(self):
        if not self.child:
            self.child = pexpect.spawnu(self.executable, self.cmd_line, echo=False)
    
    def write(self, s):
        self.connect()
        self.child.write(s)

    def communicate(self, inp=''):
        self.connect()
        self.child.write(inp)
#             self.child.sendcontrol('d')
        self.child.sendeof()
        if inp[-1] != '\n':
            self.child.sendeof()
#         self.child.expect(chr(0x04))
        self.child.expect("\r\n")
#         self.child.expect(pexpect.EOF)
        return self.child.before

if __name__ == '__main__':
    import time
    
    os.environ['CLASSPATH'] += ':' + os.path.dirname(grammars.__file__)
    io = PipeTextIO('java', ['pyinterface.ParserIntf', 'python3.python3', 'file_input'])
#     io = PipeTextIO('java', ['pyinterface.ParserIntf', 'linpath.linpath', 'main'])
    
    start_time = time.time()
    io.connect()
    print(time.time() - start_time)
    
    rets = []
    for _ in range(10):
        with open('/data/projects/pyde/pyde/QsciScintillaCompat.py') as f:
            data = f.read()
            start_time = time.time()
            rets.append(io.communicate(data))
            print(time.time() - start_time)    

    ret = rets[0]
    for r in rets[1:]:
        if r != ret:
#             dif = list(difflib.Differ().compare(r, ret))
            with open('/data/projects/pyde/proba.log', 'w') as f:
                f.write(r)
                f.write('\n')
                f.write(ret)
            import sys
            sys.exit(0)
#     print(ret)