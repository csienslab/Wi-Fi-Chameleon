from .DaemonMgr import DaemonMgr
from ..config import PROJ_ROOT
import os

class DnsmasqMgr(DaemonMgr):
    def __init__(self):
        super().__init__("dnsmasq")
        self.conf_path = "/etc/dnsmasq.conf"
        self.template_path = PROJ_ROOT+"conf/dnsmasq.conf.template"
        self.default_domains = [
            ("wifi-chameleon.edu.tw", "10.1.0.1")
        ]
    
    def setConf(self, domains=[], add_default_domains=True):
        new_domains = (self.default_domains + domains) if add_default_domains else domains
        with open(self.template_path, 'r') as infile:
            template = infile.read()
            if template.find("$ADDRESS$") == -1:
                # throw invalid template error
                print("[!] Dnsmasq template file is invalid")
                exit(-1)
    
        address = "\n".join([f"address=/{domain[0]}/{domain[1]}" for domain in new_domains])
        conf = template.replace("$ADDRESS$", address)
        with open(self.conf_path, 'w') as ofile:
            ofile.write(conf)