import subprocess as sub
import threading
import commands
import time
from subprocess import Popen, PIPE

class RunCmd(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout
        self.output = ''
        self.err = ''
        self.time = 0.0

    def run(self):
        start = time.time()
        self.p = sub.Popen(self.cmd,stdin=PIPE, stdout=PIPE, stderr=PIPE,shell=True)
        self.time = time.time() - start
        self.output,self.err = self.p.communicate()
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()      #use self.p.kill() if process needs a kill -9
            self.join()

#command = RunCmd(["while true; do echo 'Ctrl c to kill'; sleep 1; done"], 10)
#command = RunCmd(["pwd"], 10)
#command.Run()
#print command.output,command.err