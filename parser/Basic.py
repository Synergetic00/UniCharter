import json
import re

with open('data/sorted.json') as infile:
    data = json.load(infile)

codere = '[A-Z]{4}[0-9]{4}'

output = {}

for entry in data.items():
    unitcode = entry[0]
    prereqs = entry[1]['original']
    codes = re.findall(codere, prereqs)
    output[unitcode] = codes

with open('data/codesonly.json', 'w') as outfile:
    json.dump(output, outfile, indent=4, sort_keys=True)