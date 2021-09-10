import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Actor, Movie
from auth import AuthError, requires_auth
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  db_drop_and_create_all()
  CORS(app, resources={r"/*": {"origins":"*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
    return response

  @app.route('/')
  def root():
    return 'https://dev-z6rs6ps7.us.auth0.com/authorize?audience=casting_agency&response_type=token&client_id=VB4qQBe6zyO4GeXscN992O8rnHkwbMKV&redirect_uri=http://127.0.0.1:5000/'

  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(payload):
    actors = Actor.query.all()
    res = format_actors(actors)
    return jsonify({
      'success': True,
      'Actors': res})


  @app.route('/actors', methods=['POST'])
  @requires_auth('add:actors')
  def create_actor(payload):
    body = request.get_json()
    name = body.get('name',None)
    age = body.get('age',None)
    gender = body.get('gender', None)

    if name == '' or age == '' or gender == '':
      abort(422)
    
    try:
      actor = Actor(name=name,age=age,gender=gender)
      actor.create()
      return jsonify({'success':True})
    except:
      abort(422)
  
  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def edit_actor(payload, id):
    actor = Actor.query.get(id)
    if actor == None:
      abort(404)
    
    body = request.get_json()
    if body.get('name'):
      actor.name = body.get('name')
    if body.get('age'):
      actor.age = body.get('age')
    
    actor.update()
    return jsonify({
      'success': True
    })

  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, id):
    actor = Actor.query.get(id)
    if actor == None:
      abort(404)
    actor.delete()
    return jsonify({
      'success': True
    }) 

  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(payload):
    movies = Movie.query.all()
    res = format_movies(movies)
    return jsonify({
      'success': True,
      'movies': res
    })
  
  
  @app.route('/movies', methods=['POST'])
  @requires_auth('add:movies')
  def create_movie(payload):
    body = request.get_json()
    title = body.get('title',None)
    release_date = body.get('release date',None)

    if title == '' or release_date == '':
      abort(422)
    
    try:
      movie = Movie(title=title,release_date=release_date)
      movie.create()
      return jsonify({'success':True})
    except:
      abort(422)

  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def edit_movie(payload, id):
    movie = Movie.query.get(id)
    if movie == None:
      abort(404)
    
    body = request.get_json()
    if body.get('title'):
      movie.title = body.get('title')
    if body.get('release date'):
      movie.release_date = body.get('release date')
    
    movie.update()
    return jsonify({
      'success': True
    })

  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, id):
    movie = Movie.query.get(id)
    if movie == None:
      abort(404)
    movie.delete()
    return jsonify({
      'success': True
    })  

#Error handelers for : 400,404,422,500

  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
      'success': False,
      'error' : error.status_code,
      'message': error.error['code']
      }), error.status_code

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': "Bad Request."
    })
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found."
        }), 404
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': "The request was well-formed but can not be processed due to semantic errors."
    }), 422
    @app.errorhandler(500)
    def internal_error(error):
      return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal server error.'
      }), 500
    
        
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

def format_actors(actors):
  res = []
  for actor in actors:
    data = actor.format()
    res.append(data)
  return res

def format_movies(movies):
    res = []
    for movie in movies:
      data = movie.format()
      res.append(data)
    return res