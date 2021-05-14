import json
import re

with open('data/prereqs.json') as infile:
    data = json.load(infile)

arr = []

for unit in data:
    prereq = data[str(unit)]['original'] if 'original' in data[str(unit)] else 'None'
    arr.append(unit+'|'+prereq)
    

output = '\n'.join(arr)

with open('data/codes.csv', 'w') as outfile:
    outfile.write(output)