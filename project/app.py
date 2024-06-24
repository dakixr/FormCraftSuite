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

    # # Handle file upload
    # if form.profile_pic.data:
    #     filename = secure_filename(form.profile_pic.data.filename)
    #     form.profile_pic.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #     form_data['profile_pic'] = filename

    # Save form_data to a file or database
    # For example, saving to a JSON file:
    with open('form_data.json', 'w') as f:
        json.dump(form.data, f, indent=2, default=str)

    return "Form submitted successfully!"


if __name__ == "__main__":
    app.run(port=8000, debug=True)
