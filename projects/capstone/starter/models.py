import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json


database_name = "casting_agency"
user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
database_path = "postgresql://{}:{}@{}/{}".format(user, password, 'localhost:5432', database_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key =True)
    title = db.Column(db.String, nullable = False)
    release_date = db.Column(db.Date, nullable= False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
    
    def create(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'title': self.title,
            'release date': self.release_date}
        
    


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    age = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String, nullable = False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    
    def create(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }