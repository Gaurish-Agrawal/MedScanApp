from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    type =  db.Column(db.String(15))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    image_path = db.Column(db.String(100))
    height = db.Column(db.String(100))
    age = db.Column(db.String(100))
    condition = db.Column(db.String(100))
    birthday = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    econtact = db.Column(db.String(100))

    def __init__(self, type, name, email, password, image_path, height, age, condition, birthday, gender, econtact):
        self.type = type
        self.name = name
        self.email = email
        self.password = password
        self.image_path =  image_path
        self.height = height
        self.age = age
        self.condition = condition
        self.birthday = birthday
        self.gender = gender
        self.econtact = econtact

