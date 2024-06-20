from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from forms import ProfileForm
import pprint

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ProfileForm()
    if form.validate_on_submit():
        # Save form data
        form_data = {
            'first_name': form.first_name.data,
            'surname': form.surname.data,
            'date_of_birth': form.date_of_birth.data.strftime('%d-%m-%Y %Y-%m-'),
            'city': form.city.data,
            'nationality': form.nationality.data,
            'availability': form.availability.data.strftime('%d-%m-%Y'),
            'drivers_license': form.drivers_license.data,
            'profile_and_ambition': form.profile_and_ambition.data,
            'highlights': [highlight.highlight.data for highlight in form.highlights],
            'education': [{'period': edu.period.data, 'name_education': edu.name_education.data, 'name_employer_client': edu.name_employer_client.data, 'status': edu.status.data} for edu in form.education],
            'courses': [{'period': course.period.data, 'name_education': course.name_education.data, 'name_employer_client': course.name_employer_client.data, 'status': course.status.data} for course in form.courses],
            'work_experience': [{'period': work.period.data, 'function_name': work.function_name.data, 'name_employer_client': work.name_employer_client.data, 'bullet_points': [bp.bullet_point.data for bp in work.bullet_points]} for work in form.work_experience],
            'expertise_programming': [{'expertise': exp.expertise.data, 'level': exp.level.data} for exp in form.expertise_programming],
            'expertise_languages': [{'expertise': exp.expertise.data, 'level': exp.level.data} for exp in form.expertise_languages]
        }
        # Handle file upload
        # if form.profile_pic.data:
        #     profile_pic = form.profile_pic.data
        #     filename = secure_filename(profile_pic.filename)
        #     profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     form_data['profile_pic'] = filename

        # Simulating save operation
        print("Form data saved successfully!")
        pprint.pprint(form.data)
        flash('Form submitted successfully!', 'success')
        return redirect(url_for('index'))
        
    return render_template('form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)