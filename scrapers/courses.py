import requests
import json
from utilities import parseInput

apiUrl = 'https://coursehandbook.mq.edu.au/api/es/search'
apiData = {'query':{'bool':{'must':[{'term':{'live':'true'}},[{'bool':{'minimum_should_match':'100%','should':[{'query_string':{'fields':['mq2_pcourse.implementationYear'],'query':'*2021*'}}]}}]],'filter':[{'terms':{'contenttype':['mq2_pcourse']}}]}},'sort':[{'mq2_pcourse.title_dotraw':{'order':'asc'}}],'from':0,'size':205,'track_scores':'true','_source':{'includes':['*.code','*.name','*.award_titles','*.keywords','urlmap','contenttype'],'excludes':['','null']}}
apiHeaders = {'content-type': 'application/json'}
fields = ['accredited_by_external_body', 'active', 'admission_requirements', 'admission_to_combined_double', 'any_double_degree_exclusions', 'application_method_other_details', 'are_there_additional_admission_points', 'arrangements', 'assessment', 'assessment_regulations', 'atar', 'capstone_or_professional_practice', 'course_standards_and_quality', 'delivery_with_third_party_provider', 'external_body', 'external_provider', 'ext_id', 'formal_articulation_pathway_to_higher_award', 'hours_per_week', 'how_does_this_course_deliver_a_capstone_experience', 'independent research', 'is_this_an_accelerated_course', 'justify_capstone_unit', 'number_of_weeks', 'offered_by_an_external_provider', 'provider_name_and_supporting_documentation', 'support_for_learning', 'wam_required_for_progression', 'what_is_the_internal_structure_of_course_majors', 'work_based_training_component']
req = requests.post(url=apiUrl, data=json.dumps(apiData), headers=apiHeaders)

output = {}

if req.status_code == 200:
    reqJson = req.json()
    contentlets = reqJson['contentlets']
    for element in contentlets:
        rawData = element['data']
        data = json.loads(rawData)

        output[data['code']] = {}
        
        for field in fields:
            if data[field] != '':
                output[data['code']][field] = parseInput(data[field])
        
        output[data['code']]['title'] = parseInput(data['title'])
        output[data['code']]['credits'] = parseInput(data['credit_points'])
        if data['graduate_destinations_and_employability'] != '':
            output[data['code']]['graduateDestinations'] = parseInput(data['graduate_destinations_and_employability'])
        if data['learning_and_teaching_methods'] != '':
            output[data['code']]['learningMethods'] = parseInput(data['learning_and_teaching_methods'])
        if data['overview_and_aims_of_the_course'] != '':
            output[data['code']]['overview'] = parseInput(data['overview_and_aims_of_the_course'])

        if data['accreditation_text_for_ahegs'] != '' and data['ahegs_award_text'] != '':
            output[data['code']]['ahegs'] = {}
            if data['accreditation_text_for_ahegs'] != '':
                output[data['code']]['ahegs']['accreditation'] = parseInput(data['accreditation_text_for_ahegs'])
            if data['ahegs_award_text'] != '':
                output[data['code']]['ahegs']['award'] = parseInput(data['ahegs_award_text'])

        if len(data['application_method']) != 0:
            output[data['code']]['application'] = parseInput(data['application_method'][0]['value'])
        output[data['code']]['type'] = parseInput(data['type']['label'])
        if data['volume_of_learning']['label'] is not None:
            output[data['code']]['volume'] = parseInput(data['volume_of_learning']['label'])
        output[data['code']]['aqf'] = parseInput(data['aqf_level']['label'])
        if data['course_duration_in_years']['label'] is not None:
            output[data['code']]['duration'] = parseInput(data['course_duration_in_years']['label'])
        if data['cricos_code'] != '':
            output[data['code']]['cricos'] = parseInput(data['cricos_code'])
        
        # Offerings
        if len(data['offering']) != 0:
            output[data['code']]['offerings'] = {}
            for i in range(len(data['offering'])):
                output[data['code']]['offerings']['o'+str(i)] = {}
                output[data['code']]['offerings']['o'+str(i)]['period'] = parseInput(data['offering'][i]['admission_calendar']['value'])
                if data['offering'][i]['location']['value'] != '':
                    output[data['code']]['offerings']['o'+str(i)]['location'] = parseInput(data['offering'][i]['location']['value'])

        #ielts
        if data['ielts_overall_score'] != '':
            output[data['code']]['ielts'] = {}
            output[data['code']]['ielts']['listening'] = parseInput(data['ielts_listening_score'])
            output[data['code']]['ielts']['overall'] = parseInput(data['ielts_overall_score'])
            output[data['code']]['ielts']['reading'] = parseInput(data['ielts_reading_score'])
            output[data['code']]['ielts']['speaking'] = parseInput(data['ielts_speaking_score'])
            output[data['code']]['ielts']['writing'] = parseInput(data['ielts_writing_score'])

        # Learning Outcomes
        if len(data['learning_outcomes']) != 0:
            output[data['code']]['outcomes'] = {}
            for ulo in data['learning_outcomes']:
                desc = parseInput(ulo['description'])
                output[data['code']]['outcomes'][ulo['code']] = desc
    
    with open('data/courses.json', 'w') as outfile:
        json.dump(output, outfile, indent=4, sort_keys=True)
else:
    print('Error encountered: '+str(req.status_code))