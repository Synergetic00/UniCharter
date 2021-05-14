import json
import re

# Read from file
with open('data/units.json') as infile:
    data = json.load(infile)

justCredits = '^[0-9]{2,3}cp at [0-9]{4} level or above$'

total = 0

for unit in data:
    if 'prerequisite' in data[str(unit)]:
        original = data[str(unit)]['prerequisite']
        original = original.replace(chr(160), chr(32))
        if re.match(justCredits, original):
            total += 1
        

print(str(total)+" / 2488")