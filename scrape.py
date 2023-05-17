#!/usr/bin/env python3
import requests
import json
from bs4 import BeautifulSoup

url = "https://applipedia.paloaltonetworks.com/Home/GetApplicationListView"
data = {
    "category": "",
    "subcategory": "",
    "technology": "",
    "risk": "",
    "characteristic": "",
    "searchstring": ""
}

response = requests.post(url, data=data)
content = response.text

soup = BeautifulSoup(content, 'html.parser')
table = soup.find(id="bodyScrollingTable")
child_elements = table.find_all('tr')

services = {}

for i in range(len(child_elements)):
    service_strip = child_elements[i].find_all('td')[0].get_text().strip().replace(' ', '')
    services[service_strip] = []

    elem_size = int(child_elements[i].get('ottawagroup'))

    if elem_size == 1:
        b = i + 1
        while int(child_elements[b].get('ottawagroup')) == 2:
            service = child_elements[b].find_all('td')[0].get_text().strip().replace(' ', '')
            services[service_strip].append(service)
            b += 1

j = json.dumps(services, indent=4)

with open("appid.txt", "w") as file:
    file.write(j)

