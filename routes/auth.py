from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, StringField, PasswordField, EmailField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length, AnyOf, EqualTo, ValidationError
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask import Flask, render_template, redirect, request, Blueprint, session, url_for, flash
from app.db import db, User
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import pickle

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
images = UploadSet('photos', IMAGES)


@login_manager.unauthorized_handler  # login page
def unauthorized():
    return redirect(url_for('auth.login'))


class Register_Form(FlaskForm):
    account_type = SelectField('account_type', choices=["Paramedic", "Citizen"])
    username = StringField('Name', validators=[InputRequired(), Length(min=4, max=15)])
    email = EmailField('Email', validators=[InputRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm = PasswordField('Confirm Password',
                            validators=[InputRequired(), EqualTo('password', message='Passwords must match')])


class Login_Form(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ["jpeg", "jpg", "png"]


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter(User.id == user_id).first()


@auth_blueprint.route('/auth/upload', methods=["POST", "GET"])
def upload():
    print("test","\n\n\n\n")
    email = current_user.email
    if request.method == "POST":
        user = db.session.query(User).filter(User.email == email).first()
        if "file" in request.files:
            file = request.files["file"]
            file.filename = current_user.name.title() + "." + (file.filename.split('.'))[-1]
            if file and allowed_file(file.filename):
                image_name = secure_filename(file.filename)
                path = r"./faces/" + image_name
                user.file_path = path
                file.save(path)

                lst = []

                #only for first run (not needed anymore!)
                with open('file.pkl', 'wb') as pickle_file:
                    pickle.dump(lst, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
                

                with open('file.pkl', 'rb') as pickle_load:
                    lst = pickle.load(pickle_load)

                lst.append(current_user.name)
                with open('file.pkl', 'wb') as pickle_file:
                    pickle.dump(lst, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
           
                    #for citizens
                return redirect(url_for("auth.cdashboard"))

    return render_template('upload.html')


@auth_blueprint.route('/edithome', methods=["GET", "POST"])
@login_required
def cdashboard():

    msg = ""

    name = current_user.name
    email = current_user.email
    gender = current_user.gender
    birthday =current_user.birthday
    height =current_user.height
    age =current_user.age
    ec = current_user.econtact
    medcon = current_user.condition

    if request.method == "POST":
        height = request.form.get("height")
        age = request.form.get("age")
        birthday = request.form.get("birthday")
        gender = request.form.get("gender")
        medcon = request.form.get("medcon")
        ec = request.form.get("ec")


        #user = User.query.filter_by(email=email).first()
        current_user.height = height
        current_user.age = age
        current_user.birthday = birthday
        current_user.gender = gender
        current_user.condition = medcon
        current_user.econtact = ec
        db.session.commit()

        print("Updated Edits\n\n\n\n\n")

        msg = "Information Updated"
  
    return render_template('cdashboard.html', name=name, email=email, height=height, age=age, ec=ec, birthday=birthday, gender=gender, medcon=medcon, msg=msg)


@auth_blueprint.route('/auth/register', methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("services.dashboard"))
    form = Register_Form()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user is not None:
            form.email.errors.append('You already have an account. Please log in.')
            return render_template('register.html', form=form)
        if form.account_type.data == "Citizen":
            if request.method == "POST":
                height = request.form.get("height")
                age = request.form.get("age")
                birthday = request.form.get("birthday")
                gender = request.form.get("gender")
                condition = request.form.get("conditions")
                ec = request.form.get("ec")




            new_user = User(type=form.account_type.data, name=form.username.data, email=form.email.data,
                            password=generate_password_hash(form.password.data),
                            image_path="", height=height, age=age, condition=condition,birthday=birthday,gender=gender,econtact=ec)
            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("auth.upload"))



        elif form.account_type.data == "Paramedic":
            new_paramedic = User(type=form.account_type.data, name=form.username.data, email=form.email.data,
                            password=generate_password_hash(form.password.data), image_path="", height=None, age=None, condition=None,birthday=None,gender=None,econtact=None)
            db.session.add(new_paramedic)
            db.session.commit()
            login_user(new_paramedic)
            return redirect(url_for("services.dashboard"))

    return render_template('register.html', form=form)



@auth_blueprint.route('/auth/login', methods=["POST", "GET"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("services.dashboard"))
    
    form = Login_Form()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first() #None
        if user is None:
            form.email.errors.append('You do not have a account please register')

            return render_template('login.html', form=form)
        elif check_password_hash(user.password, form.password.data): #not check_password_hash(user.password, form.password.data)

            form.password.errors.append('Please check your login details.')
            return render_template('login.html', form=form)
        else:

            login_user(user)

            if user.account_type=="Paramedic":
                return redirect(url_for("services.dashboard"))
            else:
                return "Hello World"

    else:
        return render_template('login.html', form=form)


@auth_blueprint.route('/logout', methods=["POST", "GET"])
def logout():
    logout_user()
    return redirect(url_for("auth.login"))