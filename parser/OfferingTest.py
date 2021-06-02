import json

with open('data/units.json') as infile:
    data = json.load(infile)

for item in data:
    offered = False
    if 'offerings' in data[item]:
        for offering in data[item]['offerings']:
            text = data[item]['offerings'][offering]
            if '3' in text['period']: #Offered in Session 3
                offered = True
    if offered and item[4] is '1': #Is a first year unit
        print(item)