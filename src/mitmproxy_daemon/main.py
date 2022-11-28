import sys
import os
import subprocess
import time

base = os.path.abspath(os.path.join(__file__,  ".."))
scripts = ["handle_location.py", "handle_meta.py"]

p = subprocess.run(
    f"iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080".split(" "),
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
)

try:
    cmd = "mitmdump --mode transparent" + "".join([f" -s {base}/{script}" for script in scripts]) # + " -q"
    s = subprocess.run(cmd.split(" "), stderr=subprocess.DEVNULL)
except:
    print("[!] Some error happened, exiting...")
    subprocess.run(
        "iptables -t nat -F PREROUTING".split(), 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )