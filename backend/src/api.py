import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/*": {"origins": "*"}})

db_drop_and_create_all()


# ROUTES


@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in drinks]
    })


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_detail(jwt):
    drinks = Drink.query.all()

    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in drinks]
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(jwt):
    data = request.get_json()
    if 'title' and 'recipe' not in data:
        abort(422)

    title = data.get('title')
    recipe = json.dumps(data.get('recipe'))
    new_drink = Drink()
    try:
        new_drink = Drink(title=title, recipe=recipe)
        new_drink.insert()
    except Exception:
        abort(400)

    return jsonify({
        'success': True,
        'drinks': [new_drink.long()]
    })


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    drink = Drink.query.get(id)

    if drink is None:
        abort(404)

    data = request.get_json()
    if 'title' in data:
        drink.title = data.get('title')

    if 'recipe' in data:
        drink.recipe = data.get('recipe')
    try:
        drink.update()
    except Exception:
        db.session.rollback()
        abort(422)

    return jsonify({
        'success': True,
        'drink': [drink.long()]
    })


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    drink = Drink.query.get(id)

    if drink is None:
        abort(404)

    try:
        drink.delete()
    except Exception:
        db.session.rollback()
        abort(422)

    return jsonify({
        'success': True,
        'delete': [drink.id]
    })


# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
    }), 422


@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method is not allowed"
    }), 405


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
    }), 400


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
    }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
