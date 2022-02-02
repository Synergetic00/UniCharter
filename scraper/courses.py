import requests
import json

apiUrl = 'https://coursehandbook.mq.edu.au/api/es/search'
apiData = {'query':{'bool':{'must':[{'term':{'live':'true'}},[{'bool':{'minimum_should_match':'100%','should':[{'query_string':{'fields':['mq2_pcourse.implementationYear'],'query':'*2021*'}}]}}]],'filter':[{'terms':{'contenttype':['mq2_pcourse']}}]}},'sort':[{'mq2_pcourse.title_dotraw':{'order':'asc'}}],'from':0,'size':205,'track_scores':'true','_source':{'includes':['*.code','*.name','*.award_titles','*.keywords','urlmap','contenttype'],'excludes':['','null']}}
apiHeaders = {'content-type': 'application/json'}
fields = ['accredited_by_external_body', 'active', 'admission_requirements', 'admission_to_combined_double', 'any_double_degree_exclusions', 'application_method_other_details', 'are_there_additional_admission_points', 'arrangements', 'assessment', 'assessment_regulations', 'atar', 'capstone_or_professional_practice', 'course_standards_and_quality', 'delivery_with_third_party_provider', 'external_body', 'external_provider', 'ext_id', 'formal_articulation_pathway_to_higher_award', 'hours_per_week', 'how_does_this_course_deliver_a_capstone_experience', 'independent research', 'is_this_an_accelerated_course', 'justify_capstone_unit', 'number_of_weeks', 'offered_by_an_external_provider', 'provider_name_and_supporting_documentation', 'support_for_learning', 'wam_required_for_progression', 'what_is_the_internal_structure_of_course_majors', 'work_based_training_component']
req = requests.post(url=apiUrl, data=json.dumps(apiData), headers=apiHeaders)

outputData = {}

def parseInput(string):
    return string.replace('<p>','').replace('</p>','').replace('\u00a0',' ').replace('<div>\\n','').replace('<div>\n','').replace('<br />','').replace('\u202f', ' ').replace('\u2022', '•').replace('\u2026', '...').replace('\u2018', ''').replace('\u2019', ''').replace('\u201c', '\'').replace('\u201d', '\'').replace('\u2014', '-').replace('\u2013', '-').replace('\t', ' ').replace('\n', ' ').replace('  ', ' ').replace('  ', ' ').replace('&amp;', '&').strip()

if req.status_code == 200:
    reqJson = req.json()
    contentlets = reqJson['contentlets']
    for element in contentlets:
        rawData = element['data']
        data = json.loads(rawData)

        outputData[data['code']] = {}
        
        for field in fields:
            if data[field] != '':
                outputData[data['code']][field] = parseInput(data[field])
        
        outputData[data['code']]['title'] = parseInput(data['title'])
        outputData[data['code']]['credits'] = parseInput(data['credit_points'])
        if data['graduate_destinations_and_employability'] != '':
            outputData[data['code']]['graduateDestinations'] = parseInput(data['graduate_destinations_and_employability'])
        if data['learning_and_teaching_methods'] != '':
            outputData[data['code']]['learningMethods'] = parseInput(data['learning_and_teaching_methods'])
        if data['overview_and_aims_of_the_course'] != '':
            outputData[data['code']]['overview'] = parseInput(data['overview_and_aims_of_the_course'])

        if data['accreditation_text_for_ahegs'] != '' and data['ahegs_award_text'] != '':
            outputData[data['code']]['ahegs'] = {}
            if data['accreditation_text_for_ahegs'] != '':
                outputData[data['code']]['ahegs']['accreditation'] = parseInput(data['accreditation_text_for_ahegs'])
            if data['ahegs_award_text'] != '':
                outputData[data['code']]['ahegs']['award'] = parseInput(data['ahegs_award_text'])

        if len(data['application_method']) != 0:
            outputData[data['code']]['application'] = parseInput(data['application_method'][0]['value'])
        outputData[data['code']]['type'] = parseInput(data['type']['label'])
        if data['volume_of_learning']['label'] is not None:
            outputData[data['code']]['volume'] = parseInput(data['volume_of_learning']['label'])
        outputData[data['code']]['aqf'] = parseInput(data['aqf_level']['label'])
        if data['course_duration_in_years']['label'] is not None:
            outputData[data['code']]['duration'] = parseInput(data['course_duration_in_years']['label'])
        if data['cricos_code'] != '':
            outputData[data['code']]['cricos'] = parseInput(data['cricos_code'])
        
        # Offerings
        if len(data['offering']) != 0:
            outputData[data['code']]['offerings'] = {}
            for i in range(len(data['offering'])):
                outputData[data['code']]['offerings']['o'+str(i)] = {}
                outputData[data['code']]['offerings']['o'+str(i)]['period'] = parseInput(data['offering'][i]['admission_calendar']['value'])
                if data['offering'][i]['location']['value'] != '':
                    outputData[data['code']]['offerings']['o'+str(i)]['location'] = parseInput(data['offering'][i]['location']['value'])

        #ielts
        if data['ielts_overall_score'] != '':
            outputData[data['code']]['ielts'] = {}
            outputData[data['code']]['ielts']['listening'] = parseInput(data['ielts_listening_score'])
            outputData[data['code']]['ielts']['overall'] = parseInput(data['ielts_overall_score'])
            outputData[data['code']]['ielts']['reading'] = parseInput(data['ielts_reading_score'])
            outputData[data['code']]['ielts']['speaking'] = parseInput(data['ielts_speaking_score'])
            outputData[data['code']]['ielts']['writing'] = parseInput(data['ielts_writing_score'])

        # Learning Outcomes
        if len(data['learning_outcomes']) != 0:
            outputData[data['code']]['outcomes'] = {}
            for ulo in data['learning_outcomes']:
                desc = parseInput(ulo['description'])
                outputData[data['code']]['outcomes'][ulo['code']] = desc
    
    with open('data/courses.json', 'w') as outfile:
        json.dump(outputData, outfile, indent=4, sort_keys=True)
else:
    print('Error encountered: '+str(req.status_code))