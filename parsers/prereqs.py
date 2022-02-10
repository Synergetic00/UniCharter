import json
import re

with open('data/units.json') as file:
    data = json.load(file)

codere = '[A-Z]{4}[0-9]{4}'
output = {}

def splitPrereqs(prereq, tokens):
    output = []
    parsed = prereq
    parsed = parsed.replace('(or', 'or (') # fix a single error
    parsed = re.sub(r' ?\(|\)| or | and ', '|', parsed)
    parsed = parsed.split('|')
    output.append(parsed[0])
    for i in range(len(tokens)):
        output.append(tokens[i].strip())
        output.append(parsed[i+1].strip())
    output = list(filter(None, output))
    return output

highest = []

for entry in data.items():
    unitcode = entry[0]
    output[unitcode] = {}

    if 'prerequisite' in data[unitcode]:
        prereqs = entry[1]['prerequisite']
        # prevent parsing errors
        prereqs = prereqs.replace('and above', 'minimum')
        prereqs = prereqs.replace('or above', 'minimum')
        prereqs = prereqs.replace('(P)', '>= 50')
        prereqs = prereqs.replace('(Cr)', '>= 65')
        prereqs = prereqs.replace('(D)', '>= 75')
        prereqs = prereqs.replace('(HD)', '>= 85')
    else:
        output[unitcode]['prereqs'] = 'None'
        continue # don't go futher, nothing to analyse
    tokens = re.findall(r'\)|\(| or | and ', prereqs)
    tokens = [token.strip() for token in tokens]
    arr = splitPrereqs(prereqs, tokens)
    highest.append([len(arr), unitcode, arr])
    output[unitcode]['prereqs'] = prereqs

sorted = sorted(highest, key=lambda x:x[0])
print(sorted[-1][2])
    
with open('data/prereqs.json', 'w') as outfile:
    json.dump(output, outfile, indent=4, sort_keys=True)