import os

from flask import Flask, render_template, request

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

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
    tpl = DocxTemplate("template.docx")
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

    return render_and_send_file(
        data=data,
        tpl=tpl,
        download_name="TMC Generated CV.docx",
    )


@app.route("/qm-meeting-report", methods=["GET", "POST"])
def qm_meeting_report():
    if request.method == "GET":
        return render_template("qm-meeting-report.html")

    # Parse data
    tpl = DocxTemplate("qm-template.docx")
    data = unflatten_dict(request.form.to_dict())

    def concat_list(l: None | list):
        if l is None:
            return ""
        return ", ".join(l)

    for attr in ("tmc_attendees", "company_attendees"):
        data[attr] = concat_list(data.get(attr))

    return render_and_send_file(
        data=data,
        tpl=tpl,
        download_name="Qualifications Meeting Report.docx",
    )


if __name__ == "__main__":
    app.run(
        port=os.getenv("PORT", default=8000),
        debug=True,
    )
