import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def get_current_questions(request, search_term = None, category_id = None):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  if (search_term != None):
    questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).order_by(Question.id).limit(QUESTIONS_PER_PAGE).offset(start)
  elif (category_id != None):
     questions = Question.query.filter_by(category = category_id).limit(QUESTIONS_PER_PAGE).offset(start)
  else:
    questions = Question.query.order_by(Question.id).limit(QUESTIONS_PER_PAGE).offset(start)
  
  current_questions = [question.format() for question in questions]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  CORS(app, resources={'/': {'origins': '*'}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
    return response

  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    categories_arr = {}

    for category in categories:
      categories_arr[category.id] = category.type

    if (len(categories_arr) == 0):
      abort(404)

    return jsonify({
      'success': True,
      'categories': categories_arr
    })

  @app.route('/questions')
  def get_questions():
    questions = get_current_questions(request)
    '''@TODO: search for a better way to get rows count'''
    total_questions = len(Question.query.all())

    categories = Category.query.all()
    categories_arr = {}
    for category in categories:
      categories_arr[category.id] = category.type

    if (len(questions) == 0):
      abort(404)

    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': total_questions,
      'categories': categories_arr
    })

  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      question = Question.query.filter(Question.id == id).one_or_none()

      if question is None:
        abort(404)

      question.delete()

      return jsonify({
        'success': True,
        'deleted': id
      })

    except:
      abort(422)

  @app.route('/questions', methods=['POST'])
  def post_question():
    body = request.get_json()

    if (body.get('searchTerm')):
      search_term = body.get('searchTerm')
      questions = get_current_questions(request, search_term)

      if (len(questions) == 0):
        abort(404)

      return jsonify({
        'success': True,
        'questions': questions,
        'total_questions': len(Question.query.all())
      })
    
    else:
      new_question = body.get('question')
      new_answer = body.get('answer')
      new_difficulty = body.get('difficulty')
      new_category = body.get('category')

      if ((new_question is None) or (new_answer is None) or (new_difficulty is None) or (new_category is None)):
        abort(422)

      try:
        question = Question(question = new_question, answer = new_answer, difficulty = new_difficulty, category = new_category)
        question.insert()

        current_questions = get_current_questions(request)

        return jsonify({
          'success': True,
          'created': question.id,
          'question_created': question.question,
          'questions': current_questions,
          'total_questions': len(Question.query.all())
        })

      except:
        abort(422)

  '''
  @TODO: 
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category(id):
    category = Category.query.filter(Category.id == id).one_or_none()

    if (category is None):
      abort(400)

    category_id = category.id
    questions = get_current_questions(request, None, category_id)

    return jsonify({
      'success': True,
      'questions': questions,
      'total_questions': len(Question.query.all()),
      'current_category': category.type
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
      "message": "Not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad request"
    }), 400
  
  return app

    