#!/usr/bin/env python3
import requests
import re

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

matches = re.findall(r"ShowApplicationDetail\('\d+', '(.*?)', '\d+'\);", content, re.MULTILINE)
output = '\n'.join(matches)

with open("file.txt", "w") as file:
    file.write(output)

