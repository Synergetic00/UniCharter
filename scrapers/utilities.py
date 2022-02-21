import re

def parseInput(string):
    output = string
    # HTML elements
    output = output.replace('<p>','')
    output = output.replace('</p>','')
    output = output.replace('<div>\\n','')
    output = output.replace('<div>\n','')
    output = output.replace('<br />','')
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
    # Escaped values
    output = output.replace('\t', ' ')
    output = output.replace('\n', ' ')
    output = output.replace('&amp;', '&')
    # Unicode characters
    output = output.replace('\u00a0',' ') # NO-BREAK SPACE
    output = output.replace('\u00ad', '-') # SOFT HYPHEN
    output = output.replace('\u00ae', '(R)') # REGISTERED SIGN
    output = output.replace('\u00b1', '+/-')
    output = output.replace('\u2122', '(tm)')
    output = output.replace('\u037e', ';')
    output = output.replace('\u00f6', 'o')
    output = output.replace('\u200b', '')
    output = output.replace('\u00e2', '')
    output = output.replace('\u20ac', '')
    output = output.replace('\u02dc', '')
    output = output.replace('\u00b7', '-')
    output = output.replace('\u00d7', '*')
    output = output.replace('\u2013', '-')
    output = output.replace('\u2014', '-')
    output = output.replace('\u2018', '\'')
    output = output.replace('\u2019', '\'')
    output = output.replace('\u201c', '\'')
    output = output.replace('\u201d', '\'')
    output = output.replace('\u2022', '-')
    output = output.replace('\u2026', '...')
    output = output.replace('\u2028', '') # LINE SEPERATOR
    output = output.replace('\u202f', ' ')
    output = output.replace('\u25e6', '-') # WHITE BULLET
    output = output.replace('\u00e9', '') # LATIN SMALL LETTER E WITH ACUTE
    output = output.replace('\ufb01', 'fi') # LATIN SMALL LIGATURE FI
    output = output.replace('\uf0a7', '-')
    # Link tags
    output = output.replace('<a target=\"_blank\" href=\"', '')
    output = output.replace('<a href=\"', '')
    output = output.replace('<a target=\"\" href=\"\" rel=\"noopener noreferrer nofollow\">', '')
    # Regex
    output = re.sub(r'\" target=.*a>', '', output)
    output = re.sub(r'\\\" rel=\\\"nofollow\\\">[A-Za-z0-9.]+</a>', '', output)
    output = output.replace(' orb)', ' or b)')
    output = re.sub(r'  +', ' ', output)
    # Additional cleanup
    output = output.replace('<blockquote> ', '')
    output = output.replace(' </blockquote>', '')
    return output.strip()