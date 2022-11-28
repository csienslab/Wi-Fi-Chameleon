from .DaemonMgr import DaemonMgr

class MitmMgr(DaemonMgr):
    def __init__(self):
        super().__init__("mitm")