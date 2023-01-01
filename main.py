from flask import Flask, render_template, redirect, request, Blueprint, url_for, send_from_directory
import os
from flask_bootstrap import Bootstrap5
from flask_uploads import UploadSet, IMAGES, configure_uploads
from app.db import db
from routes.auth import auth_blueprint, images
from routes.auth import login_manager
from flask_login import login_required, current_user
from routes.misc import misc_blueprint
from routes.services import services_blueprint, photos
from app.db import db

# Defining secret key, app, and templates directory
template_dir = os.path.abspath('views/templates')
static_dir = os.path.abspath('views/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
boostrap = Bootstrap5()

app.config['SECRET_KEY'] = ';lkja;lkjg;lajk4oi;h    '
app.config['UPLOAD_FOLDER'] = "./"
app.config['UPLOADED_PHOTOS_DEST'] = "./views/static/images/uploads/"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Register photo folders
configure_uploads(app, images)
configure_uploads(app, photos)

#Registering Blueprints
app.register_blueprint(auth_blueprint, url_prefix="")
app.register_blueprint(misc_blueprint, url_prefix="")
app.register_blueprint(services_blueprint, url_prefix="")

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory("./views/static/images/uploads/", filename)


with app.app_context():

    db.init_app(app)
    db.drop_all() #reset database
    db.create_all()
    
    login_manager.init_app(app)
    boostrap.init_app(app)
    
app.run(debug=True)


