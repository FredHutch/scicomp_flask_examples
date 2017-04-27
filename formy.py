from flask import Flask, url_for, redirect, render_template
from flask_wtf import Form
from flask_wtf.file import FileField
from werkzeug import secure_filename

class UploadForm(Form):
    file = FileField()

app = Flask(__name__) # pylint: disable=invalid-name
app.config['WTF_CSRF_SECRET_KEY'] = 'a random stringsdslkdjfjldkghlfkj'
app.secret_key = 'dsjhglfkjghflkjhflgfhlkj'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('uploads/' + filename)
        return redirect(url_for('upload'))

    return render_template('upload.html', form=form)
