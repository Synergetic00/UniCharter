import json
# Read from file
with open('data/units.json') as infile:
    data = json.load(infile)

for unit in data:
    if 'prerequisite' in data[str(unit)]:
        original = data[str(unit)]['prerequisite']
        original = original.replace(chr(160), chr(32))
        for char in original:
            num = ord(char)
            if num > 127:
                print(num)