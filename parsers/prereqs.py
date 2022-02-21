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
    parsed = re.sub(r' ?\(|\)| or | and | including', '|', parsed)
    parsed = parsed.split('|')
    output.append(parsed[0])
    for i in range(len(tokens)):
        output.append(tokens[i].strip())
        output.append(parsed[i+1].strip())
    output = list(filter(None, output))
    return output

highest = []

def getParsedArr(prereqs):
    tokens = re.findall(r'\)|\(| or | and | including', prereqs)
    tokens = [token.strip() for token in tokens]
    return splitPrereqs(prereqs, tokens)

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
        prereqs = prereqs.replace('(Hons)', ' - Honours ')
        prereqs = prereqs.replace('(Prim)', ' - Primary ')
        prereqs = prereqs.replace('(Sec)', ' - Secondary ')
        prereqs = re.sub(r'  +', ' ', prereqs)
    else:
        output[unitcode]['prereqs'] = 'None'
        continue # don't go futher, nothing to analyse
    output[unitcode]['prereqs'] = prereqs
    # arr = getParsedArr(prereqs)
    # depth = 0
    # result = []
    # current = []
    # for element in arr:
    #     if element == '(':
    #         depth += 1
    #     elif element == ')':
    #         depth -= 1
    #     else:
    #         current.append(element)
    #         print(depth, element)
    # print(result)
    # highest.append([len(arr), unitcode, arr])
    # output[unitcode]['prereqs'] = prereqs

# from ast import literal_eval
import json

def getDepthParsedArr(arr):
    strconv = str(arr)
    strconv = strconv.replace('\'(\'','[')
    strconv = strconv.replace('\')\'',']')
    strconv = strconv.replace('\'', '"')
    strconv = strconv.replace('[, [', '[[')
    strconv = strconv.replace('[, "', '["')
    strconv = strconv.replace(', ]', ']')
    output = json.loads(strconv)
    return output
    # output = []
    # depth = 0
    # for element in arr:
    #     if element == '(':
    #         current = []
    #         depth += 1
    #     elif element == ')':
    #         print(current)
    #         current = []
    #         depth -= 1
    #     else:
    #         current.append(element)
    #         print(depth, element)
    # return output

arr = getParsedArr('((ELEC2040 or ELEC240) and (MATH235 or MATH2055)and (TELE3001 or STAT394)) or admission to MEngElecEng or MEngNetTeleEng')
print(getDepthParsedArr(arr))

# sorted = sorted(highest, key=lambda x:x[0])
# print(sorted[-1][2])
    
with open('data/prereqs.json', 'w') as outfile:
    json.dump(output, outfile, indent=4, sort_keys=True)