import json

with open('data/prereqs.json') as infile:
    data = json.load(infile)

sorteddict = sorted(data.items(), key=lambda x: len(x[1]['original']))

output = {}

for entry in sorteddict:
    output[entry[0]] = {}
    output[entry[0]]['original'] = data[entry[0]]['original']

with open('data/sorted.json', 'w') as outfile:
    json.dump(output, outfile, indent=4)