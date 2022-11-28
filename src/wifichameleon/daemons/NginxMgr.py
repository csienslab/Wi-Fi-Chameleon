from .DaemonMgr import DaemonMgr
from ..config import PROJ_ROOT
import os

class NginxMgr(DaemonMgr):
    def __init__(self):
        super().__init__("nginx")
        self.enabled_path = "/etc/nginx/sites-enabled/"
        self.available_path = "/etc/nginx/sites-available/"
        self.default_enabled = []
    
    def get_path(self, site):
        return self.available_path + site, self.enabled_path + site
    
    def add_site(self, site, config):
        self.remove_site(site)
        with open(self.available_path + site, 'w') as ofile:
            ofile.write(config)
        self.enable_site(site)
    
    def remove_site(self, site):
        for file in self.get_path(site):
            try:
                os.remove(file)
            except:
                pass
    
    def disable_site(self, site):
        try:
            os.remove(self.enabled_path + site)
        except:
            pass
    
    def enable_site(self, site):
        site_avail, site_enable = self.get_path(site)
        if os.path.isfile(site_enable):
            return
        os.symlink(site_avail, site_enable)
    
    def enable_default(self):
        for site in self.default_enabled:
            self.enable_site(site)

    def disable_all(self):
        for site in os.listdir(self.enabled_path):
            self.disable_site(site)
    
    def set_redirection_location(self, url):
        site_avail, site_enable = self.get_path("default")
        template = ""
        with open(PROJ_ROOT+"conf/default", "r") as f:
            template = f.read()
        with open(site_avail, "w") as f:
            f.write(template.replace("http://portal.wifi-chameleon.edu/", url))
        self.enable_site("default")

    def set_portal_configs(self, config_string):
        site_avail, site_enable = self.get_path("portal")
        template = ""
        with open(PROJ_ROOT+"conf/portal", "r") as f:
            template = f.read()

        with open(site_avail, "w") as f:
            f.write(template.replace("$CONFIG$", config_string))
