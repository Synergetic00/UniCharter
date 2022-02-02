import re

def parseInput(string):
    output = string
    output = output.replace('<p>','')
    output = output.replace('</p>','')
    output = output.replace('\u00a0',' ')
    output = output.replace('<div>\\n','')
    output = output.replace('<div>\n','')
    output = output.replace('<br />','')
    output = output.replace('\u202f', ' ')
    output = output.replace('\u2022', '-')
    output = output.replace('\u2026', '...')
    output = output.replace('\u2018', '\'')
    output = output.replace('\u2019', '\'')
    output = output.replace('\u201c', '\'')
    output = output.replace('\u201d', '\'')
    output = output.replace('\u2014', '-')
    output = output.replace('\u2013', '-')
    output = output.replace('\t', ' ')
    output = output.replace('\n', ' ')
    output = output.replace('&amp;', '&')
    output = output.replace('\u037e', ';')
    output = output.replace('\u00f6', 'o')
    output = output.replace('\u200b', '')
    output = output.replace('\uf0a7', '-')
    output = output.replace('\uf0a7', '-')
    output = output.replace('\u00e2', '')
    output = output.replace('\u20ac', '')
    output = output.replace('\u02dc', '')
    output = output.replace('\u00b1', '+/-')
    output = output.replace('\u00b7', '-')
    output = output.replace('\u00d7', '*')
    output = output.replace('\u2028', '') # LINE SEPERATOR
    output = output.replace('\u2028', '-') # SOFT HYPHEN
    output = output.replace('\u00ad', '-') # SOFT HYPHEN
    output = output.replace('\u25e6', '-') # WHITE BULLET
    output = output.replace('\u00e9', '') # LATIN SMALL LETTER E WITH ACUTE
    output = output.replace('\ufb01', 'fi') # LATIN SMALL LIGATURE FI
    output = output.replace('<div>', '')
    output = output.replace(' </div>', '')
    output = output.replace('</div>', '')
    output = output.replace('<em>', '')
    output = output.replace('</em>', '')
    output = output.replace('<strong>', '')
    output = output.replace('</strong>', '')
    output = output.replace('<ul>', '')
    output = output.replace(' </ul>', '')
    output = output.replace('</ul>', '')
    output = output.replace(' <li>', ' - ')
    output = output.replace('<li>', ' - ')
    output = output.replace(' </li>', '')
    output = output.replace('</li>', '')
    output = output.replace('<ol>', '')
    output = output.replace(' </ol>', '')
    output = output.replace('</ol>', '')
    output = output.replace('<blockquote> ', '')
    output = output.replace(' </blockquote>', '')
    output = output.replace('<a target=\"_blank\" href=\"', '')
    output = output.replace('<a href=\"', '')
    output = output.replace('<a target=\"\" href=\"\" rel=\"noopener noreferrer nofollow\">', '')
    output = re.sub(r'\" target=.*a>', '', output)
    output = re.sub(r'\\\" rel=\\\"nofollow\\\">.*a>', '', output)
    output = output.replace(' orb)', ' or b)')
    output = re.sub(r'  +', ' ', output)
    return output.strip()