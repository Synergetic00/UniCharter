import requests
import json

url = "https://coursehandbook.mq.edu.au/api/es/search"
courses = {"query":{"bool":{"must":[{"term":{"live":"true"}},[{"bool":{"minimum_should_match":"100%","should":[{"query_string":{"fields":["mq2_pcourse.implementationYear"],"query":"*2021*"}}]}}]],"filter":[{"terms":{"contenttype":["mq2_pcourse"]}}]}},"sort":[{"mq2_pcourse.title_dotraw":{"order":"asc"}}],"from":0,"size":205,"track_scores":"true","_source":{"includes":["*.code","*.name","*.award_titles","*.keywords","urlmap","contenttype"],"excludes":["","null"]}}
units = {"query":{"bool":{"must":[{"term":{"live":"true"}},[{"bool":{"minimum_should_match":"100%","should":[{"query_string":{"fields":["mq2_psubject.implementationYear"],"query":"*2021*"}}]}}]],"filter":[{"terms":{"contenttype":["mq2_psubject"]}}]}},"sort":[{"mq2_psubject.code_dotraw":{"order":"asc"}},{"mq2_psubject.title_dotraw":{"order":"asc"}}],"from":0,"size":2489,"track_scores":"true","_source":{"includes":["*.code","*.name","*.award_titles","*.keywords","urlmap","contenttype"],"excludes":["","null"]}}
headers = {'content-type': 'application/json'}

formatted = {}

r = requests.post(url, data=json.dumps(units), headers=headers)
if r.status_code == 200:
    output = r.json()
    contentlets = output.get('contentlets')
    element = contentlets[0]
    data = element.get('data')
    parsed = json.loads(data)
    formatted[parsed['code']] = {}

    formatted[parsed['code']]['title'] = parsed['title']
    formatted[parsed['code']]['credits'] = parsed['credit_points']
    formatted[parsed['code']]['type'] = parsed['content_type']
    formatted[parsed['code']]['group'] = parsed['special_unit_type'][0]['label']
    formatted[parsed['code']]['description'] = parsed['description']
    formatted[parsed['code']]['department'] = parsed['academic_org']['value']
    formatted[parsed['code']]['faculty'] = parsed['school']['value']
    formatted[parsed['code']]['level'] = parsed['level']['value']
    formatted[parsed['code']]['outcomes'] = parsed['unit_learning_outcomes']
    formatted[parsed['code']]['offerings'] = parsed['unit_offering']
    formatted[parsed['code']]['assessments'] = parsed['assessments']
    formatted[parsed['code']]['prerequisites'] = parsed['enrolment_rules']
    formatted[parsed['code']]['activities'] = {}
    formatted[parsed['code']]['activities']['scheduled'] = parsed['scheduled_learning_activities']
    formatted[parsed['code']]['activities']['non-scheduled'] = parsed['non_scheduled_learning_activities']

    with open('data.txt', 'w') as outfile:
        json.dump(formatted, outfile)
else:
    print("Error encountered: "+str(r.status_code))