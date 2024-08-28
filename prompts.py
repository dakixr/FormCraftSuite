###############################################################################
# CV

CV_PARSER_PROMPT = """
Please read the following text extracted from a CV and create a detailed output following the schema below. 
The lists can have an arbitrary length based on the content of the CV. 

Text extracted from a CV:
'''
{cv_text}
'''
"""

CV_SCHEMA_DEFINITION = """
{
        "first_name": "First Name from CV",
        "surname": "Surname from CV",
        "function": "Job Title or Function",
        "date_of_birth": "YYYY-MM-DD",
        "city": "City of Residence",
        "nationality": "Nationality",
        "availability": "YYYY-MM-DD",
        "drivers_license": "Yes/No",
        "profile_and_ambition": "Summary of profile and career ambitions",
        "highlights": [
            "Key highlight 1",
            "Key highlight 2",
            "Key highlight 3",
            "... (additional highlights)"
        ],
        "education": [
            {
                "period": "Start Year - End Year",
                "name_education": "Degree or Qualification",
                "name_school": "Name of Institution",
                "status": "Completed/In Progress"
            },
            "... (additional education entries)"
        ],
        "courses": [
            {
                "period": "Year of Completion",
                "name_education": "Course Name",
                "name_school": "Institution/Platform",
                "status": "Completed/Ongoing"
            },
            "... (additional courses)"
        ],
        "work_experience": [
            {
                "period": "Start Year - End Year",
                "function_name": "Job Title",
                "name_employer_client": "Employer/Client Name, Location",
                "bullet_points": [
                    "Responsibility or Achievement 1",
                    "Responsibility or Achievement 2",
                    "Responsibility or Achievement 3",
                    "... (additional points)"
                ],
                "tools_tech_used": "concise list of technologies and/or tools used in this role"
            },
            "... (additional work experience entries)"
        ],
        "expertise": [
            {
                "category": "Category Name",
                "list": [
                    {"name": "Skill/Language Name", "basic": "", "good": "", "excellent": "X"},
                    "... (additional skills)"
                ]
            },
            "... (additional expertise categories)"
        ]
        "languages": [
            {"name": "Language Name", "proficiency": "Skill Level"}, # Skill Levels: Beginner, Intermediate, Advanced, Fluent, Native
            "... (additional languages)"
    }
"""


###############################################################################
# Job Description

JOB_DESCRIPTION_PARSER_PROMPT = """
Please read the following job description and Applicant CV. 
The task is to create the best front page of the CV based on the job description.
Make this candidate be the best fit for the job description.

Job Description:
'''
{job_description}
'''

Applicant CV:
'''
{cv}
'''
"""

CV_FRONT_PAGE_SCHEMA_DEFINITION = """
{
    "front_sheet": {
        "candidate_name": "Full Name",
        "position_sought": "Position Title",
        "description": "Brief description of relevant experience.",
        "key_skills": [ "list of top 3 key skills relevant to the job description" , ... ],
        "education_and_qualifications": [ # only the ones relevant to the job description
            {
                "degree": "Degree Name",
                "institution": "Institution Name",
                "year": "Completion Year"
            },
            "... (additional education_and_qualifications entries)"
        ],
        "location": "location of residence",
        "languages": [
            {
                "language": "Language 1",
                "proficiency_level": "Proficiency Level"
            },
            "... (additional languages entries)"
        ],
        "consultant_comments": "reason why is a good fit for the job description" # be concise
    }
"""
