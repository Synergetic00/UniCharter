import json
import re

def parseTrim(string):
    return string.replace('<p>','').replace('</p>','').replace('\u00a0',' ').replace('<div>\\n','').replace('<div>\n','').replace('<br />','').replace("\u2018", "'").replace("\u2019", "'").replace("\u2013", "-").replace("&amp;", "&").strip()

def splitParenstheses(string):
    depth = 0
    first = 0
    ignoreNext = False

    for i in range(len(string)):
        char = string[i]
        valid = (i - 1) > 0
    return string

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

        append = True

        original = parseTrim(data[str(unit)]['prerequisite'])
        if unit == 'EDTE3010':
            print("Started")

        #if re.match(adm, original):
            #print(original)
        
        if re.match(cps, original):
            if re.match('^'+cps+'$', original):
                output[unit]['generalCredits'] = {}
                cpsArgs = original.split(' ')
                output[unit]['generalCredits']['minCredits'] = re.sub(r'[a-z]+', '', cpsArgs[0], re.I)
                output[unit]['generalCredits']['minLevel'] = re.sub(r'[a-z]+', '', cpsArgs[2], re.I)
                append = False
                #print(original)
            if 'including' in original:
                includes = original.split(' including ')
                output[unit]['generalCredits'] = {}
                cpsArgs = includes[0].split(' ')
                output[unit]['generalCredits']['minCredits'] = re.sub(r'[a-z]+', '', cpsArgs[0], re.I)
                output[unit]['generalCredits']['minLevel'] = re.sub(r'[a-z]+', '', cpsArgs[2], re.I)
                #print(includes)
        
        # Save original string to file
        if append:
            output[unit]['original'] = original

# Write to file
with open('data/prereqs.json', 'w') as outfile:
    json.dump(output, outfile, indent=4, sort_keys=True)