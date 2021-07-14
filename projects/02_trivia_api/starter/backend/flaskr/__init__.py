import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/*": {"origins":"*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_cat():
    categories = Category.query.all()
    result = format_categories(categories) 
    return jsonify({
      'success': True,
      'categories': result
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  '''
  @app.route('/questions')
  def get_questions():
    ### In the case of a request coming as a result of a search operation
    if 'searchTerm' in request.args :
      search = request.args.get('searchTerm')
      questions = Question.query.filter(Question.question.ilike('%' + search + '%')).all()
      formatted_questions = format_questions(questions)
  
      return jsonify({
        'questions':formatted_questions,
        'total_questions': len(questions),
        'current_category': 'all',
        'success':True,
        'status_code':200
        })
    
    
    ### regular get request

    page = request.args.get('page',1,type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE 
    end = start + QUESTIONS_PER_PAGE
    questions = Question.query.all()
    if len(questions[start:end]) == 0:
      abort(404)
    formatted_questions = format_questions(questions)
    categories = Category.query.all()
    res = format_categories(categories)
    return jsonify({
      'questions':formatted_questions[start:end],
      'total_questions': len(questions),
      'categories': res,
      'current_category': 'all',
      'success':True,
      'status_code':200
    })
  '''
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
  '''
  @app.route('/questions/<int:id>', methods=["DELETE"])
  def delete_question(id):
    question = Question.query.get(id)
    if question == None :
      abort(404)
    
    question.delete()
    return jsonify({
      'success':True,
      'status_code': 200})
  '''
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  '''
  @app.route('/questions', methods=['post'])
  def post_question():
    body = request.get_json()
    question_text = body.get('question',None)
    answer = body.get('answer',None)
    difficulty = body.get('difficulty',None)
    category = body.get('category',None)
    if question_text == '' or answer == '' or difficulty == '' or category == '':
      abort(422)
    try:
      question = Question(question=question_text,answer=answer,difficulty=difficulty,category=category)
      question.insert()
      return jsonify({'success':True})
    except:
      abort(422)
  '''
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 
  '''
  '''
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 
  '''
  @app.route('/categories/<int:id>/questions')
  def get_by_category(id):
    questions = Question.query.filter_by(category=id).all()
    category = Category.query.get(id)
    if category == None:
      abort(404)
    formatted_questions = format_questions(questions)
    return jsonify({
      'questions': formatted_questions,
      'total_questions': len(questions),
      'current_category':category.type,
      'success':True,
      'status_code': 200
    })


  '''
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quiz():
    body = request.get_json()
    previous_questions = body.get('previous_questions')
    category = body.get('quiz_category')
    if category['id'] == 0:
      questions = Question.query.filter(Question.id.not_in(previous_questions)).all()
      length = len(questions)
    else:
      if not Category.query.get(category['id']):
        abort(404)
      questions = Question.query.filter_by(category = category['id']).filter(Question.id.not_in(previous_questions)).all()
      length = len(questions)
    if length == 0:
      return jsonify({
        'question': None
      })
    
    ## selects a random number between 0 and the length of the array of questions. [0,length)
    index = random.randrange(0,length)
    question = questions[index]
    
    return jsonify({
      'question': question.format(),
      'success': True,
      'status_code':200})
  '''
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

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
      'message': "The request was well-formed but was unable to be followed due to semantic errors."
    }), 422
    @app.errorhandler(500)
    def internal_error(error):
      return jsonify({
        'success': False,
        'error': 500,
        'messge': 'Internal server error.'
      }), 500

  
  return app

# Helper method to return questions in the proper form
def format_questions(questions):
  res = []
  for question in questions:
    data = question.format()
    res.append(data)
  return res

# Helper method to return categories in the proper form
def format_categories(categories):
    res = {}
    for cat in categories:
      res[cat.id] = cat.type
    return res

  

    