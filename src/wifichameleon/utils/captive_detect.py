from urllib.parse import urlparse
import time

def parse_meta(content):
    begin_meta = content.lower().find("meta http-equiv=\"refresh\"")
    if begin_meta == -1:
        begin_meta = content.lower().find("meta http-equiv='refresh'")
    if begin_meta == -1:
        return None
    begin_url = content.lower().find("url=", begin_meta)
    if begin_url == -1:
        return None
    begin_url += 4
    tmp = content[begin_url:]
    end_url = tmp.find("'")
    if end_url == -1:
        end_url = tmp.find("\"")
    if end_url == -1:
        return None
    return tmp[:end_url]

def detect():
    print("[*] Detecting login url")
    # Move to here since requests will take forever to load
    import requests
    trial = 0
    r = None
    while True:
        try:
            r = requests.get("http://captive.apple.com/hotspot-detect.html", allow_redirects=False, timeout=10)
            break
        except:
            trial += 1
            print("[!] Detection failed. Giving another try...")
            time.sleep(3)
            if trial > 3:
                return None
    #if r.status_code != 302:
    if r.status_code < 300 or r.status_code >= 400:
        parsed_meta = parse_meta(r.text)
        if parsed_meta is None:
            return None
        try_parsed = urlparse(parsed_meta)
        if try_parsed.scheme == '' or try_parsed.netloc == '':
            return None
        r = requests.get(parsed_meta, allow_redirects=False, timeout=10)
        if r.status_code < 300 or r.status_code >= 400:
            print(f"[*] Found login URL: {try_parsed.scheme}://{try_parsed.netloc}")
            return (try_parsed.scheme, try_parsed.netloc)
    o = urlparse(r.headers['Location'])
    print(f"[*] Found login URL: {o.scheme}://{o.netloc}")
    return (o.scheme, o.netloc)


if __name__ == '__main__':
    print(detect())