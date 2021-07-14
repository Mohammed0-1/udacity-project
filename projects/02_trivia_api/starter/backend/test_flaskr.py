import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','root','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
    
    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['status_code'], 200)
    
    def test_404_get_questions(self):
        res = self.client().get('/questions?page=10')
        data = json.loads(res.data)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['error'], 404)
    
    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_code'],200)
    
    def test_404_delete_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
    
    def test_post_question(self):
        res = self.client().post('/questions', json={
        'question': 'Who won the 2020 euros?',
        'answer': 'Italy',
        'difficulty':2,
        'category':6})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
    
    def test_422_post_question(self):
        res = self.client().post('/questions', json={
        'question': '',
        'answer': '',
        'difficulty':2,
        'category':6})
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
    
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['status_code'], 200)
    
    def test_404_get_questions_by_category(self):
        res = self.client().get('/categories/99/questions')
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
    
    def test_get_quiz(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category':{'id':1, 'type':'Science'}
        })
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['status_code'],200)
    
    def test_404_get_quiz(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category':{'id':100, 'type':'Ex'}
        })
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'],404)
    
    def test_search(self):
        res = self.client().get('/questions?searchTerm=title')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['status_code'],200)
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()