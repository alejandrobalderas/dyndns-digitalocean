import requests
import os
import json

domain = "balderas.de"
subdomain = "*"
apikey = os.environ["apikey"]

url = f"https://api.digitalocean.com/v2/domains/{domain}/records"
headers = {
    "Authorization": f"Bearer {apikey}",
    "Content-Type": "application/json"
    }
params = {"type": "A", "name": f"{subdomain}.{domain}"}

r = requests.get(url, headers=headers, params=params)
record_id = r.json()["domain_records"][0]["id"]
record_ip = r.json()["domain_records"][0]["data"]
record_url = url + f"/{record_id}"

current_ip = requests.get("https://ifconfig.me").text

if current_ip != record_ip:
    update_ip = {"data": f"{current_ip}"}
    r = requests.put(record_url, headers=headers, data=json.dumps(update_ip))
else:
    print("No change made")


class Dyndns:

    def __init__(self, domain:str, subdomain:str = None, apikey:str=None) -> None:
        self.url = f"https://api.digitalocean.com/v2/domains/{self.domain}/records"
        self.headers = {
            "Authorization": f"Bearer {apikey}",
            "Content-Type": "application/json"
            }
        self.record_id = None
        self.current_ip = None

    def get_record_info(self):
        params = {"type": "A", "name": f"{subdomain}.{domain}"}
        r = requests.get(url, headers=headers, params=params)
        self.record_id = r.json()["domain_records"][0]["id"]
