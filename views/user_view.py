from flask import Blueprint, jsonify, request
import json
from controllers.user_controller import create_user, login_user, fetch_all_users
from helpers.token_validation import validate_jwt

user = Blueprint("user", __name__)

@user.route("/users/", methods=["POST"])
def create():
    try:
        data = json.loads(request.data)

        if 'email' not in data:
            return jsonify({'error': 'Email is needed in the request.'}), 400
        if 'password' not in data:
            return jsonify({'error': 'Password is needed in the request.'}), 400
        if 'name' not in data:
            return jsonify({'error': 'Name is needed in the request.'}), 400

        created_user = create_user(data)

        if created_user == "Duplicated User":
            return jsonify({'error': 'There is already an user with this email.'}), 400

        return jsonify({'id': str(created_user.inserted_id)})
    except ValueError:
        return jsonify({'error': 'Error on creating user.'}), 500

@user.route("/users/login", methods=["POST"])
def login():
    try:
        data = json.loads(request.data)

        if 'email' not in data:
            return jsonify({'error': 'Email is needed in the request.'}), 400
        if 'password' not in data:
            return jsonify({'error': 'Password is needed in the request.'}), 400

        login_attempt = login_user(data)

        if login_attempt == "Invalid Email":
            return jsonify({'error': 'Email not found.'}), 401
        if login_attempt == "Invalid Password":
            return jsonify({'error': 'Invalid Password.'}), 401

        return jsonify({'token': login_attempt['token'], "expiration": login_attempt['expiration'], "logged_user":  login_attempt["logged_user"]})
    except ValueError:
        return jsonify({'error': 'Error login user.'}), 500


@user.route("/users/", methods=["GET"])
def fetch():
    try:
        token = validate_jwt()

        if token == 400:
            return jsonify({'error': 'Token is missing in the request.'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token.'}), 401

        users = fetch_all_users()

        return jsonify({'users': users, 'request_made_by': token})

    except ValueError:
        return jsonify({'error': 'Error fetching users.'}), 500