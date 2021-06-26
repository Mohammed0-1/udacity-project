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
from models import Show, Artist,Venue



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
  shows = Show.query.join(Venue, Show.venue_id == Venue.id).filter(Venue.id == venue_id)
  past_shows = []
  upcoming_shows = []
  for show in shows.filter(Show.start_date < datetime.utcnow()).all():
    data = {
      'artist_id':show.artist_id,
      'artist_name':show.artist.name,
      'artist_image_link':show.artist.image_link,
      'start_time':str(show.start_date)}
    past_shows.append(data)

  for show in shows.filter(Show.start_date > datetime.utcnow()).all():
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
    form = VenueForm(request.form)
    if form.validate():
      name = form.name.data
      city = form.city.data
      state = form.state.data
      address = form.address.data
      phone = form.phone.data
      genres = form.genres.data
      facebook_link = form.facebook_link.data
      image_link = form.image_link.data
      website_link = form.website_link.data
      seeking_talent = form.seeking_talent.data
      description = form.seeking_description.data
      venue = Venue(name=name,city=city,state=state,address=address,phone=phone,genres=genres,
                  facebook_link=facebook_link,image_link=image_link,website_link=website_link,
                  seeking_talent=seeking_talent,description=description)
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else:
      flash('The data you have entered is invalid')
  # on successful db insert, flash success
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
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
  shows = Show.query.join(Artist, Show.artist_id == Artist.id).filter(Artist.id == artist_id)
  past_shows = []
  upcoming_shows = []
  for show in shows.filter(Show.start_date < datetime.utcnow()).all():
    data = {
      'venue_id':show.venue_id,
      'venue_name':show.venue.name,
      'venue_image_link':show.venue.image_link,
      'start_time':str(show.start_date)}
    past_shows.append(data)

  for show in shows.filter(Show.start_date > datetime.utcnow()).all():
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
    form = ArtistForm(request.form)
    if form.validate():
      artist = Artist.query.get(artist_id)
      artist.name = form.name.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.genres = form.genres.data
      artist.facebook_link = form.facebook_link.data
      artist.image_link = form.image_link.data
      artist.website_link = form.website_link.data
      artist.seeking_venue = form.seeking_venue.data
      artist.description = form.seeking_description.data
      db.session.commit()
    else:
      flash('The data you have entered is invalid')
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
    form = VenueForm(request.form)
    if form.validate():
      venue = Venue.query.get(venue_id)
      venue.name = form.name.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.address = form.address.data
      venue.phone = form.phone.data
      venue.genres = form.genres.data
      venue.facebook_link = form.facebook_link.data
      venue.image_link = form.image_link.data
      venue.website_link = form.website_link.data
      venue.seeking_talent = form.seeking_talent.data
      venue.description = form.seeking_description.data
      db.session.commit()
    else:
      flash('The data you have entered is invalid')
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
    form = ArtistForm(request.form)
    if form.validate():
      name = form.name.data
      city = form.city.data
      state = form.state.data
      phone = form.phone.data
      genres = form.genres.data
      facebook_link = form.facebook_link.data
      image_link = form.image_link.data
      website_link = form.website_link.data
      seeking_venue = form.seeking_venue.data
      description = form.seeking_description.data
      artist = Artist(name=name,city=city,state=state,phone=phone,genres=genres,
                    facebook_link=facebook_link,image_link=image_link,website_link=website_link,
                    seeking_venue=seeking_venue,description=description)
      db.session.add(artist)
      db.session.commit()
    # called upon submitting the new artist listing form
    # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else:
      flash('The data you have entered is invalid')
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
    form = ShowForm(request.form)
    artist_id = form.artist_id.data
    venue_id = form.venue_id.data
    start_time = form.start_time.data
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
