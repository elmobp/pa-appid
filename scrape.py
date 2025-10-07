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
print(content)
soup = BeautifulSoup(content, "html.parser")
table = soup.find(id="bodyScrollingTable")
child_elements = table.find_all("tr")

services = {}

# Iterate over the table rows
for i in range(len(child_elements)):
    td_elements = child_elements[i].find_all("td")

    service_strip = td_elements[0].get_text().strip().replace(" ", "")
    category = td_elements[1].get_text().strip().replace(" ", "")
    subcategory = td_elements[2].get_text().strip().replace(" ", "")

    services[service_strip] = {}
    if td_elements[3].find("img"):
        risk = td_elements[3].find("img")["title"]
        services[service_strip]["risk"] = risk

    technology = td_elements[4].get_text().strip().replace(" ", "")
    services[service_strip]["category"] = category
    services[service_strip]["subcategory"] = subcategory
    services[service_strip]["technology"] = technology

    b = i
    elem_size = int(child_elements[i].get("ottawagroup"))
    if elem_size == 1:
        services[service_strip]["subapplications"] = {}
        b += 1
        while int(child_elements[b].get("ottawagroup")) == 2:
            name = child_elements[b].find_all("td")[0].get_text().strip().replace(" ", "")
            category = child_elements[b].find_all("td")[1].get_text().strip().replace(" ", "")
            subcategory = child_elements[b].find_all("td")[2].get_text().strip().replace(" ", "")
            service = {}

            if child_elements[b].find_all("td")[3].find("img"):
                risk = child_elements[b].find_all("td")[3].find("img")["title"]
                service["risk"] = risk

            technology = child_elements[b].find_all("td")[4].get_text().strip().replace(" ", "")
            service["category"] = category
            service["subcategory"] = subcategory
            service["technology"] = technology

            services[service_strip]["subapplications"][name] = [service]
            b += 1

# Convert services dictionary to JSON
j = json.dumps(services, indent=4)

# Write JSON to file
with open("appid.txt", "w") as fh:
    fh.write(j)
