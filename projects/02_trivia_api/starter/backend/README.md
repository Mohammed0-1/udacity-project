# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r modified_requirements.txt
```
This will install all of the required packages we selected within the `modified_requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


Endpoints
GET '/categories'
GET '/questions'
GET '/categories/<id>/questions'
POST '/questions'
POST '/quizzes'
DELETE '/questions/<id>'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a two keys,success, which indicates if the request have succeeded or failed. And categories, that contains a object of id: category_string key:value pairs. 
{{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"},
'success': True}

GET '/questions'
- Fetches a list of questions with thier answers, categories and thier difficulty levels.
If the search argument is provided; the endpoint will fetch the questions that include the search term. The same aforementioned attributes will be returned.
- Request Arguments: searchTerm (optional)
- Returns: An object with five keys: 
1- questions, which contains a list of questions with releated data.
2- total_questions, which returns the number of questions that exist in the app.
3- current_categroy, which describes the category of questions.
4- success, which indicates if the request has succeeded of failed.
5- status_code, which returns the HTTP status code of the response.

GET '/categories/5/quesions'
- Fetches a list of questions that fall under the category with id 5 with the related data: answer, category and difficulty level.
In addition, it will fetch the number of questions in the category of ID 5. As well as an object that contains the ID and the category name.
- Request Arguments: The category ID
- Returns: An object with five keys: 
1- questions, which contains a list of questions with releated data.
2- total_questions, which returns the number of questions that exist in the app.
3- current_categroy, which describes the category of questions.
4- success, which indicates if the request has succeeded of failed.
5- status_code, which returns the HTTP status code of the response. 

POST '/questions'
- Posts a new question in the app.
- Request Arguments: The question, The answer, The category and the difficulty level
- Returns: A variable "success" that indicates if the request passed or failed. The request fails in the case of a missing argument.

POST '/quizzes'
- Fetches a single question with its releated date: answer, category and difficulty level.
- Request Arguments:
1- previous_questions, which is a list that includes the id of the questions that have been displayed to the user.
2- quiz_category, which indicates the category of the question that will be displayed 
- Returns: A single question with its related data.

DELETE '/questions/2'
- Deletes the question with ID of 2.
- Request Arguments: The ID of the question to be deleted.
- Returns: A "Success" variable that indicates if the request have been fulfilled or not.

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
