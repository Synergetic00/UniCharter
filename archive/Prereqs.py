import json
import re

def parseTrim(string):
    return string.replace('<p>','').replace('</p>','').replace('\u00a0',' ').replace('<div>\\n','').replace('<div>\n','').replace('<br />','').replace("\u2018", "'").replace("\u2019", "'").replace("\u2013", "-").replace("&amp;", "&").strip()

def remove(string, start, length):
    output = string[0 : start] + string[start + length:]
    return output

def make_tree(data):
    output = data.replace("(", "[")\
             .replace(")", "]")\
             .replace("] [", "], [")
    return output

def splitData(string):
    output = {}
    andsplit1 = string.split(' and ')
    for and1 in range(len(andsplit1)):
        output['and'+str(and1)] = andsplit1[and1]
    return output

output = {}

# Regex
cps = "\w+ at \w+ level or above"
adm = "^Admission to .*"

# Read from file
with open('data/units.json') as infile:
    data = json.load(infile)

for unit in data:
    output[unit] = {}
    if 'prerequisite' in data[str(unit)]:
        original = parseTrim(data[str(unit)]['prerequisite'])
        output[unit]['original'] = original

# Write to file
with open('data/prereqs.json', 'w') as outfile:
    json.dump(output, outfile, indent=4, sort_keys=True)