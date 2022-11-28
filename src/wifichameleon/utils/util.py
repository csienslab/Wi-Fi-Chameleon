import os
import json
from . import errors
from .. import config

def isRoot():
    return os.geteuid() == 0

def requireRoot():
    if not isRoot():
        errors.notRoot()
        exit(-1)

def convertIP(ip, type=0):
    # Bytes to str
    if type == 0:
        return f"{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}"

def write_settings(settings):
    with open(config.SETTINGS_PATH, 'w') as ofile:
        ofile.write(json.dumps(settings))

def read_settings():
    try:
        with open(config.SETTINGS_PATH, 'r') as ifile:
            return json.loads(ifile.read())
    except FileNotFoundError:
        errors.noFile(config.SETTINGS_PATH)
        exit()

def set_config(key, val):
    configs = {}
    config_path = config.PROJ_ROOT+"src/wifichameleon/config.py"
    with open(config_path, 'r') as infile:
        for line in infile.read().split("\n"):
            if "=" not in line:
                continue
            _key, _val = line.split("=")
            configs[_key] = _val
    configs[key] = val
    with open(config_path, 'w') as ofile:
        for _key in configs.keys():
            ofile.write(f"{_key}={configs[_key]}\n")

def safe_read(file):
    try:
        with open(file, 'r') as ifile:
            return ifile.read()
    except:
        return ""

def safe_json_loads(text):
    try:
        got = json.loads(text)
        return got
    except:
        return {}

def safe_decode(some_bytes):
    try:
        return some_bytes.decode()
    except:
        return "".join([chr(n) if n < 0x80 else f"%{hex(n)[2:]}" for n in some_bytes])

def load_password():
    id_to_data = {}
    raw_data = safe_read(config.PROJ_ROOT+config.PASSWORD_LOG)
    for line in raw_data.split("\n"):
        if "id" not in line:
            continue
        data = json.loads(line)
        id_to_data[data['id']] = data
    return id_to_data

def save_password(id_to_data):
    with open(config.PROJ_ROOT+config.PASSWORD_LOG, 'w') as ofile:
        for key in id_to_data.keys():
            ofile.write(json.dumps(id_to_data[key]))
            ofile.write("\n")

def hide_password(_id):
    old_passwords = load_password()
    if _id not in old_passwords:
        return False
    else:
        old_passwords[_id]['hide'] = 1
    save_password(old_passwords)
    return True

def delete_password(_id):
    old_passwords = load_password()
    if _id not in old_passwords:
        return False
    else:
        del old_passwords[_id]
    save_password(old_passwords)
    return True