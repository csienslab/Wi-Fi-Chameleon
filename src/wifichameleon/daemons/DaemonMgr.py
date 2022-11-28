import subprocess
import os
from ..utils.util import isRoot
from ..utils import errors as errors


OK, DEAD_RUN, DEAD_LOCK, NOT_RUNNING, UNKNOWN = range(5)

class DaemonMgr:
    '''Manager class for general system daemons'''

    def __init__(self, name, log_path="", _args=None):
        if not isRoot():
            errors.notRoot()
            exit(-1)
        self.name = name
        self.log_path = log_path
        self.state = None
        
        # Static Member
        if _args is not None:
            args = _args
    
    def getState(self):
        '''Retrieve daemon status using systemctl command'''

        p = subprocess.run(["systemctl", "status", self.name], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        output = p.stdout.decode()
        activeIdx = output.find("Active: ")+8
        statusEnd = output[activeIdx:].find(" ")
        _status = output[activeIdx:activeIdx+statusEnd]
        self.state = {
            "exists": p.returncode != UNKNOWN,
            "status": 0 if _status == "active" else 1
        }
        return _status;

    def restart(self):
        '''Restart daemon using systemctl command'''

        subprocess.run(["systemctl", "restart", self.name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def stop(self):
        subprocess.run(["systemctl", "stop", self.name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def setConf(self):
        raise NotImplementedError("Abstract method")
    
    def getLog(self, line):
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r') as infile:
                lines = infile.readline()
                return lines[-1*line:]
    
    def isRunning(self):
        self.getState()
        return self.state["status"] == OK
