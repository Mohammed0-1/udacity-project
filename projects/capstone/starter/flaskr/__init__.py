import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/*": {"origins":"*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
    return response

  @app.route('/')
  def root():
    return '200'

  @app.route('/actors', methods=['GET'])
  def get_actors():
    pass # Todo
  @app.route('/actors', methods=['POST'])
  def create_actor():
    pass #Todo
  
  @app.route('/actor/<int:id>', methods=['PATCH'])
  def edit_actor(id):
    pass #Todo

  @app.route('/actor/<int:id>', methods=['DELETE'])
  def delete_actor(id):
    pass #Todo  
  @app.route('/movies', methods=['GET'])
  def get_movies():
    pass #Todo
  
  
  @app.route('/movies', methods=['POST'])
  def create_movie():
    pass #Todo

  @app.route('/movie/<int:id>', methods=['PATCH'])
  def edit_movie(id):
    pass #Todo

  @app.route('/movie/<int:id>', methods=['DELETE'])
  def delete_movie(id):
    pass #Todo  
  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)