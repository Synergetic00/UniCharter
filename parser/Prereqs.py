import json

def parseTrim(string):
    return string.replace('<p>','').replace('</p>','').replace('\u00a0',' ').replace('<div>\\n','').replace('<div>\n','').replace('<br />','').replace("\u2018", "'").replace("\u2019", "'").replace("\u2013", "-").replace("&amp;", "&").strip()

output = {}

# Read from file
with open('data/units.json') as infile:
    data = json.load(infile)

for unit in data:
    output[unit] = {}
    if 'prerequisite' in data[str(unit)]:
        output[unit]['original'] = parseTrim(data[str(unit)]['prerequisite'])

# Write to file
with open('data/prereqs.json', 'w') as outfile:
    json.dump(output, outfile, indent=4, sort_keys=True)