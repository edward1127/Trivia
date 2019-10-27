import os
import unittest
import json
import random
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
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','e2806387','localhost:5432', self.database_name)
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
    # test get categories function
    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_categories'])

    # test get questions function
    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(data['categories']) 

    # test get question function when a page contains nothing
    def test_get_questions_404(self):
        response = self.client().get('/questions?page=999')
        data = json.loads(response.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'Resource Not found') 

    # test delete question function
    def test_delete_question(self):
        random_id = random.choice([question.id for question in Question.query.all()])
        response = self.client().delete('questions/{}'.format(random_id))
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')
        self.assertTrue(data['deleted'])

    # test delete question function when question doesn't exist
    def test_delete_question_404(self):
        response = self.client().delete('questions/999')
        data = json.loads(response.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'Resource Not found')

    # test post question function 
    def test_post_question(self):
        new_question = {
            'question': 'test',
            'answer': 'answer',
            'category': '1',
            'difficulty': '1'
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')

    # test post question function when a form field is empty
    def test_post_question_422(self):
        new_question = {
            'question': '',
            'answer': '',
            'category': '',
            'difficulty': ''
        }
        response = self.client().post('/questions', json=new_question)
        data = json.loads(response.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 422)
        self.assertTrue(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    # test search by searchterm function
    def test_search_questions_by_searchterm(self):
        response = self.client().post('/searchterms',
                                      json={'searchTerm': "wh"})

        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    # test search by searchterm function when no result found 
    def test_search_questions_by_searchterm_404(self):
        response = self.client().post('/searchterms',
                                      json={'searchTerm': "ThisTermCan'tNotBeMatched"})

        data = json.loads(response.data)


        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'Resource Not found')

    # test search by category function
    def test_search_questions_by_categories(self):
        response = self.client().get('/categories/1/questions')

        data = json.loads(response.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status_message'], 'OK')
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    # test search by category function when no result found 
    def test_pick_random_question(self):
        response = self.client().post('/categories/9/questions')

        data = json.loads(response.data)


        self.assertEqual(data['success'], False)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'Resource Not found')


    # test pick random question function 
    def test_pick_random_question(self):

        response = self.client().post('/quizzes',
                                      json={'previous_questions': [],
                                            'quiz_category': {'type': 'Science',  
                                                              'id': '1'
                                                              }
                                            })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_message'], 'OK')
        self.assertTrue(data['question'])

    # test pick random question function when no question left 
    def test_pick_random_question_404(self):
 
        response = self.client().post('/quizzes',
                                      json={'previous_questions': [n for n in range(100)],
                                            'quiz_category': {'type': 'Science',
                                                              'id': '1'
                                                              }
                                            })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not found')


    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()