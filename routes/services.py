from flask import render_template, Blueprint, url_for
from flask_login import login_required
from flask_uploads import IMAGES, UploadSet
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import send_from_directory
from wtforms import SubmitField
from app import facialrec
import scrape

# Create services blueprint
services_blueprint = Blueprint('services', __name__, template_folder='templates')

photos = UploadSet('photos', IMAGES, default_dest="./views/static/images/uploads/")
class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('Feil Field should not be empty'),
        ]
    )
    submit = SubmitField('Upload')


# make default route ""


@services_blueprint.route('/home', methods=["GET", "POST"])
@login_required
def dashboard():
    name = gender = bd = height = age = ec = None
    medcon = []

    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        prefix = r'/Users/gaurishagrawal/Desktop/medscanhack/views/static/images'
        file_url = url_for('get_file', filename=filename)
        data = facialrec.returndata(prefix + file_url)
        if data:
            name = data[-1]
            name = name
            gender = data[0].title()
            bd = data[1]
            height = data[2]
            age = data[3]
            medcon = data[4]
            ec = data[-2]
    else:
        file_url = None
    l = []
    for i in medcon:
        d = scrape.getapidata(i)
        l.append([i, d])
    return render_template('dashboard.html', form=form, file_url=file_url, name=name, bd=bd, gender=gender, height=height,
                           age=age, medcon=l, ec=ec)

