import requests
import json

code = "ABST3040"
query = 'mq2_psubject.code: \"'+code+'\"'
url = "https://coursehandbook.mq.edu.au/api/es/search"
units = {"query":{"bool":{"must":[{"query_string":{"query":query}},{"term":{"live":"true"}}]}},"aggs":{"implementationYear":{"terms":{"field":"mq2_psubject.implementationYear_dotraw","size":100}},"availableInYears":{"terms":{"field":"mq2_psubject.availableInYears_dotraw","size":100}}},"size":100,"_source":{"includes":["versionNumber","availableInYears","implementationYear"]}}
headers = {'content-type': 'application/json'}

formatted = {}

r = requests.post(url, data=json.dumps(units), headers=headers)
if r.status_code == 200:
    output = r.json()
    contentlets = output.get('contentlets')
    element = contentlets[len(contentlets)-1]
    data = element.get('data')
    parsed = json.loads(data)
    formatted[parsed['code']] = {}
    formatted[parsed['code']]['title'] = parsed['title']
    formatted[parsed['code']]['credits'] = parsed['credit_points']
    formatted[parsed['code']]['type'] = parsed['content_type']
    formatted[parsed['code']]['group'] = parsed['special_unit_type'][0]['label']
    desc = parsed['description'].replace('<p>','').replace('</p>','').replace('\u00a0',' ').replace('<div>\\n','').replace('<div>\n','').strip()
    formatted[parsed['code']]['description'] = desc
    formatted[parsed['code']]['department'] = parsed['academic_org']['value']
    formatted[parsed['code']]['faculty'] = parsed['school']['value']
    formatted[parsed['code']]['level'] = parsed['level']['value']

    # Learning Outcomes
    formatted[parsed['code']]['outcomes'] = {}
    for ulo in parsed['unit_learning_outcomes']:
        desc = ulo['description'].replace('<p>','').replace('</p>','').replace('\u00a0',' ').replace('<div>\\n','').replace('<div>\n','').strip()
        formatted[parsed['code']]['outcomes'][ulo['code']] = desc
    
    # Offerings
    formatted[parsed['code']]['offerings'] = {}
    for offering in parsed['unit_offering']:
        formatted[parsed['code']]['offerings'][offering['order']] = {}
        formatted[parsed['code']]['offerings'][offering['order']]['period'] = offering['teaching_period']['value']
        formatted[parsed['code']]['offerings'][offering['order']]['attendance'] = offering['attendance_mode']['value']
        if offering['location']['value'] != '':
            formatted[parsed['code']]['offerings'][offering['order']]['location'] = offering['location']['value']
    
    # Assessments
    formatted[parsed['code']]['assessments'] = {}
    for i in range(len(parsed['assessments'])):
        formatted[parsed['code']]['assessments'][i] = {}
        formatted[parsed['code']]['assessments'][i]['title'] = parsed['assessments'][i]['assessment_title']
        formatted[parsed['code']]['assessments'][i]['type'] = parsed['assessments'][i]['type']['label']
        formatted[parsed['code']]['assessments'][i]['weighting'] = parsed['assessments'][i]['weight']
        formatted[parsed['code']]['assessments'][i]['hurdle'] = parsed['assessments'][i]['hurdle_task']
        if parsed['assessments'][i]['offerings'] != '':
            formatted[parsed['code']]['assessments'][i]['offerings'] = parsed['assessments'][i]['offerings']
        desc = parsed['assessments'][i]['description'].replace('<p>','').replace('</p>','').replace('\u00a0',' ').replace('<div>\\n','').replace('<div>\n','').strip()
        formatted[parsed['code']]['assessments'][i]['description'] = desc

    # Prerequisites
    for prereq in parsed['enrolment_rules']:
        if prereq['type']['value'] == 'nccw':
            formatted[parsed['code']]['nccw'] = prereq['description']
        if prereq['type']['value'] == 'prerequisite':
            formatted[parsed['code']]['prerequisite'] = prereq['description']
    
    # Activities
    formatted[parsed['code']]['activities'] = {}
    formatted[parsed['code']]['activities']['scheduled'] = {}
    for i in range(len(parsed['scheduled_learning_activities'])):
        formatted[parsed['code']]['activities']['scheduled'][i] = {}
        # Name
        name = parsed['scheduled_learning_activities'][i]['activity']['label'].replace('<p>','').replace('</p>','').replace('\u00a0',' ').replace('<div>\\n','').replace('<div>\n','').strip()        
        formatted[parsed['code']]['activities']['scheduled'][i]['name'] = name
        # Offerings
        offers = parsed['scheduled_learning_activities'][i]['offerings'].replace('<p>','').replace('</p>','').replace('\u00a0',' ').replace('<div>\\n','').replace('<div>\n','').strip()
        formatted[parsed['code']]['activities']['scheduled'][i]['offerings'] = offers
        # Description
        if parsed['scheduled_learning_activities'][i]['description'] != '':
            desc = parsed['scheduled_learning_activities'][i]['description'].replace('<p>','').replace('</p>','').replace('\u00a0',' ').replace('<div>\\n','').replace('<div>\n','').strip()
            formatted[parsed['code']]['activities']['scheduled'][i]['description'] = desc
        
    formatted[parsed['code']]['activities']['non-scheduled'] = {}
    for i in range(len(parsed['non_scheduled_learning_activities'])):
        formatted[parsed['code']]['activities']['non-scheduled'][i] = {}
        # Name
        name = parsed['non_scheduled_learning_activities'][i]['activity']['label'].replace('<p>','').replace('</p>','').replace('\u00a0',' ').replace('<div>\\n','').replace('<div>\n','').strip()        
        formatted[parsed['code']]['activities']['non-scheduled'][i]['name'] = name
        # Offerings
        offers = parsed['non_scheduled_learning_activities'][i]['offerings'].replace('<p>','').replace('</p>','').replace('\u00a0',' ').replace('<div>\\n','').replace('<div>\n','').strip()
        formatted[parsed['code']]['activities']['non-scheduled'][i]['offerings'] = offers
        # Description
        if parsed['non_scheduled_learning_activities'][i]['description'] != '':
            desc = parsed['non_scheduled_learning_activities'][i]['description'].replace('<p>','').replace('</p>','').replace('\u00a0',' ').replace('<div>\\n','').replace('<div>\n','').strip()
            formatted[parsed['code']]['activities']['non-scheduled'][i]['description'] = desc

    with open('data/unit.json', 'w') as outfile:
        json.dump(formatted, outfile, indent=4, sort_keys=True)
else:
    print("Error encountered: "+str(r.status_code))