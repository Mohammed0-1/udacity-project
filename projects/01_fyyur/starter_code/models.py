from flask_sqlalchemy import SQLAlchemy
from datetime import *

db = SQLAlchemy()

class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer,primary_key=True)
    venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'))
    artist_id = db.Column( db.Integer, db.ForeignKey('Artist.id'))
    start_date = db.Column(db.DateTime,default=datetime.utcnow(),nullable=False)
    venue = db.relationship('Venue',backref=db.backref('shows',lazy=True))
    artist = db.relationship('Artist',backref=db.backref('shows',lazy=True))

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, default = False)
    description = db.Column(db.String(),nullable=True)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120),nullable=True)
    seeking_venue = db.Column(db.Boolean, default = False)
    description = db.Column(db.String(),nullable=True)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.