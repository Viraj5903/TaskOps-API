# Import the necessary modules.

from flask import Blueprint, jsonify, request  # Import Flask modules
import json  # Import JSON module

from helpers.token_validation import validate_jwt # Import module for token validation
from controllers.user_controller import ( # Import controller functions for task related operations
     # Import controller functions for user creation
    create_user,
    # Import controller functions for user login
    login_user,
    # Import controller functions for fetching all users
    fetch_all_users
)

user = Blueprint("user", __name__)
"""
Blueprint for user related views.

This blueprint handles the following routes:
- POST /users/: Creates a new user.
- GET /users/: Fetches all users.
- POST /users/login/: Logs in a user.

"""

@user.route("/users/", methods=["POST"])
def create():
    """
    Create a new user.

    This function handles the HTTP POST request to create a new user.
    It expects the request data to contain the following keys:
    - 'email': The email of the user.
    - 'password': The password of the user.
    - 'name': The name of the user.

    If any of the required keys are missing from the request data,
    it returns a JSON response with an error message and a HTTP status code of 400.

    If the user already exists, it returns a JSON response with an error message and a HTTP status code of 400.

    If the user is successfully created, it returns a JSON response with the ID of the created user and a HTTP status code of 200.

    If there is a ValueError during the execution of the function, it returns a JSON response with an error message and a HTTP status code of 500.

    Returns:
        A JSON response with the ID of the created user and a HTTP status code of 200, or a JSON response with an error message and a HTTP status code of 400 or 500.
    """
    try:
        # Load the request data
        data = json.loads(request.data)

        # Check if the required keys are in the request data
        if 'email' not in data:
            return jsonify({'error': 'Email is needed in the request.'}), 400
        if 'password' not in data:
            return jsonify({'error': 'Password is needed in the request.'}), 400
        if 'name' not in data:
            return jsonify({'error': 'Name is needed in the request.'}), 400

        # Create the user
        created_user = create_user(data)

        # Check if the user already exists
        if created_user == "Duplicated User":
            return jsonify({'error': 'There is already an user with this email.'}), 400

        # Return the ID of the created user
        return jsonify({'id': str(created_user.inserted_id)})
    except ValueError:
        # Return an error message if there was an issue creating the user
        return jsonify({'error': 'Error on creating user.'}), 500

@user.route("/users/login", methods=["POST"])
def login():
    """
    Handle the HTTP POST request to login a user.

    This function expects the request data to contain the 'email' and 'password' keys.
    It returns a JSON response with the JWT token, expiration time, and logged user information.

    Returns:
        A JSON response with the JWT token, expiration time, and logged user information.
    """
    try:
        # Load the request data
        data = json.loads(request.data)

        # Check if the required keys are in the request data
        if 'email' not in data:
            return jsonify({'error': 'Email is needed in the request.'}), 400
        if 'password' not in data:
            return jsonify({'error': 'Password is needed in the request.'}), 400

        # Attempt to login the user
        login_attempt = login_user(data)

        # Check the result of the login attempt
        if login_attempt == "Invalid Email":
            return jsonify({'error': 'Email not found.'}), 401
        if login_attempt == "Invalid Password":
            return jsonify({'error': 'Invalid Password.'}), 401

        # Return the login details
        return jsonify(login_attempt)
    except ValueError:
        # Return an error message if there was an issue logging in the user
        return jsonify({'error': 'Error login user.'}), 500


@user.route("/users/", methods=["GET"])
def fetch():
    """
    Handle the HTTP GET request to fetch all users.

    This function expects the JWT token in the request header.
    If the token is missing or invalid, it returns a JSON response with an error message and the appropriate HTTP status code.

    It returns a JSON response with all the users and the user information from the token.

    Returns:
        A JSON response with all the users and the user information from the token,
        or a JSON response with an error message and a HTTP status code of 400 or 401.
    """
    try:
        # Validate the JWT token
        token = validate_jwt()

        if token == 400:
            # Return an error message if the token is missing in the request
            return jsonify({'error': 'Token is missing in the request.'}), 400
        if token == 401:
            # Return an error message if the token is invalid
            return jsonify({'error': 'Invalid authentication token.'}), 401

        # Fetch all the users
        users = fetch_all_users()

        # Return the users along with the user information from the token
        return jsonify({'users': users, 'request_made_by': token})

    except ValueError:
        # Return an error message if there was an issue fetching the users
        return jsonify({'error': 'Error fetching users.'}), 500
