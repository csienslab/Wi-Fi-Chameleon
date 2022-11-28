HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def notRoot():
    error("Please run this script with root privilege.")

def noModule(name):
    error(f"Module: {name} not found. Please install it with pip.")

def noFile(name):
    error(f"File:{name} not found.")

def daemonFailed(name):
    error(f"Daemon: {name} failed. Check daemon status with 'sudo systemctl status {name}' command.")

def error(msg):
    print("[!] " + msg)