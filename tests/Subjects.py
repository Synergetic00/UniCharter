import json
import re

with open('data/units.json') as infile:
    data = json.load(infile)

regex = '^[a-zA-Z]{4}[0-9]{4}$'

subjects = {''}

for label in data:
    code = label[0:4]
    subjects.add(code)

subjects.remove('')

print(sorted(subjects))