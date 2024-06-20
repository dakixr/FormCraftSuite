
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

tpl = DocxTemplate("template.docx")

context = {
    # First Page
    "function": "Software Engineer",
    # Personal Details
    "first_name": "Daniel",
    "surname": "Rodriguez Mariblanca",
    "date_of_birth": "08-08-1999",
    "city": "Luxembourg",
    "nationality": "Spanish",
    "availability": "Full Time",
    "drivers_license": "Yes",
    "profile_pic":  InlineImage(tpl, 'pooo.png', height=Mm(40)),
    # Profile & Ambition
    "profile_and_ambition": "bla bla bla " * 30,
    "highlights": [f"This is my highlight {n}" for n in range(4)],
    # Education & Courses
    "education": [
        {
            "period": "1999-2024",
            "name_education": "Life",
            "name_employer_client": "My parents",
            "status": "Ongoing",
        }
    ],
    "courses": [
        {
            "period": "2020-2021",
            "name_education": "Covid",
            "name_employer_client": "A virus",
            "status": "Finished?",
        }
    ],
    # Work experience
    "work_experience": [
        {
            "period": "1999-2024",
            "function_name": "Life learner",
            "name_employer_client": "My parents",
            "bullet_points": [f"This is my bullet_point {n}" for n in range(4)],
        }
    ],
    # Expertise
    "expertise": [
        {
            "category": "Programming Languages",
            "list": [
                {
                    "name": "Python",
                    "basic": "",
                    "good": "",
                    "excellent": "X",
                },
                {
                    "name": "Eating",
                    "basic": "",
                    "good": "",
                    "excellent": "X",
                },
                {
                    "name": "Sleeping",
                    "basic": "",
                    "good": "",
                    "excellent": "X",
                },
            ],
        },
        {
            "category": "Languages",
            "list": [
                {
                    "name": "Spanish",
                    "basic": "",
                    "good": "",
                    "excellent": "X",
                },
                {
                    "name": "English",
                    "basic": "",
                    "good": "",
                    "excellent": "X",
                },
                {
                    "name": "German",
                    "basic": "X",
                    "good": "",
                    "excellent": "",
                },
            ],
        },
    ],
}

tpl.render(context)
tpl.replace_media('dummy_profile_pic.png', 'pooo.png')
tpl.save("generated_cv.docx")

print("Successfully generated the CV!")
