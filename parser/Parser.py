import json

with open('data/prereqs.json') as infile:
    data = json.load(infile)

output = sorted(data.items(), key=lambda x: len(x[1]['original']))

with open('data/prereqs.json', 'w') as outfile:
    json.dump(output, outfile, indent=4)