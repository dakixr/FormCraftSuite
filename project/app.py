import os
from flask import Flask, render_template, send_file
from forms import ProfileForm
import json
import io
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF protection
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "media")


@app.route("/", methods=["GET"])
def index():
    return render_template("form.html", form=ProfileForm())


@app.route("/", methods=["POST"])
def submit_form():
    form = ProfileForm()
    tpl = DocxTemplate("template.docx")

    # Parse data
    form_data = parse_form_data(form_data=form.data, tpl=tpl)
    # with open("form_data.json", "w") as f:
    #     json.dump(form_data, f, indent=2, default=str)

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
    form_data["profile_pic"] = None
    if profile_pic:
        filename = secure_filename(profile_pic.filename)
        profile_pic.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        form_data["profile_pic"] = InlineImage(tpl, filename, height=Mm(40))

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
    app.run(port=8000, debug=True)
