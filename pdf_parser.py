import io
import os
import PyPDF2
from openai import OpenAI
import json
from datetime import datetime


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def name_talent_file(data: dict):
    # Talent file DRVersion Daniel Rodriguez version July 2024
    first_name = data.get("first_name")
    if not first_name:
        first_name = "[First Name]"
        
    surname = data.get("surname")
    if not surname:
        surname = "[Surname]"
    
    # Get the current date
    current_date = datetime.now()

    # Format the date as "Month Year"
    formatted_date = current_date.strftime("%B %Y")

    return f"Talent file DRVersion {first_name} {surname} version {formatted_date}.docx"


# Function to extract text from PDF
def extract_text_from_pdf(pdf: io.BytesIO) -> str:
    reader = PyPDF2.PdfReader(pdf)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text


# Function to parse extracted text and format into schema
def parse_text_to_schema(text: str) -> dict:
    prompt = f"""
    Please read the following text extracted from a CV and create a detailed output following the schema below. The lists can have an arbitrary length based on the content of the CV. 

    The text is:
    {text}

    The output should be structured as follows (json format):
    {{
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
            {{
                "period": "Start Year - End Year",
                "name_education": "Degree or Qualification",
                "name_school": "Name of Institution",
                "status": "Completed/In Progress"
            }},
            "... (additional education entries)"
        ],
        "courses": [
            {{
                "period": "Year of Completion",
                "name_education": "Course Name",
                "name_school": "Institution/Platform",
                "status": "Completed/Ongoing"
            }},
            "... (additional courses)"
        ],
        "work_experience": [
            {{
                "period": "Start Year - End Year",
                "function_name": "Job Title",
                "name_employer_client": "Employer/Client Name, Location",
                "bullet_points": [
                    "Responsibility or Achievement 1",
                    "Responsibility or Achievement 2",
                    "Responsibility or Achievement 3",
                    "... (additional points)"
                ]
            }},
            "... (additional work experience entries)"
        ],
        "expertise": [
            {{
                "category": "Category Name",
                "list": [
                    {{"name": "Skill/Language Name", "basic": "", "good": "", "excellent": "X"}},
                    "... (additional skills)"
                ]
            }},
            "... (additional expertise categories)"
        ]
        "languages": [
            {"name": "Language Name", "proficiency": "Skill Level"}, # Skill Levels: Beginner, Intermediate, Advanced, Fluent, Native
            "... (additional languages)"
    }}
    Ensure the output captures all relevant details accurately and comprehensively from the CV. The lists such as highlights, education, courses, work experience, and expertise should reflect the content of the CV.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        content = response.choices[0].message.content

        if content is None:
            raise ValueError("Error when retrieving the api response")

        return json.loads(content)

    except Exception as e:
        print(e)
        return {}


# Main function to handle the process
def process_cv(pdf: io.BytesIO) -> dict:
    text = extract_text_from_pdf(pdf)
    return parse_text_to_schema(text)
