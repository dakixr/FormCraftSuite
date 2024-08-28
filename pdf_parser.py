import io
import os
from textwrap import dedent
import PyPDF2
from openai import OpenAI
import json
from datetime import datetime
import prompts


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def name_talent_file(cv: dict):
    # Talent file DRVersion Daniel Rodriguez version July 2024
    first_name = cv.get("first_name")
    if not first_name:
        first_name = "[First Name]"

    surname = cv.get("surname")
    if not surname:
        surname = "[Surname]"

    # Get the current date
    current_date = datetime.now()

    # Format the date as "Month Year"
    formatted_date = current_date.strftime("%B %Y")

    return f"Talent file DRVersion {first_name} {surname} version {formatted_date}.docx"


def extract_text_from_pdf(pdf: io.BytesIO) -> str:
    reader = PyPDF2.PdfReader(pdf)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text


def prompt_gpt(prompt: str, schema_definition: str) -> dict:
    _prompt = f'''
    {prompt}
    
    The output MUST be structured as follows (json format):
    """
    {schema_definition}
    """
    '''
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": dedent(_prompt),
                }
            ],
        )
        content = response.choices[0].message.content
        return json.loads(content)  # type: ignore

    except Exception as e:
        print(e)
        return {}

###############################################################################
# Main functions to handle the process

def generate_cv(pdf: io.BytesIO) -> dict:
    cv_text = extract_text_from_pdf(pdf)
    return prompt_gpt(
        prompt=prompts.CV_PARSER_PROMPT.format(cv_text=cv_text),
        schema_definition=prompts.CV_SCHEMA_DEFINITION,
    )


def generate_cv_front_page(job_description: str, cv: dict) -> dict:
    return prompt_gpt(
        prompt=prompts.JOB_DESCRIPTION_PARSER_PROMPT.format(
            job_description=job_description, cv=cv
        ),
        schema_definition=prompts.CV_FRONT_PAGE_SCHEMA_DEFINITION,
    )
