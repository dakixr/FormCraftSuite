from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, FileField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired

class HighlightForm(FlaskForm):
    highlight = StringField('Highlight', validators=[DataRequired()])

class BulletPointForm(FlaskForm):
    bullet_point = StringField('Bullet Point', validators=[DataRequired()])

class EducationForm(FlaskForm):
    period = StringField('Period', validators=[DataRequired()])
    name_education = StringField('Name of Education', validators=[DataRequired()])
    name_employer_client = StringField('Name of School', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Ongoing', 'Ongoing'), ('Finished', 'Finished')])

class CourseForm(FlaskForm):
    period = StringField('Period', validators=[DataRequired()])
    name_education = StringField('Name of Education', validators=[DataRequired()])
    name_employer_client = StringField('Name of School', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Ongoing', 'Ongoing'), ('Finished', 'Finished')])

class WorkExperienceForm(FlaskForm):
    period = StringField('Period', validators=[DataRequired()])
    function_name = StringField('Function Name', validators=[DataRequired()])
    name_employer_client = StringField('Name of Employer/Client', validators=[DataRequired()])
    bullet_points = FieldList(FormField(BulletPointForm), min_entries=1, max_entries=10)

class ExpertiseForm(FlaskForm):
    expertise = StringField('Expertise', validators=[DataRequired()])
    level = SelectField('Level', choices=[("1","1"), ("2", "2"), ("3", "3")])

class ExpertiseSectionForm(FlaskForm):
    title = StringField('Section Title', validators=[DataRequired()])
    items = FieldList(FormField(ExpertiseForm), min_entries=1, max_entries=10)

class ProfileForm(FlaskForm):
    function = StringField('Function Name', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    nationality = StringField('Nationality', validators=[DataRequired()])
    availability = DateField('Availability', format='%Y-%m-%d', validators=[DataRequired()])
    drivers_license = SelectField('Driver\'s License', choices=[('Yes', 'Yes'), ('No', 'No')])
    profile_pic = FileField('Profile Picture')
    profile_and_ambition = TextAreaField('Profile and Ambition', validators=[DataRequired()])
    highlights = FieldList(FormField(HighlightForm), min_entries=1, max_entries=10)
    education = FieldList(FormField(EducationForm), min_entries=1, max_entries=10)
    courses = FieldList(FormField(CourseForm), min_entries=1, max_entries=10)
    work_experience = FieldList(FormField(WorkExperienceForm), min_entries=1, max_entries=10)
    expertise_sections = FieldList(FormField(ExpertiseSectionForm), min_entries=1, max_entries=5)