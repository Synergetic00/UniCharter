import requests
import json

url = "https://coursehandbook.mq.edu.au/api/es/search"
courses = {"query":{"bool":{"must":[{"term":{"live":"true"}},[{"bool":{"minimum_should_match":"100%","should":[{"query_string":{"fields":["mq2_pcourse.implementationYear"],"query":"*2021*"}}]}}]],"filter":[{"terms":{"contenttype":["mq2_pcourse"]}}]}},"sort":[{"mq2_pcourse.title_dotraw":{"order":"asc"}}],"from":0,"size":205,"track_scores":"true","_source":{"includes":["*.code","*.name","*.award_titles","*.keywords","urlmap","contenttype"],"excludes":["","null"]}}
headers = {'content-type': 'application/json'}

def parseTrim(string):
    return string.replace('<p>','').replace('</p>','').replace('\u00a0',' ').replace('<div>\\n','').replace('<div>\n','').replace('<br />','').replace("\u2018", "'").replace("\u2019", "'").replace("\u2013", "-").replace("&amp;", "&").replace("\u2122", "™").replace("\u201c", "\"").replace("\u00e9", "é").strip()

formatted = {}

r = requests.post(url, data=json.dumps(courses), headers=headers)
if r.status_code == 200:
    output = r.json()
    contentlets = output.get('contentlets')
    first = json.loads(contentlets[0].get('data'))

    for k, v in first.items():
        has = False
        if type(v) == str:
            for element in contentlets:
                data = element.get('data')
                parsed = json.loads(data)
                if parsed[k] != '':
                    has = True
        if has:
            print(k)
                
else:
    print("Error encountered: "+str(r.status_code))