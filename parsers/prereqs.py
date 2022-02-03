import json
import re

with open('data/units.json') as file:
    data = json.load(file)

codere = '[A-Z]{4}[0-9]{4}'

output = {}

for entry in data.items():
    unitcode = entry[0]
    output[unitcode] = {}

    prereqs = 'None'
    if 'prerequisite' in data[unitcode]:
        prereqs = entry[1]['prerequisite']
    tokens = re.findall(r'\)|\(|or|and', prereqs)
    output[unitcode]['prereqs'] = prereqs
    
with open('data/prereqs.json', 'w') as outfile:
    json.dump(output, outfile, indent=4, sort_keys=True)