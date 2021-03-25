import requests
import json

url = "https://coursehandbook.mq.edu.au/api/es/search"
courses = {"query":{"bool":{"must":[{"term":{"live":"true"}},[{"bool":{"minimum_should_match":"100%","should":[{"query_string":{"fields":["mq2_pcourse.implementationYear"],"query":"*2021*"}}]}}]],"filter":[{"terms":{"contenttype":["mq2_pcourse"]}}]}},"sort":[{"mq2_pcourse.title_dotraw":{"order":"asc"}}],"from":0,"size":205,"track_scores":"true","_source":{"includes":["*.code","*.name","*.award_titles","*.keywords","urlmap","contenttype"],"excludes":["","null"]}}
headers = {'content-type': 'application/json'}
fields = ['accredited_by_external_body', 'active', 'admission_requirements', 'admission_to_combined_double', 'any_double_degree_exclusions', 'application_method_other_details', 'are_there_additional_admission_points', 'arrangements', 'assessment', 'assessment_regulations', 'atar', 'capstone_or_professional_practice', 'course_standards_and_quality', 'delivery_with_third_party_provider', 'external_body', 'external_provider', 'ext_id', 'formal_articulation_pathway_to_higher_award', 'hours_per_week', 'how_does_this_course_deliver_a_capstone_experience', 'independent research', 'is_this_an_accelerated_course', 'justify_capstone_unit', 'number_of_weeks', 'offered_by_an_external_provider', 'provider_name_and_supporting_documentation', 'support_for_learning', 'wam_required_for_progression', 'what_is_the_internal_structure_of_course_majors', 'work_based_training_component']

def parseTrim(string):
    return string.replace('<p>','').replace('</p>','').replace('\u00a0',' ').replace('<div>\\n','').replace('<div>\n','').replace('<br />','').replace("\u2018", "'").replace("\u2019", "'").replace("\u2013", "-").replace("&amp;", "&").replace("\u2122", "™").replace("\u201c", "\"").replace("\u00e9", "é").strip()

formatted = {}

r = requests.post(url, data=json.dumps(courses), headers=headers)
if r.status_code == 200:
    output = r.json()
    contentlets = output.get('contentlets')
    for element in contentlets:
        data = element.get('data')
        parsed = json.loads(data)
        formatted[parsed['code']] = {}
        
        for field in fields:
            if parsed[field] != '':
                formatted[parsed['code']][field] = parseTrim(parsed[field])
        
        formatted[parsed['code']]['title'] = parsed['title']
        formatted[parsed['code']]['credits'] = parsed['credit_points']
        if parsed['graduate_destinations_and_employability'] != '':
            formatted[parsed['code']]['graduateDestinations'] = parseTrim(parsed['graduate_destinations_and_employability'])
        if parsed['learning_and_teaching_methods'] != '':
            formatted[parsed['code']]['learningMethods'] = parseTrim(parsed['learning_and_teaching_methods'])
        if parsed['overview_and_aims_of_the_course'] != '':
            formatted[parsed['code']]['overview'] = parseTrim(parsed['overview_and_aims_of_the_course'])

        if parsed['accreditation_text_for_ahegs'] != '' and parsed['ahegs_award_text'] != '':
            formatted[parsed['code']]['ahegs'] = {}
            if parsed['accreditation_text_for_ahegs'] != '':
                formatted[parsed['code']]['ahegs']['accreditation'] = parseTrim(parsed['accreditation_text_for_ahegs'])
            if parsed['ahegs_award_text'] != '':
                formatted[parsed['code']]['ahegs']['award'] = parseTrim(parsed['ahegs_award_text'])

        if len(parsed['application_method']) != 0:
            formatted[parsed['code']]['application'] = parsed['application_method'][0]['value']
        formatted[parsed['code']]['type'] = parsed['type']['label']
        if parsed['volume_of_learning']['label'] is not None:
            formatted[parsed['code']]['volume'] = parsed['volume_of_learning']['label']
        formatted[parsed['code']]['aqf'] = parsed['aqf_level']['label']
        if parsed['course_duration_in_years']['label'] is not None:
            formatted[parsed['code']]['duration'] = parsed['course_duration_in_years']['label']
        if parsed['cricos_code'] != '':
            formatted[parsed['code']]['cricos'] = parsed['cricos_code']
        
        # Offerings
        if len(parsed['offering']) != 0:
            formatted[parsed['code']]['offerings'] = {}
            for i in range(len(parsed['offering'])):
                formatted[parsed['code']]['offerings']['o'+str(i)] = {}
                formatted[parsed['code']]['offerings']['o'+str(i)]['period'] = parsed['offering'][i]['admission_calendar']['value']
                if parsed['offering'][i]['location']['value'] != '':
                    formatted[parsed['code']]['offerings']['o'+str(i)]['location'] = parsed['offering'][i]['location']['value']

        #ielts
        if parsed['ielts_overall_score'] != '':
            formatted[parsed['code']]['ielts'] = {}
            formatted[parsed['code']]['ielts']['listening'] = parsed['ielts_listening_score']
            formatted[parsed['code']]['ielts']['overall'] = parsed['ielts_overall_score']
            formatted[parsed['code']]['ielts']['reading'] = parsed['ielts_reading_score']
            formatted[parsed['code']]['ielts']['speaking'] = parsed['ielts_speaking_score']
            formatted[parsed['code']]['ielts']['writing'] = parsed['ielts_writing_score']

        # Learning Outcomes
        if len(parsed['learning_outcomes']) != 0:
            formatted[parsed['code']]['outcomes'] = {}
            for ulo in parsed['learning_outcomes']:
                desc = parseTrim(ulo['description'])
                formatted[parsed['code']]['outcomes'][ulo['code']] = desc


    with open('data/courses.json', 'w') as outfile:
        json.dump(formatted, outfile, indent=4, sort_keys=True)
else:
    print("Error encountered: "+str(r.status_code))