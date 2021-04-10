
def remove(string, start, length):
    output = string[0 : start] + string[start + length:]
    return output

string = 'Michelle Violet Banks'

print(remove(string, 3, 3))

def splitParenstheses(string):
    groups = {}

    depth = 0
    first = 0
    ignoreNext = False

    for i in range(len(string)):
        char = string[i]
        valid = (i - 1) > 0
        prev = string[i - 1] if valid else None

        if char == '(':
            if prev != None:
                prevltr = prev.isalpha()
                if prevltr:
                    ignoreNext = True
            if not ignoreNext:
                if depth == 0:
                    first = i
                depth += 1
        elif char == ')':
            if ignoreNext:
                ignoreNext = False
            else:
                depth -= 1
            if depth == 0:
                sublen = (i+1) - first
                group = string[first:sublen]
                if group[0] == '(':
                    group = group[1:-1]
                firstopen = group.index('(')
                further = False

                if firstopen >= 1:
                    prevopen = group[firstopen-1]
                    if char.isalpha():
                        further = True
                    else:
                        if group.count('(') > 1:
                            further = True
                
                firstrange = range(first, i)
                hashcode = hash(group) + hash(range)
                groups.update({hashcode, 1})
    return groups