from models.user_model import User
from database.__init__ import conn
import app_config as config
import bcrypt # pip install bcrypt
from datetime import datetime, timedelta
import jwt # pip install pyjwt

def generate_hash_password(password):
    """
    Generate a hashed password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    # Generate a salt for hashing the password
    salt = bcrypt.gensalt()

    # Hash the password using the generated salt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    # Return the hashed password
    return hashed_password

def create_user(user_information):
    """
    Create a new user in the database.

    Args:
        user_information (dict): A dictionary containing user information.
            Required keys:
                - 'name': The name of the user.
                - 'email': The email of the user.
                - 'password': The password of the user.

    Returns:
        pymongo.results.InsertOneResult: The result of the insert operation.

    Raises:
        ValueError: If there is an error creating the user.
    """
    try:
        # Create a new User object
        new_user = User()

        # Set the user's name, email, and hashed password
        new_user.name = user_information["name"]
        new_user.email = user_information["email"]
        new_user.password = generate_hash_password(user_information["password"])

        # Connect to the user collection of the database
        db_collection = conn.database[config.CONST_USER_COLLECTION]

        # Check if a user with the same email already exists
        if db_collection.find_one({'email': new_user.email}):
            return 'Duplicated User'

        # Insert the new user into the database
        created_user = db_collection.insert_one(new_user.__dict__)

        # Return the result of the insert operation
        return created_user

    except Exception as err:
        # If there is an error creating the user, raise a ValueError
        raise ValueError("Error on creating user.", err)

def login_user(user_information):
    """
    Handles the user login process by checking the provided credentials against the database.

    Args:
        user_information (dict): A dictionary containing user information.
            Required keys:
                - 'email': The email of the user.
                - 'password': The password of the user.

    Returns:
        dict: A dictionary containing the JWT token, expiration time, and logged user information.
    """
    try:
        # Extract user information from the request
        email = user_information["email"]
        password = user_information["password"].encode('utf-8')

        # Connect to the user collection of the database
        db_collection = conn.database[config.CONST_USER_COLLECTION]

        # Find the user with the provided email
        current_user = db_collection.find_one({'email': email})

        # Check if the user exists
        if not current_user:
            return "Invalid Email"
        
        # Check if the provided password matches the hashed password in the database
        if not bcrypt.checkpw(password, current_user["password"]):
            return "Invalid Password"
        
        # Create a dictionary with the logged user information
        logged_user = {}
        logged_user['id'] = str(current_user['_id'])
        logged_user['email'] = current_user['email']
        logged_user['name'] = current_user['name']

        # Calculate the expiration time for the JWT token
        expiration = datetime.utcnow() + timedelta(seconds = config.JWT_EXPIRATION)

        # Create the JWT token data
        jwt_data = {'email': logged_user['email'], 'id': logged_user['id'], 'exp': expiration}

        # Encode the JWT token with the secret key
        jwt_to_return = jwt.encode(payload=jwt_data, key=config.TOKEN_SECRET)

        # Return the JWT token, expiration time, and logged user information
        return {'token': jwt_to_return, 'expiration': config.JWT_EXPIRATION, 'logged_user': logged_user}
    
    except Exception as err:
        # If there is an error logging in the user, raise a ValueError with the error message
        raise ValueError("Error on trying to login.", err)


def fetch_all_users():
    """
    Fetches all users from the database and returns them as a list of dictionaries.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing the users. Each dictionary contains the user's ID, email, and name.

    Raises:
        ValueError: If there is an error fetching the users.
    """
    try:
        # Connect to the user collection of the database
        db_collection = conn.database[config.CONST_USER_COLLECTION]
        users = []

        # Iterate over each user in the database, create a dictionary with their ID, email, and name,
        # and add it to the list of users
        for user in db_collection.find():
            current_user = {}
            current_user["id"] = str(user["_id"])
            current_user["email"] = user["email"]
            current_user["name"] = user["name"]
            users.append(current_user)
        
        # Return the fetch users.
        return users
    
    except Exception as err:
        # If there is an error fetching the users, raise a ValueError with the error message
        raise ValueError("Error on trying to fetch users.", err)
