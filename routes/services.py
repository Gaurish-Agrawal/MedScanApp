from flask import render_template, Blueprint, url_for, request
from flask_login import login_required
from flask_uploads import IMAGES, UploadSet
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import send_from_directory
from wtforms import SubmitField
from app import facialrec
import scrape
from flask_login import current_user
from app.db import db

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

@services_blueprint.route('/edithome', methods=["GET", "POST"])
@login_required
def cdashboard():
    msg = ""

    name = current_user.name
    email = current_user.email
    gender = current_user.gender
    birthday = current_user.birthday
    height = current_user.height
    age = current_user.age
    ec = current_user.econtact
    medcon = current_user.condition

    if request.method == "POST":
        height = request.form.get("height")
        age = request.form.get("age")
        birthday = request.form.get("birthday")
        gender = request.form.get("gender")
        medcon = request.form.get("medcon")
        ec = request.form.get("ec")

        # user = User.query.filter_by(email=email).first()
        current_user.height = height
        current_user.age = age
        current_user.birthday = birthday
        current_user.gender = gender
        current_user.condition = medcon
        current_user.econtact = ec
        db.session.commit()

        print("Updated Edits\n\n\n\n\n")

        msg = "Information Updated"

    return render_template('cdashboard.html', name=name, email=email, height=height, age=age, ec=ec, birthday=birthday,
                           gender=gender, medcon=medcon, msg=msg)