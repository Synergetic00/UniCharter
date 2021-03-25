import requests
import json

url = "https://coursehandbook.mq.edu.au/api/es/search"
units = {"query":{"bool":{"must":[{"term":{"live":"true"}},[{"bool":{"minimum_should_match":"100%","should":[{"query_string":{"fields":["mq2_psubject.implementationYear"],"query":"*2021*"}}]}}]],"filter":[{"terms":{"contenttype":["mq2_psubject"]}}]}},"sort":[{"mq2_psubject.code_dotraw":{"order":"asc"}},{"mq2_psubject.title_dotraw":{"order":"asc"}}],"from":0,"size":2489,"track_scores":"true","_source":{"includes":["*.code","*.name","*.award_titles","*.keywords","urlmap","contenttype"],"excludes":["","null"]}}
headers = {'content-type': 'application/json'}

def parseTrim(string):
    return string.replace('<p>','').replace('</p>','').replace('\u00a0',' ').replace('<div>\\n','').replace('<div>\n','').replace('<br />','').replace("\u2018", "'").replace("\u2019", "'").replace("\u2013", "-").replace("&amp;", "&").strip()

formatted = {}

r = requests.post(url, data=json.dumps(units), headers=headers)
if r.status_code == 200:
    output = r.json()
    contentlets = output.get('contentlets')
    for element in contentlets:
        data = element.get('data')
        parsed = json.loads(data)
        print(parsed['code'])
        formatted[parsed['code']] = {}
        formatted[parsed['code']]['title'] = parsed['title'].strip()
        formatted[parsed['code']]['credits'] = parsed['credit_points'].strip()
        formatted[parsed['code']]['group'] = parsed['special_unit_type'][0]['label'].strip()
        if parsed['description'] is not None:
            desc = parseTrim(parsed['description'])
            formatted[parsed['code']]['description'] = desc
        formatted[parsed['code']]['department'] = parsed['academic_org']['value'].strip()
        formatted[parsed['code']]['faculty'] = parsed['school']['value'].strip()
        formatted[parsed['code']]['level'] = parsed['level']['value'].strip()

        # Learning Outcomes
        if len(parsed['unit_learning_outcomes']) != 0:
            formatted[parsed['code']]['outcomes'] = {}
            for ulo in parsed['unit_learning_outcomes']:
                desc = parseTrim(ulo['description'])
                formatted[parsed['code']]['outcomes'][ulo['code']] = desc
    
        # Offerings
        if len(parsed['unit_offering']) != 0:
            formatted[parsed['code']]['offerings'] = {}
            for offering in parsed['unit_offering']:
                formatted[parsed['code']]['offerings']['o'+offering['order']] = {}
                formatted[parsed['code']]['offerings']['o'+offering['order']]['period'] = offering['teaching_period']['value']
                formatted[parsed['code']]['offerings']['o'+offering['order']]['attendance'] = offering['attendance_mode']['value']
                if offering['location']['value'] != '':
                    formatted[parsed['code']]['offerings']['o'+offering['order']]['location'] = offering['location']['value']
    
        # Assessments
        if len(parsed['assessments']) != 0:
            formatted[parsed['code']]['assessments'] = {}
            for i in range(len(parsed['assessments'])):
                formatted[parsed['code']]['assessments']['a'+str(i)] = {}
                formatted[parsed['code']]['assessments']['a'+str(i)]['title'] = parsed['assessments'][i]['assessment_title']
                formatted[parsed['code']]['assessments']['a'+str(i)]['type'] = parsed['assessments'][i]['type']['label']
                formatted[parsed['code']]['assessments']['a'+str(i)]['weighting'] = parsed['assessments'][i]['weight']
                formatted[parsed['code']]['assessments']['a'+str(i)]['hurdle'] = parsed['assessments'][i]['hurdle_task']
                if parsed['assessments'][i]['offerings'] != '':
                    formatted[parsed['code']]['assessments']['a'+str(i)]['offerings'] = parsed['assessments'][i]['offerings']
                if parsed['assessments'][i]['description'] is not None:
                    desc = parseTrim(parsed['assessments'][i]['description'])
                    formatted[parsed['code']]['assessments']['a'+str(i)]['description'] = desc

        # Prerequisites
        for prereq in parsed['enrolment_rules']:
            if prereq['type']['value'] == 'nccw':
                formatted[parsed['code']]['nccw'] = prereq['description']
            if prereq['type']['value'] == 'prerequisite':
                formatted[parsed['code']]['prerequisite'] = prereq['description']

        # Scheduled Activities
        if len(parsed['scheduled_learning_activities']) != 0 and len(parsed['non_scheduled_learning_activities']) != 0:
            formatted[parsed['code']]['activities'] = {}
            formatted[parsed['code']]['activities']['scheduled'] = {}
            for i in range(len(parsed['scheduled_learning_activities'])):
                formatted[parsed['code']]['activities']['scheduled']['s'+str(i)] = {}
                # Name
                if parsed['scheduled_learning_activities'][i]['activity']['label'] is not None:
                    name = parseTrim(parsed['scheduled_learning_activities'][i]['activity']['label'])        
                    formatted[parsed['code']]['activities']['scheduled']['s'+str(i)]['name'] = name
                # Offerings
                if parsed['scheduled_learning_activities'][i]['offerings'] is not None:
                    offers = parseTrim(parsed['scheduled_learning_activities'][i]['offerings'])
                    formatted[parsed['code']]['activities']['scheduled']['s'+str(i)]['offerings'] = offers
                # Description
                if parsed['scheduled_learning_activities'][i]['description'] is not None:
                    if parsed['scheduled_learning_activities'][i]['description'] != '':
                        desc = parseTrim(parsed['scheduled_learning_activities'][i]['description'])
                        formatted[parsed['code']]['activities']['scheduled']['s'+str(i)]['description'] = desc
 
            # Non-Scheduled Activities
            formatted[parsed['code']]['activities']['non-scheduled'] = {}
            for i in range(len(parsed['non_scheduled_learning_activities'])):
                formatted[parsed['code']]['activities']['non-scheduled']['ns'+str(i)] = {}
                # Name
                if parsed['non_scheduled_learning_activities'][i]['activity']['label'] is not None:
                    name = parseTrim(parsed['non_scheduled_learning_activities'][i]['activity']['label'])        
                    formatted[parsed['code']]['activities']['non-scheduled']['ns'+str(i)]['name'] = name
                # Offerings
                if parsed['non_scheduled_learning_activities'][i]['offerings'] is not None:
                    offers = parseTrim(parsed['non_scheduled_learning_activities'][i]['offerings'])
                    formatted[parsed['code']]['activities']['non-scheduled']['ns'+str(i)]['offerings'] = offers
                # Description
                if parsed['non_scheduled_learning_activities'][i]['description'] is not None:
                    if parsed['non_scheduled_learning_activities'][i]['description'] != '':
                        desc = parseTrim(parsed['non_scheduled_learning_activities'][i]['description'])
                        formatted[parsed['code']]['activities']['non-scheduled']['ns'+str(i)]['description'] = desc

    with open('data/units.json', 'w') as outfile:
        json.dump(formatted, outfile, indent=4, sort_keys=True)
else:
    print("Error encountered: "+str(r.status_code))