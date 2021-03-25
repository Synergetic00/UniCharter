# Crawler

Needs:

* `pip3 install requests`

`Crawler.py`

the request's json returns:

```
json
    contentlets
        element0
            hostName
            modDate
            creditPoints
            code
            data
            sysId
            description
            studyLevel
            type
            title
            contentTypeLabel
            baseType
            inode
            mode
            archived
            host
            working
            locked
            stInode
            contentType
            live
            academicOrg
            owner
            identifier
            level
            studyLevelValue
            languageId
            active
            URL_MAP_FOR_CONTENT
            teachingPeriod
            version
            parentAcademicOrg
            url
            titleImage
            modUserName
            implementationYear
            urlMap
            folder
            hasTitleImage
            publishedInHandbook
            sortOrder
            modUser
            location
            levelDisplay
            effectiveDate
            status
        element1
            hostName
            modDate
            creditPoints
            code
            data
            sysId
            description
            studyLevel
            type
            title
            contentTypeLabel
            baseType
            inode
            mode
            archived
            host
            working
            locked
            stInode
            contentType
            live
            academicOrg
            owner
            identifier
            level
            studyLevelValue
            languageId
            active
            URL_MAP_FOR_CONTENT
            teachingPeriod
            version
            parentAcademicOrg
            url
            titleImage
            modUserName
            implementationYear
            urlMap
            folder
            hasTitleImage
            publishedInHandbook
            sortOrder
            modUser
            location
            levelDisplay
            effectiveDate
            status
    esresponse
```

Courses

```
aqf_level
implementation_year  
accrediting_bodies   
published_in_handbook
academic_org
status
school
credit_points
type
description
search_title
cl_id
code
title
version
content_type
abbreviated_name_and_major
version_name
course_code
abbreviated_name
ext_id
source
active
class_name
effective_date
learning_and_teaching_methods
overview_and_aims_of_the_course
support_for_learning
graduate_destinations_and_employability
fitness_to_practice
independent research
justify_capstone_unit
how_will_students_meet_clos_in_this_duration
what_is_the_internal_structure_of_course_majors
other_double_degree_considerations
course_standards_and_quality
exit
part_time
structure
no_enrolment
publication_information
internship_placement
cricos_code
specialisations
govt_special_course_type
entry_list
entry_guarantee
police_check
year_12_prerequisites
last_review_date
career_opportunities
fees_description
location
overview
course_version
alternative_exits
progression
english_language
ib_maths
requirements
qualification_requirement
articulation_arrangement
partner_faculty
full_time
qualifications
double_degrees
international_students
special_admission
entry
atar
course_data_updated
prior_learning_recognition
vce_other
award_titles
on_campus
research_areas
accreditation_start_date
participation_enrolment
vce_english
ib_other
online
progress_to_masters
additional_info
cricos_disclaimer_applicable
other_description
other
health_records_and_privacy
information_declaration
ahegs
part_time_duration
cricos_status
full_time_duration
prohibited_employment_declaration
minimum_entry_requirements
accreditation_end_date
accreditation_end
post_nominals
ib_english
credit_arrangements
outcomes
maximum_duration
majors_minors
vce_maths
degrees_awarded
non_year_12_entry
working_with_children_check
entry_pathways_and_adjustment_factors_other_details
course_duration_in_years
entry_pathways_and_adjustment_factors
does_undergraduate_principle_26_3_apply
formal_articulation_pathway_to_higher_award
application_method_other_details
ielts_overall_score
is_this_an_accelerated_course
how_does_this_course_deliver_a_capstone_experience
hours_per_week
exclusively_an_exit_award
ielts_listening_score
admission_to_combined_double
ielts_speaking_score
capstone_or_professional_practice
external_body
other_provider_name
provider_name_and_supporting_documentation
arrangements
number_of_weeks
application_method
delivery_with_third_party_provider
are_there_additional_admission_points
volume_of_learning
award_abbreviation
admission_requirements
any_double_degree_exclusions
ielts_writing_score
ahegs_award_text
work_based_training_component
ielts_reading_score
wam_required_for_progression
accreditation_text_for_ahegs
provider_name
assessment_regulations
accredited_by_external_body
offered_by_an_external_provider
assessment
level2_org_unit_data
related_associated_items
offering
study_modes
additional_admission_points
course_rules
course_notes
learning_outcomes
fees
higher_level_courses_that_students_may_exit_from
level1_org_unit_data
articulations
course_search_title
availableInDoubles
availableDoubles
credit_points_header
partner_org_unit_data
academic_item_type
inherent_requirements
availableAOS
external_provider
other_requirements
links
```

## Does the string exist in the set and used

```
accreditation_text_for_ahegs
accredited_by_external_body
active
admission_requirements
admission_to_combined_double
ahegs_award_text
any_double_degree_exclusions
application_method_other_details
are_there_additional_admission_points
arrangements
assessment
assessment_regulations
atar
award_abbreviation
capstone_or_professional_practice
class_name
cl_id
code
content_type
course_code
course_data_updated
course_search_title
course_standards_and_quality
credit_points
credit_points_header
cricos_code
cricos_disclaimer_applicable
delivery_with_third_party_provider
does_undergraduate_principle_26_3_apply
effective_date
entry_guarantee
external_body
external_provider
ext_id
formal_articulation_pathway_to_higher_award
full_time
graduate_destinations_and_employability
health_records_and_privacy
hours_per_week
how_does_this_course_deliver_a_capstone_experience
ielts_listening_score
ielts_overall_score
ielts_reading_score
ielts_speaking_score
ielts_writing_score
implementation_year
independent research
information_declaration
international_students
is_this_an_accelerated_course
justify_capstone_unit
learning_and_teaching_methods
no_enrolment
number_of_weeks
offered_by_an_external_provider
online
on_campus
other
overview_and_aims_of_the_course
part_time
police_check
prohibited_employment_declaration
provider_name_and_supporting_documentation
search_title
support_for_learning
title
version
version_name
wam_required_for_progression
what_is_the_internal_structure_of_course_majors
working_with_children_check
work_based_training_component
```

```
academic_item_type
accreditation_text_for_ahegs
accredited_by_external_body
active
admission_requirements
admission_to_combined_double
ahegs_award_text
any_double_degree_exclusions
application_method_other_details
are_there_additional_admission_points
arrangements
assessment
assessment_regulations
atar
award_abbreviation
capstone_or_professional_practice
class_name
cl_id
code
content_type
course_code
course_data_updated
course_search_title
course_standards_and_quality
credit_points
credit_points_header
cricos_code
cricos_disclaimer_applicable
delivery_with_third_party_provider
does_undergraduate_principle_26_3_apply
effective_date
entry_guarantee
external_body
external_provider
ext_id
formal_articulation_pathway_to_higher_award
full_time
graduate_destinations_and_employability
health_records_and_privacy
hours_per_week
how_does_this_course_deliver_a_capstone_experience
ielts_listening_score
ielts_overall_score
ielts_reading_score
ielts_speaking_score
ielts_writing_score
implementation_year
independent research
information_declaration
international_students
is_this_an_accelerated_course
justify_capstone_unit
learning_and_teaching_methods
no_enrolment
number_of_weeks
offered_by_an_external_provider
online
on_campus
other
overview_and_aims_of_the_course
part_time
police_check
prohibited_employment_declaration
provider_name_and_supporting_documentation
search_title
support_for_learning
title
version
version_name
wam_required_for_progression
what_is_the_internal_structure_of_course_majors
working_with_children_check
work_based_training_component
```