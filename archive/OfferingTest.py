import json

with open('data/prereqs.json') as infile:
    data = json.load(infile)

output = {}

for item in data:
    if 'original' in data[item]:
        offering = data[item]['original']
        print(len(offering))