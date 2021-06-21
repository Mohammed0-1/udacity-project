#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database

migrate = Migrate(app,db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

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

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  states_query = 'SELECT DISTINCT state FROM "Venue";'
  cities_query = 'SELECT DISTINCT city FROM "Venue" WHERE state=\'?\';'
  res = db.session.execute(states_query)

  #returns all the states in the Venues table.
  states = [row[0] for row in res]
  #loop through the states.
  for state in states:
    res = db.session.execute(cities_query.replace('?', state))

    #returns all the cities in the state
    cities = [row[0] for row in res]
    #for every city in the state, loop through the cities.
    for city in cities:
      venues_list = []

      #Find all the venues with with state = state and city = city
      venues = Venue.query.filter(Venue.state == state, Venue.city == city)

      #loop through the venues, and arrange them in a list.
      for venue in venues:
        v = {'id': venue.id, 'name': venue.name}
        venues_list.append(v)
      data.append({'state':state,'city':city,'venues':venues_list})

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search = request.form.get('search_term')

  results = Venue.query.filter(Venue.name.ilike('%' + search + '%')).all()
  data = []
  for result in results:
    data.append({'id': result.id, 'name': result.name})
  response={
    "count": len(data),
    "data":data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  genres = venue.genres.translate({ord('{'): '', ord('}'): ''}) if venue.genres else ''
  genres = genres.split(',')
  past_shows = []
  upcoming_shows = []
  for show in Show.query.filter(Show.venue_id == venue.id, Show.start_date < datetime.utcnow()).all():
    data = {
      'artist_id':show.artist_id,
      'artist_name':show.artist.name,
      'artist_image_link':show.artist.image_link,
      'start_time':str(show.start_date)}
    past_shows.append(data)

  for show in Show.query.filter(Show.venue_id == venue.id, Show.start_date > datetime.utcnow()).all():
    data = {
      'artist_id':show.artist_id,
      'artist_name':show.artist.name,
      'artist_image_link':show.artist.image_link,
      'start_time':str(show.start_date)}
    upcoming_shows.append(data)
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.description,
    "image_link": venue.image_link,
    "past_shows":past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    image_link = request.form.get('image_link')
    website_link = request.form.get('website_link')
    seeking_talent = True if request.form.get('seeking_talent') == 'y' else False
    description = request.form.get('seeking_description')
    venue = Venue(name=name,city=city,state=state,address=address,phone=phone,genres=genres,
                    facebook_link=facebook_link,image_link=image_link,website_link=website_link,
                    seeking_talent=seeking_talent,description=description)
    db.session.add(venue)
    db.session.commit()
  # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + name + ' could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = Artist.query.all()
  # TODO: replace with real data returned from querying the database
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search = request.form.get('search_term')

  results = Artist.query.filter(Artist.name.ilike('%'+search+'%')).all()
  data = []
  for result in results:
    data.append({'id':result.id, 'name':result.name})
  response={
    "count": len(data),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.get(artist_id)
  genres = artist.genres.translate({ord('{'): '', ord('}'): ''})
  genres = genres.split(',')
  past_shows = []
  upcoming_shows = []
  for show in Show.query.filter(Show.artist_id == artist.id, Show.start_date < datetime.utcnow()).all():
    data = {
      'venue_id':show.venue_id,
      'venue_name':show.venue.name,
      'venue_image_link':show.venue.image_link,
      'start_time':str(show.start_date)}
    past_shows.append(data)

  for show in Show.query.filter(Show.artist_id == artist.id, Show.start_date > datetime.utcnow()).all():
    data = {
      'venue_id':show.venue_id,
      'venue_name':show.venue.name,
      'venue_image_link':show.venue.image_link,
      'start_time':str(show.start_date)}
    upcoming_shows.append(data)
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get(artist_id)
  genres = artist.genres.translate({ord('{'): '', ord('}'): ''})
  genres = genres.split(',')
  form = ArtistForm(name=artist.name,city=artist.city,
                    state=artist.state,phone=artist.phone,genres=genres,
                    facebook_link=artist.facebook_link,website_link=artist.website_link,image_link=artist.image_link,
                    seeking_venue=artist.seeking_venue,seeking_description=artist.description)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    # TODO: take values from the form submitted, and update existing
    artist = Artist.query.get(artist_id)
    artist.name = request.form.get('name')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.phone = request.form.get('phone')
    artist.genres = request.form.getlist('genres')
    artist.facebook_link = request.form.get('facebook_link')
    artist.image_link = request.form.get('image_link')
    artist.website_link = request.form.get('website_link')
    artist.seeking_venue = True if request.form.get('seeking_venue') == 'y' else False
    artist.description = request.form.get('seeking_description')
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  genres = venue.genres.translate({ord('{'): '', ord('}'): ''}) if venue.genres else ''
  genres = genres.split(',')
  form = VenueForm(name=venue.name,city=venue.city,address=venue.address,
                    state=venue.state,phone=venue.phone,genres=genres,
                    facebook_link=venue.facebook_link,website_link=venue.website_link,image_link=venue.image_link,
                    seeking_talent=venue.seeking_talent,seeking_description=venue.description)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    venue = Venue.query.get(venue_id)
    venue.name = request.form.get('name')
    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.phone = request.form.get('phone')
    venue.genres = request.form.getlist('genres')
    venue.facebook_link = request.form.get('facebook_link')
    venue.image_link = request.form.get('image_link')
    venue.website_link = request.form.get('website_link')
    venue.seeking_talent = True if request.form.get('seeking_talent') == 'y' else False
    venue.description = request.form.get('seeking_description')
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
    
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    image_link = request.form.get('image_link')
    website_link = request.form.get('website_link')
    seeking_venue = True if request.form.get('seeking_venue') == 'y' else False
    description = request.form.get('seeking_description')
    artist = Artist(name=name,city=city,state=state,phone=phone,genres=genres,
                    facebook_link=facebook_link,image_link=image_link,website_link=website_link,
                    seeking_venue=seeking_venue,description=description)
    db.session.add(artist)
    db.session.commit()
  # called upon submitting the new artist listing form
  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
   db.session.rollback()
  # TODO: on unsuccessful db insert, flash an error instead.
   flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = db.session.query(Show)
  results = []
  for show in shows:
    data = {
     'venue_id':show.venue.id,
     'venue_name':show.venue.name,
     'artist_id':show.artist.id,
     'artist_name': show.artist.name,
      'artist_image_link':show.artist.image_link,
      'start_time':str(show.start_date)}
    results.append(data)
  return render_template('pages/shows.html', shows=results)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    artist_id = request.form.get('artist_id')
    venue_id = request.form.get('venue_id')
    start_time = request.form.get('start_time')
    venue = Venue.query.get(venue_id)
    artist = Artist.query.get(artist_id)
    show = Show(start_date=start_time)
    show.artist = artist
    show.venue = venue
    db.session.add(show)
    db.session.commit()
  # on successful db insert, flash success
    flash('Show was successfully listed!')
  except:
  # TODO: on unsuccessful db insert, flash an error instead.
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
