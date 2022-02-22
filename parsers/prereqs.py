import json
import re

with open('data/units.json') as file:
    data = json.load(file)

codere = '[A-Z]{4}[0-9]{4}'
output = {}

def splitPrereqs(prereq, tokens):
    output = []
    parsed = str(prereq)
    parsed = parsed.replace('(or', 'or (') # fix a single error
    parsed = re.sub(r' ?\(|\)| or | and | including', '|', parsed)
    parsed = parsed.split('|')
    output.append(parsed[0])
    for i in range(len(tokens)):
        output.append(str(tokens[i]).strip())
        output.append(parsed[i+1].strip())
    output = list(filter(None, output))
    return output

def getParsedArr(prereqs):
    lowered = str(prereqs).lower()
    tokens = re.findall(r'\)|\(| or | and | including', lowered)
    tokens = [token.strip() for token in tokens]
    return splitPrereqs(prereqs, tokens)

def getDepthParsedArr(arr):
    strconv = str(arr)
    strconv = strconv.replace('\'(\'','[')
    strconv = strconv.replace('\')\'',']')
    strconv = strconv.replace('\'', '"')
    strconv = strconv.replace('[, [', '[[')
    strconv = strconv.replace('[, "', '["')
    strconv = strconv.replace(', ]', ']')
    strconv = strconv.replace('[, [', '[[')
    output = list(json.loads(strconv))
    return output

for entry in dict(data).items():
    unitcode = entry[0]
    output[unitcode] = {}
    if 'prerequisite' in data[unitcode]:
        prereqs = str(entry[1]['prerequisite'])
        prereqs = prereqs.replace('[', '(')
        prereqs = prereqs.replace(']', ')')
        # prevent parsing errors
        prereqs = prereqs.replace('and above', 'minimum')
        prereqs = prereqs.replace('or above', 'minimum')
        prereqs = prereqs.replace('(P)', ' >= 50')
        prereqs = prereqs.replace('(Cr)', ' >= 65')
        prereqs = prereqs.replace('(D)', ' >= 75')
        prereqs = prereqs.replace('(HD)', ' >= 85')
        prereqs = prereqs.replace('(S)', ' - S')
        prereqs = prereqs.replace('(Hons)', ' - Honours ')
        prereqs = prereqs.replace('(Prim)', ' - Primary ')
        prereqs = prereqs.replace('(Sec)', ' - Secondary ')
        prereqs = prereqs.replace('(0-12)', ' - BirthTo12 ')
        prereqs = prereqs.replace('(ECE)', ' - EarlyChildhood ')
        prereqs = prereqs.replace('OR', 'or')
        prereqs = prereqs.replace('AND', 'and')
        prereqs = re.sub(r'  +', ' ', prereqs)
        # single parsing errors
        prereqs = prereqs.replace('(ANTH150 or ANTH1050) or (40cp at 1000 level minimum', '(ANTH150 or ANTH1050) or 40cp at 1000 level minimum') # ANTH2003
        prereqs = prereqs.replace('(BIOL8770 or BIOL877) or BIOL8870 or BIOL887)', '(BIOL8770 or BIOL877) or (BIOL8870 or BIOL887)') # BIOL8710
        prereqs = prereqs.replace('(BTeach - EarlyChildhood )', '(BTeach - EarlyChildhood))') # EDST3160
        prereqs = prereqs.replace('(TEP401 or EDTE4010 - S)', '((TEP401 or EDTE4010 - S)') # EDTE4260
        prereqs = prereqs.replace('(((TEP401 or EDTE4010 - S)', '((TEP401 or EDTE4010 - S)')
        prereqs = prereqs.replace('((ELCT3005 or ELEC395)', '(ELCT3005 or ELEC395)') # ELEC4092
        prereqs = prereqs.replace('130cp at 1000 level minimum including HLTH200 or HLTH2000) or 130cp and admission to BHumanSc', '(130cp at 1000 level minimum including HLTH200 or HLTH2000) or (130cp and admission to BHumanSc)') # HLTH3100
        prereqs = prereqs.replace('(MMCC2014 or MAS214) or (BUSL250 and BUSL301)', '(MMCC2014 or MAS214) or BUSL250 and BUSL301)') # LAWS5023
        prereqs = prereqs.replace('Admission to LLM or MIntTrdeComLaw or M', '(Admission to LLM or MIntTrdeComLaw or M') # LAWS8018
        prereqs = prereqs.replace('BSpHScBPsych - Honours or DipSphComm)', 'BSpHScBPsych - Honours or DipSphComm))') # PSYU2235
        prereqs = prereqs.replace('STAX1103)) or ((COGS100 or COGS1000) or (MEDI204', 'STAX1103) or ((COGS100 or COGS1000) or (MEDI204') # PSYU2236
        prereqs = prereqs.replace('or PSY248 or PSYU2248 or PSYX248 or PSYX2248))', 'or PSY248 or PSYU2248 or PSYX248 or PSYX2248)))') # PSYU3349
        prereqs = prereqs.replace('or BHumanSc))', 'or BHumanSc)') # PSYU3399
        prereqs = prereqs.replace('SPED8260)', 'SPED8260') # SPED8901
        prereqs = prereqs.replace('PSYU2248))', 'PSYU2248)))') # STAT3102
        prereqs = prereqs.replace('ECON8040))or', 'ECON8040) or') # STAT8111
    else:
        output[unitcode]['prereqs'] = 'None'
        continue # don't go futher, nothing to analyse
    # output[unitcode]['prereqs'] = prereqs
    arr = getParsedArr(prereqs)
    depthArr = getDepthParsedArr(arr)
    output[unitcode]['prereqs'] = depthArr

with open('data/prereqs.json', 'w') as outfile:
    json.dump(output, outfile, indent=4, sort_keys=True)