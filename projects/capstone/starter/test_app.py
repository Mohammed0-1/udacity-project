import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import db_drop_and_create_all, setup_db, Movie, Actor


class castingAgencyTestCase(unittest.TestCase):
    """This class represents the casting_agency test case"""


    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        user = os.environ.get('POSTGRES_USER')
        password = os.environ.get('POSTGRES_PASSWORD')
        self.database_path = "postgresql://{}:{}@{}/{}".format(user,password,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.assistant_token = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVzVi1MWTNBVjhxakVDTkNCT3NmdyJ9.eyJpc3MiOiJodHRwczovL2Rldi16NnJzNnBzNy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzOGZmMDA2MzI2MWEwMDY4N2JhMWJhIiwiYXVkIjoiY2FzdGluZ19hZ2VuY3kiLCJpYXQiOjE2MzEyODEwNDQsImV4cCI6MTYzMTM2NzQ0NCwiYXpwIjoiVkI0cVFCZTZ6eU80R2VYc2NOOTkyTzhybkhrd2JNS1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.S9gb2Y7esVTI-k9sT9ra3TrIY-oclzx8zYZWFFEsVVzMlJOHnhL4SeXs9ysVkpow1L7rmO6bsUfkWzs-vpUOBQ0TncRrt98IeVNE7NGEQ3Bf1aPucpOo6APYGefhFbyJ2TqppcBopRaoOz4fdSxzdT45x6Ln-isW6ckahTN7jJbZn2xqGj5K1aZZLQ95T83W_cR4m134SgZ-v1572hqIvMjhWO13h-StfiDQm_2-Bvn3yAv7CZqmnIWlqbgirArrBGahpPHtom43i4tWc_PtIlhQXa8FSdIjI-O1wqh9nZ2gueaPd21QDE8DtTsB3TDFmimwtDh36m96eF-Ve-F5pQ'
        self.director_token = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVzVi1MWTNBVjhxakVDTkNCT3NmdyJ9.eyJpc3MiOiJodHRwczovL2Rldi16NnJzNnBzNy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzYjg5NmE2MzI2MWEwMDY4N2MzZjk5IiwiYXVkIjoiY2FzdGluZ19hZ2VuY3kiLCJpYXQiOjE2MzEyOTE4NTYsImV4cCI6MTYzMTM3ODI1NiwiYXpwIjoiVkI0cVFCZTZ6eU80R2VYc2NOOTkyTzhybkhrd2JNS1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiXX0.zAA8i7lZdjovILZ2ZE6eXES1SPmSx8nhlO2LwmKABXE3AesDly7pFNFViXE0_BDCGJHe8vi_J-fFvRtcsjpDKuRQ35QV16cEh4Z07zXIzMN4vn00-saDx8HO9WVLbe4C7-RnQ-CusLSyvZAKATkcra81KYGVcCVfROiguWFwkUENfk3iuTMDj5_1I4MpPqLGAJVmHKQQmS8-tXKjK5y6d6e83qXJvbzWy0dSo8_uTQJl7OwmooOt317n_Vp_PNSyhcqk_ou_OaRvcwiNKf7c6emNXqHgigwNqT_DYASYwYLdbbvw1TReWFeCCbbqIRncyBZvCUY6-h_M8vyhK7DXTw'
        self.executive_token = 'bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVzVi1MWTNBVjhxakVDTkNCT3NmdyJ9.eyJpc3MiOiJodHRwczovL2Rldi16NnJzNnBzNy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzYmEwYmU0ZmVjNmQwMDY4MmIxN2Q1IiwiYXVkIjoiY2FzdGluZ19hZ2VuY3kiLCJpYXQiOjE2MzEyOTc4MTUsImV4cCI6MTYzMTM4NDIxNSwiYXpwIjoiVkI0cVFCZTZ6eU80R2VYc2NOOTkyTzhybkhrd2JNS1YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyJdfQ.fRjeM8Ypnc5zD2zdLMQrG_-1cX30DFyGyOU12omLWYNYNDBW2QCJEHzm816vlBSPKDBTlgV4QKpHRphLCYsPCAPB7qku8aAGI0T_HnizRZSHbvQgfkzL_XIGtw9esbPHVcEokT33izfdYYlabyPUKawlMEtImCN0P_oRIdSEC5qBxynBTGNj1XW9BLAaRir9YrNkjbL9_BEK18gO0Xs1QyPLmrFMOBPURqqaqEtnnwhDYbh1RtWVK4C8kb2oHh0ATKMkeBUlwlTyJyYk47UGYX6AHZ4oODreiCCxWCmGHkks8rcJd1LjdWHKf6mzAI-_d5z-S3poEqxtxFVx_sB40A'

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            #self.db.drop_all()
            # create all tables
            #self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        db_drop_and_create_all()
        
    
    #Test Cases for Route: /actors
    
    # Method: get
    
    #1- suceessful request

    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': self.assistant_token})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)

    #2- Failed request , 401
    
    def test_401_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
    
    #Method: Post

    #1- Successful 
    def test_create_actor(self):
        res = self.client().post('/actors',
         headers={'Authorization': self.director_token},
         json={'name':'Mohammed', 'age': 20, 'gender':'Male'})
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
    
    #2- Failed request, 422
    def test_422_create_actor(self):
        res = self.client().post('/actors', headers={'Authorization': self.director_token},
        json={'name':'', 'age':'', 'gender':''})
        data = json.loads(res.data)
        self.assertEqual(data['success'],False)

    #Method: Patch

    #1- Successful
    def test_patch_actor(self):
        res = self.client().patch('/actors/1', headers={'Authorization': self.director_token},
        json={'name':'Mohammed', 'age': 22, 'gender':'Male'})
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
    
    #2- Failed request, 404
    def test_404_patch_actor(self):
        res = self.client().patch('/actors/1000', headers={'Authorization': self.director_token},
        json={'name':'Mohammed', 'age': 20})
        data = json.loads(res.data)
        self.assertEqual(data['success'],False)
    
    #Method: Delete

    #1- Successful
    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers={'Authorization': self.director_token})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
    
    #2- Failed request
    def test_404_delete_actor(self):
        res = self.client().delete('/actors/1000', headers={'Authorization': self.director_token})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
    
    #Test cases for Route: /movies 
    
    #Method: get

    #1- Successful request
    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': self.director_token})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
    
    #2- Failed request, 401
    def test_401_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)

    #Method: Post

    #1- Successful request
 
    def test_create_movie(self):
        res = self.client().post('/movies',
         headers={'Authorization': self.executive_token},
         json={'title':'Joker', 'release date': '2019-5-6'})
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
    
    #2- Failed request, 422
    def test_422_create_movie(self):
        res = self.client().post('/actors', headers={'Authorization': self.executive_token},
        json={'title':'', 'release date':''})
        data = json.loads(res.data)
        self.assertEqual(data['success'],False)

    #Method: Patch

    #1- Successful
    def test_patch_movie(self):
        res = self.client().patch('/movies/1', headers={'Authorization': self.director_token},
        json={'title':'The dark knight', 'release date': '2008-9-5'})
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
    
    #2- Failed request, 404
    def test_404_patch_movie(self):
        res = self.client().patch('/movies/1000', headers={'Authorization': self.director_token},
        json={'title':'The dark knight', 'release date': '2008-9-5', 'gender':'Male'})
        data = json.loads(res.data)
        self.assertEqual(data['success'],False)
    
    #Method: Delete

    #1- Successful
    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers={'Authorization': self.executive_token})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
    
    #2- Failed request
    def test_404_delete_movie(self):
        res = self.client().delete('/movies/1000', headers={'Authorization': self.executive_token})
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
    

    # RBAC Test cases

    #1- Casting Assistant

    # Authorized operation: get:movies
    def test_assistant_permession_success(self):
        res = self.client().get('/movies', headers={'Authorization': self.assistant_token})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)

    #Unauthorized operation: patch:movies
    def test_assistant_permession_failure(self):
        res = self.client().patch('/movies/1', headers={'Authorization': self.assistant_token},
        json={'title':'The dark knight', 'release date': '2008-9-5', 'gender':'Male'})
        data = json.loads(res.data)
        self.assertEqual(data['success'],False)
    
    #2- Casting Director
        # Authorized operation: get:movies
    def test_director_permession_success(self):
        res = self.client().get('/movies', headers={'Authorization': self.director_token})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)

    #Unauthorized operation: delete:movies
    def test_director_permession_failure(self):
        res = self.client().delete('/movies/1', headers={'Authorization': self.director_token})
        data = json.loads(res.data)
        self.assertEqual(data['success'],False)
    
    #3- Executive Producer
        # Authorized operation: create:movies
    def test_executive_permession_success(self):
        res = self.client().post('/movies',
         headers={'Authorization': self.executive_token},
         json={'title':'Lier Lier', 'release date': '2005-5-6'})
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
    #Authorized operation: delete:movies
    def test_executive_permession_success_2(self):
        res = self.client().delete('/movies/1', headers={'Authorization': self.executive_token})
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
if __name__ == "__main__":
    unittest.main()