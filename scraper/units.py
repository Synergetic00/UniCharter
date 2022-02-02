import requests
import json

apiUrl = 'https://coursehandbook.mq.edu.au/api/es/search'
apiData = {'query':{'bool':{'must':[{'term':{'live':'true'}},[{'bool':{'minimum_should_match':'100%','should':[{'query_string':{'fields':['mq2_psubject.implementationYear'],'query':'*2021*'}}]}}]],'filter':[{'terms':{'contenttype':['mq2_psubject']}}]}},'sort':[{'mq2_psubject.code_dotraw':{'order':'asc'}},{'mq2_psubject.title_dotraw':{'order':'asc'}}],'from':0,'size':2489,'track_scores':'true','_source':{'includes':['*.code','*.name','*.award_titles','*.keywords','urlmap','contenttype'],'excludes':['','null']}}
apiHeaders = {'content-type': 'application/json'}
req = requests.post(url=apiUrl, data=json.dumps(apiData), headers=apiHeaders)

outputData = {}

def parseInput(string):
    return string.replace('<p>','').replace('</p>','').replace('\u00a0',' ').replace('<div>\\n','').replace('<div>\n','').replace('<br />','').replace("\u202f", " ").replace("\u2022", "•").replace("\u2026", "...").replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", "\"").replace("\u201d", "\"").replace("\u2014", "-").replace("\u2013", "-").replace("\t", " ").replace("\n", " ").replace("  ", " ").replace("  ", " ").replace("&amp;", "&").strip()

if req.status_code == 200:
    reqJson = req.json()
    contentlets = reqJson['contentlets']
    for element in contentlets:
        rawData = element['data']
        data = json.loads(rawData)

        # Basic Information
        outputData[data['code']] = {}
        outputData[data['code']]['title'] = parseInput(data['title'])
        outputData[data['code']]['credits'] = parseInput(data['credit_points'])
        outputData[data['code']]['group'] = parseInput(data['special_unit_type'][0]['label'])
        if data['description'] is not None:
            desc = parseInput(data['description'])
            outputData[data['code']]['description'] = desc
        outputData[data['code']]['department'] = parseInput(data['academic_org']['value'])
        outputData[data['code']]['faculty'] = parseInput(data['school']['value'])
        outputData[data['code']]['level'] = parseInput(data['level']['value'])

        # Learning Outcomes
        if len(data['unit_learning_outcomes']) != 0:
            outputData[data['code']]['outcomes'] = {}
            for ulo in data['unit_learning_outcomes']:
                desc = parseInput(ulo['description'])
                outputData[data['code']]['outcomes'][ulo['code']] = desc
    
        # Offerings
        if len(data['unit_offering']) != 0:
            outputData[data['code']]['offerings'] = {}
            for offering in data['unit_offering']:
                outputData[data['code']]['offerings']['o'+offering['order']] = {}
                outputData[data['code']]['offerings']['o'+offering['order']]['period'] = parseInput(offering['teaching_period']['value'])
                outputData[data['code']]['offerings']['o'+offering['order']]['attendance'] = parseInput(offering['attendance_mode']['value'])
                if offering['location']['value'] != '':
                    outputData[data['code']]['offerings']['o'+offering['order']]['location'] = parseInput(offering['location']['value'])
    
        # Assessments
        if len(data['assessments']) != 0:
            outputData[data['code']]['assessments'] = {}
            for i in range(len(data['assessments'])):
                outputData[data['code']]['assessments']['a'+str(i)] = {}
                outputData[data['code']]['assessments']['a'+str(i)]['title'] = parseInput(data['assessments'][i]['assessment_title'])
                outputData[data['code']]['assessments']['a'+str(i)]['type'] = parseInput(data['assessments'][i]['type']['label'])
                outputData[data['code']]['assessments']['a'+str(i)]['weighting'] = parseInput(data['assessments'][i]['weight'])
                outputData[data['code']]['assessments']['a'+str(i)]['hurdle'] = parseInput(data['assessments'][i]['hurdle_task'])
                if data['assessments'][i]['offerings'] != '':
                    outputData[data['code']]['assessments']['a'+str(i)]['offerings'] = parseInput(data['assessments'][i]['offerings'])
                if data['assessments'][i]['description'] is not None:
                    desc = parseInput(data['assessments'][i]['description'])
                    outputData[data['code']]['assessments']['a'+str(i)]['description'] = desc

        # Prerequisites
        for prereq in data['enrolment_rules']:
            if prereq['type']['value'] == 'nccw':
                outputData[data['code']]['nccw'] = parseInput(prereq['description'])
            if prereq['type']['value'] == 'prerequisite':
                outputData[data['code']]['prerequisite'] = parseInput(prereq['description'])

        # Scheduled Activities
        if len(data['scheduled_learning_activities']) != 0 and len(data['non_scheduled_learning_activities']) != 0:
            outputData[data['code']]['activities'] = {}
            outputData[data['code']]['activities']['scheduled'] = {}
            for i in range(len(data['scheduled_learning_activities'])):
                outputData[data['code']]['activities']['scheduled']['s'+str(i)] = {}
                # Name
                if data['scheduled_learning_activities'][i]['activity']['label'] is not None:
                    name = parseInput(data['scheduled_learning_activities'][i]['activity']['label'])        
                    outputData[data['code']]['activities']['scheduled']['s'+str(i)]['name'] = name
                # Offerings
                if data['scheduled_learning_activities'][i]['offerings'] is not None:
                    offers = parseInput(data['scheduled_learning_activities'][i]['offerings'])
                    outputData[data['code']]['activities']['scheduled']['s'+str(i)]['offerings'] = offers
                # Description
                if data['scheduled_learning_activities'][i]['description'] is not None:
                    if data['scheduled_learning_activities'][i]['description'] != '':
                        desc = parseInput(data['scheduled_learning_activities'][i]['description'])
                        outputData[data['code']]['activities']['scheduled']['s'+str(i)]['description'] = desc
 
            # Non-Scheduled Activities
            outputData[data['code']]['activities']['non-scheduled'] = {}
            for i in range(len(data['non_scheduled_learning_activities'])):
                outputData[data['code']]['activities']['non-scheduled']['ns'+str(i)] = {}
                # Name
                if data['non_scheduled_learning_activities'][i]['activity']['label'] is not None:
                    name = parseInput(data['non_scheduled_learning_activities'][i]['activity']['label'])        
                    outputData[data['code']]['activities']['non-scheduled']['ns'+str(i)]['name'] = name
                # Offerings
                if data['non_scheduled_learning_activities'][i]['offerings'] is not None:
                    offers = parseInput(data['non_scheduled_learning_activities'][i]['offerings'])
                    outputData[data['code']]['activities']['non-scheduled']['ns'+str(i)]['offerings'] = offers
                # Description
                if data['non_scheduled_learning_activities'][i]['description'] is not None:
                    if data['non_scheduled_learning_activities'][i]['description'] != '':
                        desc = parseInput(data['non_scheduled_learning_activities'][i]['description'])
                        outputData[data['code']]['activities']['non-scheduled']['ns'+str(i)]['description'] = desc
    
    with open('data/units.json', 'w') as outfile:
        json.dump(outputData, outfile, indent=4, sort_keys=True)
else:
    print('Error encountered: '+str(req.status_code))