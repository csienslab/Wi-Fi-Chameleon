import time
import os
from wifichameleon.utils.util import requireRoot
from wifichameleon.utils import errors
from wifichameleon.daemons import DaemonMgr
from wifichameleon import config

requireRoot()
daemons = [DaemonMgr(daemon) for daemon in config.DAEMONS]
last_health_check = 0
def healthCheck():
    global last_health_check
    for i in range(len(daemons)):
        trial = 0
        while True:
            if not daemons[i].isRunning():
                daemons[i].restart()
                if daemons[i].isRunning():
                    print(f"{daemons[i]} is running!")
                    break
            else:
                break
            trial += 1
            if trial > 60:
                errors.daemonFailed(daemons[i].name)
                return
            time.sleep(1)
    last_health_check = time.time()

def getStatus():
    status = []
    for i in range(len(daemons)):
        status.append({"name": daemons[i].name, "status": daemons[i].getState()})
    return status

if __name__ == '__main__':
    healthCheck()