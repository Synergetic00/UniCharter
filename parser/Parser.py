import json
import re

with open('data/sorted.json') as infile:
    data = json.load(infile)

justcps = '^[0-9]{2,3}cp$'

for entry in data.items():
    code = entry[0]
    prereqs = entry[1]['original']

    if re.match(justcps, prereqs):
        print(prereqs)