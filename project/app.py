from flask import Flask, render_template, request, redirect, url_for
from forms import ProfileForm
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ProfileForm()
    if form.validate_on_submit():
        data = {
            "first_name": form.first_name.data,
            "surname": form.surname.data,
            "date_of_birth": form.date_of_birth.data.strftime('%d-%m-%Y'),
            "city": form.city.data,
            "nationality": form.nationality.data,
            "availability": form.availability.data,
            "drivers_license": form.drivers_license.data,
            "profile_pic": form.profile_pic.data.filename if form.profile_pic.data else "",
            "profile_and_ambition": form.profile_and_ambition.data,
            "highlights": [highlight.highlight.data for highlight in form.highlights],
            "education": [
                {
                    "period": edu.period.data,
                    "name_education": edu.name_education.data,
                    "name_employer_client": edu.name_employer_client.data,
                    "status": edu.status.data,
                } for edu in form.education
            ],
            "courses": [
                {
                    "period": course.period.data,
                    "name_education": course.name_education.data,
                    "name_employer_client": course.name_employer_client.data,
                    "status": course.status.data,
                } for course in form.courses
            ],
            "work_experience": [
                {
                    "period": work.period.data,
                    "function_name": work.function_name.data,
                    "name_employer_client": work.name_employer_client.data,
                    "bullet_points": [bp.bullet_point.data for bp in work.bullet_points],
                } for work in form.work_experience
            ],
            "expertise_programming": [
                {
                    "name": exp.name.data,
                    "basic": exp.basic.data,
                    "good": exp.good.data,
                    "excellent": exp.excellent.data,
                } for exp in form.expertise_programming
            ],
            "expertise_languages": [
                {
                    "name": exp.name.data,
                    "basic": exp.basic.data,
                    "good": exp.good.data,
                    "excellent": exp.excellent.data,
                } for exp in form.expertise_languages
            ]
        }

        if form.profile_pic.data:
            form.profile_pic.data.save(os.path.join('static', form.profile_pic.data.filename))

        with open(os.path.join('data', 'profile_data.json'), 'w') as f:
            json.dump(data, f, indent=4)

        return redirect(url_for('index'))

    return render_template('form.html', form=form)

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    app.run(debug=True)
