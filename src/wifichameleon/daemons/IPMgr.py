import subprocess
import os
import netifaces
from ..utils.util import isRoot
from ..utils.errors import error

def getInterfaces():
  return netifaces.interfaces()

def getIP(interface):
  try:
    addrs = netifaces.ifaddresses(interface)
    inet_addrs = addrs[netifaces.AF_INET]
    return inet_addrs[0]['addr']
  except KeyError:
    return None
  except ValueError:
    # TODO: print invalid interface msg
    return None

def setIP(interface, ip):
  if not isRoot():
    # TODO: ask for privilege
    print("You are not admin!")
    exit()
  p = subprocess.run(["ip", "addr", "flush", "dev", interface])
  if p.returncode != 0:
    error(f"Flushing interface {interface} address fail!")
  p = subprocess.run(["ip", "addr", "change", ip, "dev", interface])
  if p.returncode != 0:
    error(f"Setting interface {interface} address fail!")
  

if __name__ == '__main__':
  setIP("enp0s8", "10.1.0.1/24")