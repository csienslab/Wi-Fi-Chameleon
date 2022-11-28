import os
import dpkt
from ..config import PROJ_ROOT, DHCP_CLIENT_LEASE_PATH, DHCP_SERVER_CONF_PATH
from ..utils.util import convertIP, isRoot
from ..utils import errors as errors

def ascii_sum(s):
    _sum = 0
    for c in s:
        if c.isalnum():
            _sum += ord(c)
    return _sum

def similar(s1, s2):
    chunks = s2.split(" ")
    similar = True
    for chunk in chunks:
        if chunk not in chunks:
            similar = False
    return similar

def parseLeaseDNS(interface, AP):
    leases = os.listdir(DHCP_CLIENT_LEASE_PATH)
    possibles = []
    _lease = None
    for lease in leases:
        if similar(lease, f"{interface}-{AP}.lease"):
            possibles.append(lease)
    try:
        for lease in possibles:
            #print()
            _lease = open(DHCP_CLIENT_LEASE_PATH+lease, 'rb').read()
            break
    except FileNotFoundError:
        pass
    if _lease is None:
        errors.noFile(DHCP_CLIENT_LEASE_PATH+f"{interface}-{AP}.lease")
        exit()
    lease = _lease    
    parsed = dpkt.dhcp.DHCP(lease)
    dns = None
    for opt in parsed.opts:
        if opt[0] == 6:
            dns = opt[1]
    dns = [convertIP(dns[i:i+4]) for i in range(0, len(dns), 4)]
    return dns

def setConfDNS(dns):
    if not isRoot():
        errors.notRoot()
        exit()
    conf = open(PROJ_ROOT+"conf/dhcpd.conf", 'r').read()
    dns_str = ", ".join(dns)
    new_conf = conf.replace("$DNS_SERVER$", dns_str)
    open(DHCP_SERVER_CONF_PATH, 'w').write(new_conf)
    return True

if __name__ == '__main__':
    dns = parseLeaseDNS("wlan1", "NTU")
    setConfDNS(dns)