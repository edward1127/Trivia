# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT

This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

## Endpoints documentation

#### `GET '/categories'`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Required URL Arguments: None
- Required Data Arguments: None
- Returns: Returns Json data about categories 
- Success Response:
                    ```
                        {
                        "categories": {
                        "1": "Science",
                        "2": "Art",
                        "3": "Geography",
                        "4": "History",
                        "5": "Entertainment",
                        "6": "Sports"
                        },
                        "status_code": 200,
                        "status_message": "OK",
                        "success": true,
                        "total_categories": 6
                        }
                    ```

#### `GET '/questions'`
- Fetches a dictionary of quetions
- Optional URL Arguments: Page's number
- Required Data Arguments: None
- Returns: Json data about categories and questions
- Success Response:
                    ```
                        {
                        "categories": {
                        "1": "Science",
                        "2": "Art",
                        "3": "Geography",
                        "4": "History",
                        "5": "Entertainment",
                        "6": "Sports"
                        },
                        "current_category": [
                            2,
                            3,
                            4,
                            5,
                            6
                        ],
                        "questions": [
                            {
                            "answer": "Maya Angelou",
                            "category": 4,
                            "difficulty": 2,
                            "id": 5,
                            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
                            }
                        ],
                        "status_code": 200,
                        "status_message": "OK",
                        "success": true,
                        "total_questions": 1
                        }
                    ```

#### `DELETE '/questions/<int:question_id>'`
- Deletes the `question_id` of question 
- Required URL Arguments: `question_id: id=[question_id_integer]` 
- Required Data Arguments: None
- Returns: Json data about the deleted quetion's ID 
- Success Response:
                    ```
                    {
                    "deleted": 6,
                    "status_code": 200,
                    "status_message": "OK",
                    "success": true
                    }
                    ```

#### `POST '/questions'`
- Post a new question in a database.
- Required URL Arguments: None 
- Required Data Arguments:  Json data                
                            ```
                            {
                            "question": "question field"
                            "answer": "answer field"
                            "category": "category ID field"
                            "difficulty": "level of difficulty field"
                            }
                            ```
- Returns: Json data about if a quesion is posted successfully 
- Success Response:
                    ```
                    {
                    "status_code": 200,
                    "status_message": "OK",
                    "success": true
                    }
                    ```

#### `POST '/searchterms'`
- Fetches questions filtered by specified search term.
- Required URL Arguments: None
- Optional URL Arguments: Page's number
- Required DATA Arguments:  Jason data `{"searchTerm": "searchTerm"}`
- Returns: Jason data of questions filtered by specified search term.
- Success Response:
                    ```
                    {
                    "total_questions": 2
                    "current_category": [
                        3,
                        4
                    ],
                    "questions": [
                        {
                        "answer": "Muhammad Ali",
                        "category": 4,
                        "difficulty": 1,
                        "id": 9,
                        "question": "What boxer's original name is Cassius Clay?"
                        },
                        {
                        "answer": "Lake Victoria",
                        "category": 3,
                        "difficulty": 2,
                        "id": 13,
                        "question": "What is the largest lake in Africa?"
                        }
                    "status_code": 200,
                    "status_message": "OK",
                    "success": true,
                    }
                    ```
#### `GET '/categories/<int:category_id>/questions'`
- Fetches questions filtered by specified category.
- Required URL Arguments: `category_id: id=[category_id_integer]`
- Optional URL Arguments: Page's number
- Required Data Arguments: None
- Returns: Jason data about questions filtered by the ID of category
- Success Response:
                    ```
                    {
                    "current_category": [
                        1
                    ],
                    "questions": [
                        {
                        "answer": "The Liver",
                        "category": 1,
                        "difficulty": 4,
                        "id": 20,
                        "question": "What is the heaviest organ in the human body?"
                        }
                    ],
                    "status_code": 200,
                    "status_message": "OK",
                    "success": true,
                    "total_questions": 1
                    }
                    ```

#### `POST '/quizzes'`
- Fetches a random question from a specified category that is not one of the previous questions.
- Required URL Arguments: None
- Required Data Arguments: Jason
                          ```
                            {
                              "previous_questions": ["ID of previous question"], 
                              "quiz_category": {"type": "Category type field", "id": "ID number field"}
                              }
                          ```
- Returns: Jason data about the question from a specified category that is not one of the    previous 
- Success Response:
                    ```  
                    {"question": {
                        "answer": "Alexander Fleming",
                        "category": 1,
                        "difficulty": 3,
                        "id": 21,
                        "question": "Who discovered penicillin?"
                    },
                    "status_code": 200,
                    "status_message": "OK",
                    "success": true
                    }
                    ```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```