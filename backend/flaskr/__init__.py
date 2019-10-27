import os
from flask import ( Flask, 
                    request, 
                    abort, 
                    jsonify)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import (setup_db, 
                    Question, 
                    Category
                    )

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response
  
  # questions paginator
  def paginate_questions(request, selection):
    
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

  '''
  \*@TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  # get categories
  @app.route('/categories')
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    # no category found/left
    if len(categories) == 0:
        abort(404)
    Category.close()
    return jsonify({
        "success": True,
        "status_code": 200,
        "status_message": 'OK',
        "categories": {category.id : category.type for category in categories},
        "total_categories": len(categories)
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  # get questions and categories
  @app.route('/questions')
  def get_questions():
   
    questions = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, questions)
    categories = Category.query.order_by(Category.id).all()
  
    # no questions found/left
    if len(current_questions) == 0:
      abort(404)

    Question.close()
    return jsonify({
      "success": True,
      "status_code": 200,
      "status_message": 'OK',
      "questions": current_questions,
      "total_questions": len(questions),
      "current_category": list(set([question['category'] for question in current_questions])),  
      "categories": {category.id : category.type for category in categories}
      })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    
    question = Question.query.filter(Question.id == question_id).one_or_none()

    # no question found/left
    if question is None:
      abort(404)
    else:
      question.delete() 
      Question.close()
      return jsonify({
            "success": True,
            "status_code": 200,
            "status_message": 'OK',
            "deleted": question_id
        })
   
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  #post question with form validator

  @app.route('/questions', methods=['POST'])
  def post_question():
    # retrieve form data
    question = request.get_json().get('question')
    answer = request.get_json().get('answer','')
    difficulty = request.get_json().get('difficulty')
    category = request.get_json().get('category')
    
    # empty from raise 422
    if (question.strip() == "" or 
        answer.strip() == "" or 
        difficulty.strip() == "" or 
        category.strip() == ""): 
      abort(422)

    new_question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
    new_question.insert()
    
    Question.close()
    return jsonify({
          "success": True,
          "status_code": 200,
          "status_message": 'OK',
      })
  

   
      


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  # retur paginated questions filtered by search term
  @app.route('/searchterms', methods=['POST'])
  def search_questions_by_searchterm():
   
    searchterm = request.get_json().get('searchTerm')
    filtered_questions = Question.query.filter(
                                          Question.question.ilike('%{}%'.format(searchterm))
                                        ).order_by(Question.id).all()
    current_questions = paginate_questions(request,filtered_questions)

  # no question found/left 
    if len(current_questions) == 0:
      abort(404) 
    Question.close()
    return jsonify({
        "success": True,
        "status_code": 200,
        "status_message": 'OK',
        "questions": current_questions,
        "total_questions": len(filtered_questions),
        "current_category": list(set([question['category'] for question in current_questions])),  
      }) 

   

  

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  # retur paginated questions filtered by category specified
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def search_questions_by_categories(category_id):
  
    filtered_questions = Question.query.filter(
                                          Question.category == category_id
                                        ).order_by(Question.id).all()
    current_questions = paginate_questions(request,filtered_questions)

    # no question found/left
    if len(current_questions) == 0:
      abort(404)  
    
    Question.close()

    return jsonify({
        "success": True,
        "status_code": 200,
        "status_message": 'OK',
        "questions": current_questions,
        "total_questions": len(filtered_questions),
        "current_category": list(set([question['category'] for question in current_questions])),  
      }) 

    


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  # return a radom question from category specified and not one of the previous questions
  @app.route('/quizzes', methods=['POST'])
  def pick_random_question():
    previous_questions = request.get_json().get('previous_questions')
    quiz_category = request.get_json().get('quiz_category')
    
    # all or specified category 
    if quiz_category.get('id') == 0:  
      questions = Question.query.order_by(Question.id).all() 
    else: 
      questions = Question.query.filter( Question.category == quiz_category.get('id')
                                          ).order_by(Question.id).all() 
    # questions left
    question_left = []
    for question in questions:
      if question.id not in previous_questions:
        question_left.append(question.format()) 
          
    # if no question left    
    if len(question_left) == 0:
      abort(404)

    Question.close()

    return jsonify({
        "success": True,
        "status_code": 200,
        "status_message": 'OK',
        "question": random.choice(question_left),  
      }) 

    

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Resource Not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable_entity(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable Entity"
      }), 422

  @app.errorhandler(500)
  def internal_error(error):
      return jsonify({
          "success": False,
          "error": 500,
          "message": "Internal Server Error"
      }), 500


  return app

    