from flask import Flask, render_template, redirect, url_for, flash
from forms import ProfileForm
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF protection


@app.route("/", methods=["GET"])
def index():
    return render_template("form.html", form=ProfileForm())


@app.route("/", methods=["POST"])
def submit_form():
    form = ProfileForm()

    # Save form data
    form_data = {
        "first_name": form.first_name.data,
        "surname": form.surname.data,
        "date_of_birth": form.date_of_birth.data.strftime("%d-%m-%Y"),
        "city": form.city.data,
        "nationality": form.nationality.data,
        "availability": form.availability.data.strftime("%d-%m-%Y"),
        "drivers_license": form.drivers_license.data,
        "profile_and_ambition": form.profile_and_ambition.data,
        "highlights": [highlight.highlight.data for highlight in form.highlights],
        "education": [
            {
                "period": edu.period.data,
                "name_education": edu.name_education.data,
                "name_employer_client": edu.name_employer_client.data,
                "status": edu.status.data,
            }
            for edu in form.education
        ],
        "courses": [
            {
                "period": course.period.data,
                "name_education": course.name_education.data,
                "name_employer_client": course.name_employer_client.data,
                "status": course.status.data,
            }
            for course in form.courses
        ],
        "work_experience": [
            {
                "period": work.period.data,
                "function_name": work.function_name.data,
                "name_employer_client": work.name_employer_client.data,
                "bullet_points": [bp.bullet_point.data for bp in work.bullet_points],
            }
            for work in form.work_experience
        ],
        "expertise_sections": [
            {
                "title": section.title.data,
                "items": [
                    {"expertise": item.expertise.data, "level": item.level.data}
                    for item in section.items
                ]
            }
            for section in form.expertise_sections
        ],
    }

    # # Handle file upload
    # if form.profile_pic.data:
    #     filename = secure_filename(form.profile_pic.data.filename)
    #     form.profile_pic.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #     form_data['profile_pic'] = filename

    # Save form_data to a file or database
    # For example, saving to a JSON file:
    with open('form_data.json', 'w') as f:
        json.dump(form_data, f, indent=2)

    return "Form submitted successfully!"


if __name__ == "__main__":
    app.run(port=8000, debug=True)
