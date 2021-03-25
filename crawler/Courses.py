import requests
import json

url = "https://coursehandbook.mq.edu.au/api/es/search"
courses = {"query":{"bool":{"must":[{"term":{"live":"true"}},[{"bool":{"minimum_should_match":"100%","should":[{"query_string":{"fields":["mq2_pcourse.implementationYear"],"query":"*2021*"}}]}}]],"filter":[{"terms":{"contenttype":["mq2_pcourse"]}}]}},"sort":[{"mq2_pcourse.title_dotraw":{"order":"asc"}}],"from":0,"size":205,"track_scores":"true","_source":{"includes":["*.code","*.name","*.award_titles","*.keywords","urlmap","contenttype"],"excludes":["","null"]}}
headers = {'content-type': 'application/json'}

formatted = {}

r = requests.post(url, data=json.dumps(courses), headers=headers)
if r.status_code == 200:
    output = r.json()
    contentlets = output.get('contentlets')
    for element in contentlets:
        data = element.get('data')
        parsed = json.loads(data)
        formatted[parsed['code']] = {}
        formatted[parsed['code']]['title'] = parsed['title']
        formatted[parsed['code']]['credits'] = parsed['credit_points']
        if parsed['award_abbreviation'] != '':
            formatted[parsed['code']]['abbreviation'] = parsed['award_abbreviation']
        formatted[parsed['code']]['type'] = parsed['type']['label']
        if parsed['volume_of_learning']['label'] is not None:
            formatted[parsed['code']]['volume'] = parsed['volume_of_learning']['label']
        formatted[parsed['code']]['aqf'] = parsed['aqf_level']['label']
        if parsed['course_duration_in_years']['label'] is not None:
            formatted[parsed['code']]['duration'] = parsed['course_duration_in_years']['label']
        if parsed['cricos_code'] != '':
            formatted[parsed['code']]['cricos'] = parsed['cricos_code']
        if parsed['atar'] != '':
            formatted[parsed['code']]['atar'] = parsed['atar']

    with open('data/courses.json', 'w') as outfile:
        json.dump(output, outfile, indent=4, sort_keys=True)
else:
    print("Error encountered: "+str(r.status_code))