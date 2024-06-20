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
        return

        if form.profile_pic.data:
            form.profile_pic.data.save(os.path.join('static', form.profile_pic.data.filename))

        with open(os.path.join('data', 'profile_data.json'), 'w') as f:
            json.dump(data, f, indent=4)

        return redirect(url_for('index'))

    return render_template('form.html', form=form)

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    app.run(debug=True)
