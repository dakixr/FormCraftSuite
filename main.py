import io
import os

from flask import Flask, render_template, send_file
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

from forms import ProfileForm

app = Flask(__name__)
app.secret_key = "234hj32v4k32b4jb32lj4b32lj4"
app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF protection


@app.route("/", methods=["GET"])
def index():
    return render_template("form.html", form=ProfileForm())


@app.route("/", methods=["POST"])
def submit_form():
    form = ProfileForm()
    tpl = DocxTemplate("template.docx")

    # Parse data
    form_data = parse_form_data(form_data=form.data, tpl=tpl)

    # Generate CV
    tpl.render(form_data)
    cv_buffer = io.BytesIO()
    tpl.save(cv_buffer)
    cv_buffer.seek(0)

    # Return CV
    return send_file(
        cv_buffer, as_attachment=True, download_name="TMC Generated CV.docx"
    )


def parse_form_data(form_data, tpl):
    # Handle file upload
    profile_pic = form_data.get("profile_pic")
    form_data["profile_pic"] = (
        InlineImage(tpl, profile_pic, height=Mm(40)) if profile_pic else None
    )

    # Transform highlights
    form_data["highlights"] = [e.get("highlight") for e in form_data["highlights"]]

    # Transform work experience
    for e in form_data["work_experience"]:
        e["bullet_points"] = [b.get("bullet_point") for b in e["bullet_points"]]

    # Transform expertise sections
    def parse_expertise(e_expertise: dict) -> dict:
        d = {"name": e_expertise["expertise"], "basic": "", "good": "", "excellent": ""}
        level = e_expertise["level"]
        if level == "1":
            d["basic"] = "X"
        elif level == "2":
            d["good"] = "X"
        elif level == "3":
            d["excellent"] = "X"
        return d

    expertise = form_data["expertise_sections"]
    form_data["expertise"] = []
    for ex in expertise:
        form_data["expertise"].append(
            {"category": ex["title"], "list": list(map(parse_expertise, ex["items"]))}
        )
    del form_data["expertise_sections"]

    return form_data


if __name__ == "__main__":
    app.run(port=os.getenv("PORT", default=8000))
