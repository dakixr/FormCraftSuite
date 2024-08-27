import os
import io

from flask import Flask, render_template, request

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

from pdf_parser import name_talent_file, process_cv
from utils import render_and_send_file, unflatten_dict

# Config

app = Flask(__name__)
app.secret_key = "234hj32v4k32b4jb32lj4b32lj4"
app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF protection

# Routing


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/employeneur_profile_form", methods=["GET", "POST"])
def employeneur_profile_form():
    if request.method == "GET":
        return render_template("employeneur_profile_form.html")

    # Parse data
    tpl = DocxTemplate("docx_templates/cv-template.docx")
    data = unflatten_dict(request.form.to_dict())

    # Handle file upload
    profile_pic = request.files["profile_pic"]
    data["profile_pic"] = (
        InlineImage(tpl, profile_pic, height=Mm(40)) if profile_pic else None
    )

    # Transform expertise sections
    def parse_expertise(ex: dict) -> dict:
        return {
            "name": ex["name"],
            "basic": "X" if ex["level"] == "1" else "",
            "good": "X" if ex["level"] == "2" else "",
            "excellent": "X" if ex["level"] == "3" else "",
        }

    expertise = data.get("expertise")
    if expertise:
        for ex in expertise:
            ex["list"] = list(map(parse_expertise, ex["list"]))

    print(data)
    return render_and_send_file(
        data=data,
        tpl=tpl,
        download_name=name_talent_file(data),
    )


@app.route("/employeneur_profile_form_ai", methods=["GET", "POST"])
def employeneur_profile_form_ai():
    if request.method == "GET":
        return render_template("employeneur_profile_form_ai.html")
    
    cv = request.files["pdfFile"]
    form = request.form.to_dict() # Get form data
    job_description = form.get("jobDescription")
    tpl = DocxTemplate("docx_templates/cv-template.docx")
    pdf = io.BytesIO(cv.stream.read())
    data = process_cv(pdf, job_description)
    
    return render_and_send_file(
        data=data,
        tpl=tpl,
        download_name=name_talent_file(data),
    )


@app.route("/qm-meeting-report", methods=["GET", "POST"])
def qm_meeting_report():
    if request.method == "GET":
        return render_template("qm_meeting_report.html")

    # Parse data
    data = unflatten_dict(request.form.to_dict())

    def concat_list(l: None | list):
        if l is None:
            return ""
        return ", ".join(l)

    for attr in ("tmc_attendees", "company_attendees"):
        data[attr] = concat_list(data.get(attr))

    return render_and_send_file(
        data=data,
        tpl=DocxTemplate("docx_templates/qm-template.docx"),
        download_name="Qualifications Meeting Report.docx",
    )


if __name__ == "__main__":
    app.run(
        port=int(os.getenv("PORT", default=8000)),
        debug=True,
    )
