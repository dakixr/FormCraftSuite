import io
import os
import re

from pprint import pprint
from flask import Flask, render_template, send_file, request

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

from forms import ProfileForm

# Config

app = Flask(__name__)
app.secret_key = "234hj32v4k32b4jb32lj4b32lj4"
app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF protection

# Routing


@app.route("/v2", methods=["GET", "POST"])
def index_v2():
    if request.method == "GET":
        return render_template("form_v2.html")

    # Parse data
    tpl = DocxTemplate("template_v2.docx")
    data = unflatten_dict(request.form.to_dict())
    data["profile_pic"] = request.files["profile_pic"]
    data = parse_data(data=data, tpl=tpl)

    # Generate CV
    tpl.render(data)
    cv_buffer = io.BytesIO()
    tpl.save(cv_buffer)
    cv_buffer.seek(0)

    # Return CV
    return send_file(
        cv_buffer, as_attachment=True, download_name="TMC Generated CV.docx"
    )


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("form.html", form=ProfileForm())

    form = ProfileForm()
    tpl = DocxTemplate("template.docx")

    # Parse data
    form_data = parse_form_data(form_data=form.data, tpl=tpl)

    pprint(form_data)

    # Generate CV
    tpl.render(form_data)
    cv_buffer = io.BytesIO()
    tpl.save(cv_buffer)
    cv_buffer.seek(0)

    # Return CV
    return send_file(
        cv_buffer, as_attachment=True, download_name="TMC Generated CV.docx"
    )


# Util functions


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


def parse_data(data, tpl):
    # Handle file upload
    profile_pic = data.get("profile_pic")
    data["profile_pic"] = (
        InlineImage(tpl, profile_pic, height=Mm(40)) if profile_pic else None
    )

    # Transform expertise sections
    def parse_expertise(ex: dict) -> dict:
        return {
            "name": ex["category"], 
            "basic": "X" if ex["level"] == "1" else "", 
            "good": "X" if ex["level"] == "2" else "", 
            "excellent": "X" if ex["level"] == "3" else "",
        }

    expertise = data.get("expertise")
    if expertise:
        data["expertise"] = []
        for ex in expertise:
            data["expertise"].append(
                {
                    "category": ex["category"],
                    "list": list(map(parse_expertise, ex["list"])),
                }
            )

    return data


def unflatten_dict(flat_dict):
    def get_or_create_with_padding(lst, index, default=None):
        if index < len(lst):
            return lst[index]
        else:
            lst.extend([default] * (index - len(lst) + 1))
            return default

    def sliding_window(lst):
        for i in range(len(lst)):
            if i < len(lst) - 1:
                yield lst[i], lst[i + 1]
            else:
                yield lst[i], None

    def set_nested_item(data_dict: dict, keys: list[str], value):
        curr: list | dict = data_dict
        for key, next_key in sliding_window(keys):
            if isinstance(curr, list):
                key = int(key)
                if next_key is None:
                    curr.insert(key, value)
                else:
                    next = get_or_create_with_padding(
                        lst=curr,
                        index=key,
                        default=([] if next_key and next_key.isdigit() else {}),
                    )
                    curr = next
            elif isinstance(curr, dict):
                if next_key is None:
                    curr[key] = value
                elif key not in curr:
                    curr[key] = [] if next_key and next_key.isdigit() else {}
                curr = curr[key]

    unflattened_dict = {}

    for key, value in flat_dict.items():
        keys = re.split(r"\[|\]\[|\]", key)
        keys = [k for k in keys if k]  # Remove empty strings from the list
        set_nested_item(unflattened_dict, keys, value)

    return unflattened_dict


if __name__ == "__main__":
    app.run(
        port=os.getenv("PORT", default=8000),
        debug=True,
    )
