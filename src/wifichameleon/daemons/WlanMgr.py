import subprocess
import os
import time
from ..utils.errors import error

def run(cmd):
    p = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return p.stdout.decode()

def getStatus(interface):
    output = run(f"wpa_cli -i {interface} status")
    status = {}
    for line in output.split("\n"):
        line = line.strip()
        if not '=' in line:
            continue
        key, val = line.split("=")
        status[key] = val
    return status

def disconnect(interface):
    output = run(f"wpa_cli -i {interface} disc")
    return True if "OK" in output else False

def scan(interface):
    APs = []

    # Start scanning
    output = run(f"wpa_cli -i {interface} scan")
    if not "OK" in output and not "BUSY" in output:
        return APs
    
    # Wait for scan result
    time.sleep(3)

    # Get scan result
    output =  run(f"wpa_cli -i {interface} scan_result")
    keys = ["bssid", "frequency", "signal level", "flags", "ssid"]
    for line in output.split("\n")[1:]: # Skip header
        values = line.strip().split("\t")
        if len(values) < len(keys):
            continue
        AP = {}
        for i in range(len(keys)):
            AP[keys[i]] = values[i]
        APs.append(AP)
    return APs

def getNetworks(interface):
    output = run(f"wpa_cli -i {interface} list_n")
    networks = []
    keys = ["network id", "ssid", "bssid", "flags"]
    for line in output.split("\n")[1:]: # Skip header
        values = line.strip().split("\t")
        if len(values) < len(keys) - 1:
            continue
        network = {}
        for i in range(len(values)):
            network[keys[i]] = values[i]
        networks.append(network)
    return networks

def createNetwork(interface, ssid):
    # print(f"[*] creating network {ssid} on interface {interface}")
    output = run(f"wpa_cli -i {interface} add_n")
    networkId = int(output.strip())
    output = run(f"wpa_cli -i {interface} set_n {networkId} ssid \"{ssid}\"")
    if not "OK" in output:
        print(f"wpa_cli -i {interface} set_n {networkId} ssid \"{ssid}\"")
        print(output)
        return -1
    output = run(f"wpa_cli -i {interface} set_n {networkId} scan_ssid 1")
    if not "OK" in output:
        print(f"wpa_cli -i {interface} set_n {networkId} scan_ssid 1")
        print(output)
        return -1
    output = run(f"wpa_cli -i {interface} set_n {networkId} key_mgmt NONE")
    if not "OK" in output:
        print(f"wpa_cli -i {interface} set_n {networkId} key_mgmt NONE")
        print(output)
        return -1
    output = run(f"wpa_cli -i {interface} enable_n {networkId}")
    if not "OK" in output:
        print(f"wpa_cli -i {interface} enable_n {networkId}")
        print(output)
        return -1
    return networkId

def connect(interface, ssid):
    status = getStatus(interface)
    if status["wpa_state"] == "COMPLETED" and status["ssid"] == ssid:
        print(f"[*] Interface {interface} already connected to {ssid}")
        return True
    print(f"[*] connecting to {ssid} on interface {interface}")
    networks = getNetworks(interface)
    networkId = -1
    for network in networks:
        if network['ssid'] == ssid:
            networkId = network['network id']
            break
    if networkId == -1:
        networkId = createNetwork(interface, ssid)
    if networkId == -1:
        error("No network available")
        return False
    output = run(f"wpa_cli -i {interface} select_n {networkId}")
    if not "OK" in output:
        error(f"Select network {networkId} failed")
        return False
    # wait for 5 seconds for connection
    for _ in range(5):
        # print(".")
        time.sleep(1)
        status = getStatus(interface)
        if status["wpa_state"] != "COMPLETED":
            continue
        if status["ssid"] == ssid:
            print(f"[*] Interface {interface} connected to {ssid}")
            return True
    error("Connection failed")
    return False
    

if __name__ == '__main__':
    connect("wlan1", "NTU")