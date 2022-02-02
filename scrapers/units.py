import requests
import json
import re

apiUrl = 'https://coursehandbook.mq.edu.au/api/es/search'
apiData = {'query':{'bool':{'must':[{'term':{'live':'true'}},[{'bool':{'minimum_should_match':'100%','should':[{'query_string':{'fields':['mq2_psubject.implementationYear'],'query':'*2021*'}}]}}]],'filter':[{'terms':{'contenttype':['mq2_psubject']}}]}},'sort':[{'mq2_psubject.code_dotraw':{'order':'asc'}},{'mq2_psubject.title_dotraw':{'order':'asc'}}],'from':0,'size':2489,'track_scores':'true','_source':{'includes':['*.code','*.name','*.award_titles','*.keywords','urlmap','contenttype'],'excludes':['','null']}}
apiHeaders = {'content-type': 'application/json'}
req = requests.post(url=apiUrl, data=json.dumps(apiData), headers=apiHeaders)

outputData = {}

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