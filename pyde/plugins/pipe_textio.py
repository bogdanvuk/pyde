import subprocess
import os, tempfile

# import grammars
# os.environ['CLASSPATH'] += ':' + os.path.dirname(grammars.__file__)

class PipeTextIO:
    def __init__(self, executable, cmd_line=[]):
        self.executable = executable
        self.cmd_line = cmd_line
        self.fifo_in = None
        self.fifo_out = None
        self.fifo_dir = None
        self.p = None
    
    def connect(self):
        if not self.p:
            self.fifo_dir = tempfile.mkdtemp()
            self.fout = os.path.join(self.fifo_dir, 'fout')
            self.fin = os.path.join(self.fifo_dir, 'fin')
            try:
                os.mkfifo(self.fin)
                os.mkfifo(self.fout)
            except OSError as e:
                print("Failed to create FIFO: %s" % e)
            else:
                self.p = subprocess.Popen([self.executable] + self.cmd_line + [self.fout, self.fin], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.fifo_out = open(self.fout, 'w')
                self.fifo_in = open(self.fin, 'r')
            
    def __del__(self):
        if self.p:
            self.p.kill()
            
        if self.fifo_out:
            os.remove(self.fin)
        if self.fifo_in:
            os.remove(self.fout)
        
        if self.fifo_dir:
            os.rmdir(self.fifo_dir)
        
    def write(self, s):
        self.connect()
        self.fifo_out.write(s)
        self.fifo_out.flush()

    def communicate(self, inp=''):
        self.write(inp)
        self.write(chr(26))

        return self.fifo_in.readline()
#     
# import os
# import socket
# from subprocess import Popen
# import grammars
# import time
# 
# class IPC(object):
#     def __init__(self):
#         os.environ['CLASSPATH'] += ':' + os.path.dirname(grammars.__file__)
#             #     io = PipeTextIO('java', ['pyinterface.ParserIntf', 'python3.python3', 'file_input'])
#         
#         self.p = Popen(['java', 'pyinterface.ParserIntf', 'python3.python3', 'file_input'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
# 
# #         self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 
# #         connected = False
# #         while not connected:
# #             try:
# #                 self.s.connect(("localhost", 32000))
# #                 connected = True
# #             except Exception as e:
# #                 pass #Do nothing, just try again
#         
# #         self.fid = self.s.makefile() # file wrapper to read lines
#         try:
#             os.mkfifo("/tmp/pyde_out")
#         except:
#             pass
#         
#         try:
#             os.mkfifo("/tmp/pyde_in")
#         except:
#             pass
#         self.fid = open("/tmp/pyde_out", 'w')
#         self.fin = open("/tmp/pyde_in", 'r')
#         
#         self.listenLoop() # wait listening for updates from server
# 
#     def listenLoop(self):
# #         fid = self.fid
#         print("connected")
#         for _ in range(10):
#             with open('/data/projects/pyde/pyde/QsciScintillaCompat.py') as f:
#                 data = f.read()
#                 self.fid.write(data)
# #                 self.fid.write(chr(24))
# #                 self.fid.write(chr(25))
#                 self.fid.write(chr(26))
#                 self.fid.flush()
# #                 self.fid.close()
# #                self.fid.write('\n')
#     #             fid.flush()
#                 start_time = time.time()
#                 line = self.fin.readline()
#                 print(line[0:100])
#                 print(time.time() - start_time)
# #                 self.fin.close()
#     def __del__(self):
#         self.p.kill()
# #                 if line[0]=='.':
# #                     break
# #             fid.write('.\n')
# #             fid.flush()
# 
# if __name__ == '__main__':
# #     import time
# #     import grammars
# #     import os
# #     os.environ['CLASSPATH'] += ':' + os.path.dirname(grammars.__file__)
# # #     io = PipeTextIO('java', ['pyinterface.ParserIntf', 'python3.python3', 'file_input'])
# #     from subprocess import Popen
# #     Popen(['java', 'pyinterface.ParserIntf', 'python3.python3', 'file_input'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
# # #     io = PipeTextIO('java', ['pyinterface.ParserIntf', 'linpath.linpath', 'main'])
# #     import socket
# #     sock = socket.socket()
# #     sock.connect(('127', port))
# #     start_time = time.time()
# # #     io.connect()
# #     print(time.time() - start_time)
#     st = IPC()
# #     rets = []
# #     for _ in range(1):
# #         with open('/data/projects/pyde/pyde/QsciScintillaCompat.py') as f:
# #             data = f.read()
# #             start_time = time.time()
# #             rets.append(io.communicate(data))
# #             print(time.time() - start_time)    
# 
# #     io.f.close()
# #     ret = rets[0]
# #     for r in rets[1:]:
# #         if r != ret:
# # #             dif = list(difflib.Differ().compare(r, ret))
# #             with open('/data/projects/pyde/proba.log', 'w') as f:
# #                 f.write(r)
# #                 f.write('\n')
# #                 f.write(ret)
# #             import sys
# #             sys.exit(0)
# #         else:
# #             print('same')
# #     print(ret)