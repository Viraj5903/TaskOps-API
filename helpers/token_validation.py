# Import the necessary modules.

import jwt # Import the jwt module. # pip install pyjwt
from flask import request # Import Flask modules
import app_config as config 

# Function to valid the token and exact and return the user information from the token.
def validate_jwt():
    """
    Function to validate the token and extract and return the user information from the token.
    
    This function checks if the token is present in the request headers. If the token is missing it returns 400. If the token is invalid, it returns 401. If the token is expired, it returns 401.
    
    Returns:
        The user information extracted from the token if the token is valid.
        Otherwise, returns 400, 401, or None.
    """
    
    # Initialize variables
    token = None
    user_information = None
    
    try:
        
        # Check if the token is present in the request headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        # If the token is missing, return 400
        if not token:
            return 400 
        
        try:
            # Decode the token and extract the user information
            user_information = jwt.decode(token, config.TOKEN_SECRET, algorithms = ["HS256"])
        except Exception:
            # If the token is invalid, return 401
            return 401
        
        # Return the user information
        return user_information

    except jwt.ExpiredSignatureError:
        # If the token is expired, return 401
        return 401
    except:
        # If there is an error, return 400
        return 400
