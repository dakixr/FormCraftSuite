import io
import os

from flask import Flask, redirect, render_template, send_file, request, url_for

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

from utils import unflatten_dict

# Config

app = Flask(__name__)
app.secret_key = "234hj32v4k32b4jb32lj4b32lj4"
app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF protection

# Routing


@app.route("/")
def index():
    return redirect(url_for("employeneur_profile_form"))
    # return render_template("index.html")


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

    # Generate CV
    tpl.render(data)
    cv_buffer = io.BytesIO()
    tpl.save(cv_buffer)
    cv_buffer.seek(0)

    # Return CV
    return send_file(
        cv_buffer, as_attachment=True, download_name="TMC Generated CV.docx"
    )

if __name__ == "__main__":
    app.run(
        port=os.getenv("PORT", default=8000),
        # debug=True,
    )
