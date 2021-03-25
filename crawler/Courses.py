import requests
import json

url = "https://coursehandbook.mq.edu.au/api/es/search"
courses = {"query":{"bool":{"must":[{"term":{"live":"true"}},[{"bool":{"minimum_should_match":"100%","should":[{"query_string":{"fields":["mq2_pcourse.implementationYear"],"query":"*2021*"}}]}}]],"filter":[{"terms":{"contenttype":["mq2_pcourse"]}}]}},"sort":[{"mq2_pcourse.title_dotraw":{"order":"asc"}}],"from":0,"size":205,"track_scores":"true","_source":{"includes":["*.code","*.name","*.award_titles","*.keywords","urlmap","contenttype"],"excludes":["","null"]}}
headers = {'content-type': 'application/json'}
fields = ['academic_item_type', 'accreditation_text_for_ahegs', 'accredited_by_external_body', 'active', 'admission_requirements', 'admission_to_combined_double', 'ahegs_award_text', 'any_double_degree_exclusions', 'application_method_other_details', 'are_there_additional_admission_points', 'arrangements', 'assessment', 'assessment_regulations', 'atar', 'award_abbreviation', 'capstone_or_professional_practice', 'class_name', 'cl_id', 'code', 'content_type', 'course_code', 'course_data_updated', 'course_search_title', 'course_standards_and_quality', 'credit_points', 'credit_points_header', 'cricos_code', 'cricos_disclaimer_applicable', 'delivery_with_third_party_provider', 'does_undergraduate_principle_26_3_apply', 'effective_date', 'entry_guarantee', 'external_body', 'external_provider', 'ext_id', 'formal_articulation_pathway_to_higher_award', 'full_time', 'graduate_destinations_and_employability', 'health_records_and_privacy', 'hours_per_week', 'how_does_this_course_deliver_a_capstone_experience', 'ielts_listening_score', 'ielts_overall_score', 'ielts_reading_score', 'ielts_speaking_score', 'ielts_writing_score', 'implementation_year', 'independent research', 'information_declaration', 'international_students', 'is_this_an_accelerated_course', 'justify_capstone_unit', 'learning_and_teaching_methods', 'no_enrolment', 'number_of_weeks', 'offered_by_an_external_provider', 'online', 'on_campus', 'other', 'overview_and_aims_of_the_course', 'part_time', 'police_check', 'prohibited_employment_declaration', 'provider_name_and_supporting_documentation', 'search_title', 'support_for_learning', 'title', 'version', 'version_name', 'wam_required_for_progression', 'what_is_the_internal_structure_of_course_majors', 'working_with_children_check', 'work_based_training_component']

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
        formatted[parsed['code']]['title'] = parsed['title']
        formatted[parsed['code']]['credits'] = parsed['credit_points']

        formatted[parsed['code']]['ahegs'] = parseTrim(parsed['ahegs_award_text'])
        formatted[parsed['code']]['assessment'] = parseTrim(parsed['assessment'])
        formatted[parsed['code']]['graduate'] = parseTrim(parsed['graduate_destinations_and_employability'])
        formatted[parsed['code']]['methods'] = parseTrim(parsed['learning_and_teaching_methods'])
        formatted[parsed['code']]['overview'] = parseTrim(parsed['overview_and_aims_of_the_course'])

        #wam_required_for_progression

        if parsed['active'] != 'true':
            print("surprise "+parsed['code'])

        if len(parsed['application_method']) != 0:
            formatted[parsed['code']]['application'] = parsed['application_method'][0]['value']
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
        
        # Offerings
        formatted[parsed['code']]['offerings'] = {}
        for i in range(len(parsed['offering'])):
            formatted[parsed['code']]['offerings']['o'+str(i)] = {}
            formatted[parsed['code']]['offerings']['o'+str(i)]['period'] = parsed['offering'][i]['admission_calendar']['value']
            if parsed['offering'][i]['location']['value'] != '':
                formatted[parsed['code']]['offerings']['o'+str(i)]['location'] = parsed['offering'][i]['location']['value']

        #ielts
        formatted[parsed['code']]['ielts'] = {}
        formatted[parsed['code']]['ielts']['listening'] = parsed['ielts_listening_score']
        formatted[parsed['code']]['ielts']['overall'] = parsed['ielts_overall_score']
        formatted[parsed['code']]['ielts']['reading'] = parsed['ielts_reading_score']
        formatted[parsed['code']]['ielts']['speaking'] = parsed['ielts_speaking_score']
        formatted[parsed['code']]['ielts']['writing'] = parsed['ielts_writing_score']

        # Learning Outcomes
        formatted[parsed['code']]['outcomes'] = {}
        for ulo in parsed['learning_outcomes']:
            desc = parseTrim(ulo['description'])
            formatted[parsed['code']]['outcomes'][ulo['code']] = desc


    with open('data/courses.json', 'w') as outfile:
        json.dump(formatted, outfile, indent=4, sort_keys=True)
else:
    print("Error encountered: "+str(r.status_code))