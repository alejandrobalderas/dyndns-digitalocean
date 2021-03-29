import requests
import os
import json
import time
from typing import List

apikey = os.environ["apikey"]

last_ip = current_ip = "0.0.0.0"
current_ip = requests.get("http://ifconfig.me").text

domains = {
    "balderas.de": [
        "*",
        "manage",
        "server",
        "cloud"
    ],
    "balderas-home.com": [
        "example",
        "example2"
    ]
}

headers = {
    "Authorization": f"Bearer {apikey}",
    "Content-Type": "application/json"
}
    
params = {
    "type": "A",
}


def get_record_ids(do_url:str, subdomains:List[str]) -> List[str]:
    response = requests.get(do_url, headers=headers, params=params)
    response = response.json()["domain_records"]
    return [record["id"] for record in response if record["name"] in subdomains]

def get_record_urls(domain:str, subdomains:List[str]) -> List[str]:
    do_url = f"https://api.digitalocean.com/v2/domains/{domain}/records"   
    record_ids = get_record_ids(do_url, subdomains)
    return [do_url + f"/{record_id}" for record_id in record_ids]    

def update_record_ids(record_urls:List[str], new_ip: str) -> None:
    new_ip = {"data": f"{new_ip}", "ttl": 60}
    for record_url in record_urls:
        r = requests.put(record_url, headers=headers, data=json.dumps(new_ip))
        if r.status_code == 200:
            print(f"Changed record for {record_url} to IP {new_ip['data']}")

while True:

    if current_ip != last_ip:
        print("Changing IPs")
        domain_urls = {}
        for domain, subdomains in domains.items():
            record_urls = get_record_urls(domain, subdomains)        
            update_record_ids(record_urls, current_ip)
        last_ip = current_ip
    time.sleep(60)
    current_ip = requests.get("http://ifconfig.me").text


