from docxtpl import InlineImage
from docx.shared import Mm


def get_context(tpl) -> dict:
    return {
        # First Page
        "function": "Software Engineer", # missing
        # Personal Details
        "first_name": "Daniel",
        "surname": "Rodriguez Mariblanca",
        "date_of_birth": "08-08-1999",
        "city": "Luxembourg",
        "nationality": "Spanish",
        "availability": "Full Time",
        "drivers_license": "Yes",
        "profile_pic": InlineImage(tpl, "pooo.png", height=Mm(40)),
        # Profile & Ambition
        "profile_and_ambition": "A passionate and dedicated software engineer with a strong background in computer science and business administration. Experienced in developing financial Python libraries, leading machine learning forecast solutions, and spearheading data warehousing initiatives. Committed to continuous learning and adapting to new challenges.",
        "highlights": [
            "Developed a financial Python library for portfolio optimization at Deloitte",
            "Led a machine learning forecast solution optimizing a $60M+ operational plan at Amazon",
            "First place in BEST AXA UPM Hackathon",
            "First place in National Cyber Olympics (CTF - Incibe)",
        ],
        # Education & Courses
        "education": [
            {
                "period": "Sept 2017 - Jul 2022",
                "name_education": "Computer Engineering and Business Administration and Management",
                "name_employer_client": "Universidad Politécnica de Madrid",
                "status": "Completed",
            },
            {
                "period": "Sept 2021 - Dec 2021",
                "name_education": "Computer Science",
                "name_employer_client": "Aalto University - Erasmus+",
                "status": "Completed",
            },
        ],
        "courses": [
            {
                "period": "2019/20",
                "name_education": "UPM Language Center Certificate, level C1.2",
                "name_employer_client": "",
                "status": "Completed",
            },
            {
                "period": "2020",
                "name_education": "TOEIC L&R",
                "name_employer_client": "",
                "status": "Completed",
            },
        ],
        # Work experience
        "work_experience": [
            {
                "period": "2023 - Present",
                "function_name": "Software Engineer",
                "name_employer_client": "TMC, Luxembourg",
                "bullet_points": [
                    "Developed a financial Python library for portfolio optimization",
                    "Streamlined cleaning and calculation process, improving efficiency and accuracy",
                ],
            },
            {
                "period": "2022 - 2023",
                "function_name": "BI & Software Engineer",
                "name_employer_client": "Amazon, Luxembourg",
                "bullet_points": [
                    "Led ML forecast solution, optimizing a $60M+ operational plan",
                    "Developed software tools from scratch",
                    "Spearheaded data warehousing initiatives",
                ],
            },
            {
                "period": "2019",
                "function_name": "Software Engineer",
                "name_employer_client": "Vector ITC Group, Spain",
                "bullet_points": [
                    "Developed mobile application modules for Santander Bank",
                    "Backend development",
                    "Scrum methodology",
                ],
            },
            {
                "period": "2017 - 2019",
                "function_name": "IT Teacher",
                "name_employer_client": "Fundación Alas, Spain",
                "bullet_points": [
                    "Assisted over 15 elderly and disabled women",
                    "Patient and adaptable teaching strategies",
                    "Simplified IT fundamentals with creative materials",
                ],
            },
        ],
        # Expertise
        "expertise": [
            {
                "category": "Programming Languages",
                "list": [
                    {"name": "Python", "basic": "", "good": "", "excellent": "X"},
                    {"name": "Java", "basic": "", "good": "", "excellent": "X"},
                    {"name": "C", "basic": "", "good": "", "excellent": "X"},
                    {"name": "Kotlin", "basic": "", "good": "", "excellent": "X"},
                    {"name": "Assembly", "basic": "", "good": "", "excellent": "X"},
                    {"name": "JavaScript", "basic": "", "good": "", "excellent": "X"},
                    {"name": "Bash", "basic": "", "good": "", "excellent": "X"},
                ],
            },
            {
                "category": "Technologies and Tools",
                "list": [
                    {
                        "name": "Machine Learning",
                        "basic": "",
                        "good": "",
                        "excellent": "X",
                    },
                    {"name": "Data Mining", "basic": "", "good": "", "excellent": "X"},
                    {"name": "Analytics", "basic": "", "good": "", "excellent": "X"},
                    {"name": "Data Science", "basic": "", "good": "", "excellent": "X"},
                    {"name": "Big Data", "basic": "", "good": "", "excellent": "X"},
                    {"name": "Anaconda", "basic": "", "good": "", "excellent": "X"},
                    {"name": "Miniconda", "basic": "", "good": "", "excellent": "X"},
                ],
            },
            {
                "category": "Libraries/Frameworks",
                "list": [
                    {"name": "pandas", "basic": "", "good": "", "excellent": "X"},
                    {"name": "NumPy", "basic": "", "good": "", "excellent": "X"},
                    {"name": "scikit-learn", "basic": "", "good": "", "excellent": "X"},
                    {"name": "Keras", "basic": "", "good": "", "excellent": "X"},
                ],
            },
            {
                "category": "Databases",
                "list": [
                    {"name": "SQL", "basic": "", "good": "", "excellent": "X"},
                    {"name": "NoSQL", "basic": "", "good": "", "excellent": "X"},
                    {"name": "Redshift", "basic": "", "good": "", "excellent": "X"},
                    {
                        "name": "Data Warehousing",
                        "basic": "",
                        "good": "",
                        "excellent": "X",
                    },
                    {
                        "name": "Cloud Databases",
                        "basic": "",
                        "good": "",
                        "excellent": "X",
                    },
                ],
            },
            {
                "category": "Web Development",
                "list": [
                    {"name": "HTML", "basic": "", "good": "", "excellent": "X"},
                    {"name": "CSS", "basic": "", "good": "", "excellent": "X"},
                    {"name": "JavaScript", "basic": "", "good": "", "excellent": "X"},
                    {"name": "RESTful APIs", "basic": "", "good": "", "excellent": "X"},
                ],
            },
            {
                "category": "Cloud Computing",
                "list": [
                    {
                        "name": "AWS (S3, Redshift, EC2, Lambda)",
                        "basic": "",
                        "good": "",
                        "excellent": "X",
                    },
                    {
                        "name": "Cloud Computing",
                        "basic": "",
                        "good": "",
                        "excellent": "X",
                    },
                    {"name": "Big Data", "basic": "", "good": "", "excellent": "X"},
                    {"name": "Spark", "basic": "", "good": "", "excellent": "X"},
                ],
            },
            {
                "category": "Tools",
                "list": [
                    {"name": "Git", "basic": "", "good": "", "excellent": "X"},
                    {"name": "Jupyter", "basic": "", "good": "", "excellent": "X"},
                    {"name": "Unix/Linux", "basic": "", "good": "", "excellent": "X"},
                    {"name": "SSH", "basic": "", "good": "", "excellent": "X"},
                    {"name": "Cron Jobs", "basic": "", "good": "", "excellent": "X"},
                ],
            },
            {
                "category": "Soft Skills",
                "list": [
                    {
                        "name": "Agile Methodologies (Scrum)",
                        "basic": "",
                        "good": "",
                        "excellent": "X",
                    },
                    {
                        "name": "Effective Communication",
                        "basic": "",
                        "good": "",
                        "excellent": "X",
                    },
                    {
                        "name": "Team Leadership",
                        "basic": "",
                        "good": "",
                        "excellent": "X",
                    },
                    {
                        "name": "Problem-Solving",
                        "basic": "",
                        "good": "",
                        "excellent": "X",
                    },
                ],
            },
            {
                "category": "Languages",
                "list": [
                    {"name": "Spanish", "basic": "", "good": "", "excellent": "X"},
                    {"name": "English", "basic": "", "good": "", "excellent": "X"},
                ],
            },
        ],
    }
