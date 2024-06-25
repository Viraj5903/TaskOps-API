# Import the necessary modules.

from flask import Blueprint, jsonify, request  # Import Flask modules
import json  # Import JSON module

from helpers.token_validation import validate_jwt  # Import module for token validation
from controllers.task_controller import (  # Import controller functions for task related operations
    # Import controller functions for task creation
    create_task,
    # Import controller functions for getting tasks assigned to a user
    get_tasks_assigned_to_user,
    # Import controller functions for getting tasks created by a user
    get_task_created_by_user,
    # Import controller functions for updating tasks
    update_task,
    # Import controller functions for deleting tasks
    delete_task
)

# task = Blueprint("task", __name__, url_prefix="/tasks/")

task = Blueprint("task", __name__)
"""
Blueprint for task related views.

This blueprint handles the following routes:
- POST /tasks/: Creates a new task.
- GET /tasks/: Returns all tasks assigned to a specific user.
- GET /tasks/user/: Returns all tasks created by a specific user.
- PUT /tasks/: Updates a task.
- DELETE /tasks/: Deletes a task.

"""

# Create task route.
@task.route("/tasks/", methods=["POST"])
def createTask():
    """
    Create a new task.

    This function handles the HTTP POST request to create a new task. It expects the request data to contain the following keys:
    - 'description': The description of the task.
    - 'assignedToUid': The ID of the user to whom the task is assigned.

    If the JWT token is missing or invalid, it returns a JSON response with an error message and the appropriate HTTP status code.

    If the required keys are missing from the request data, it raises a ValueError with an error message.

    The function extracts the necessary information from the request data, creates a dictionary with the task information, and calls the create_task_controller function with the task information.

    If the task is successfully created, it returns a JSON response with the ID of the created task and a HTTP status code of 200.

    If there is a ValueError during the execution of the function, it returns a JSON response with the error message and a HTTP status code of 400.

    Returns:
        A JSON response with the ID of the created task and a HTTP status code of 200, or a JSON response with an error message and a HTTP status code of 400 or 401.
    """
    
    try:
        # Validate JWT token
        user_info = validate_jwt()
        
        if user_info == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401
        elif user_info == 401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403
        
        # Checking if required keys are in the request data
        data = request.json
        if 'description' not in data or 'assignedToUid' not in data:
            raise ValueError('Error validating information')
        
        # Extracting the information from request data
        description = data['description']
        assigned_to_uid = data['assignedToUid']
        created_by_uid = user_info['id']  # Extract user ID from token
        
        # Create a dictionary with task information
        task_info = {'description': description, 'assigned_to_uid': assigned_to_uid, 'created_by_uid': created_by_uid}
        
        # Call the create_task_controller function with task_info
        created_task = create_task(task_info)
        
        # Return the ID of the created task
        return jsonify({'id': str(created_task.inserted_id)}), 200
    
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


# Get tasks created by the user route.
@task.route("/tasks/createdby/", methods=["GET"])
def search_created_by():
    """
    Get tasks created by the user.

    This function handles the HTTP GET request to retrieve tasks created by the user.
    It expects the JWT token in the request header. If the token is missing or invalid, it returns a JSON response with an error message and the appropriate HTTP status code.

    If the user's tasks are successfully fetched, it returns a JSON response with the tasks and a HTTP status code of 200.

    If there is a ValueError during the execution of the function, it returns a JSON response with the error message and a HTTP status code of 400.

    Returns:
        A JSON response with the tasks and a HTTP status code of 200, or a JSON response with an error message and a HTTP status code of 400 or 401.
    """
    try:
        # Validate the JWT token
        token = validate_jwt()

        if token == 400:
            return jsonify({"error": 'Token is missing in the request.'}), 401
        if token == 401:
            return jsonify({"error": 'Invalid authentication token.'}), 403

        user_id = token['id']

        # Fetch tasks created by the user
        tasks = get_task_created_by_user(user_id=user_id)

        return jsonify(tasks)
    except ValueError as err:
        return jsonify({"error": str(err)}), 400
    except Exception as error:
        return jsonify({'error' : error}), 500

# Get tasks assigned to the user route.
# Define the route for getting tasks assigned to the user
@task.route("/tasks/assignedto/", methods=["GET"])
def get_tasks_assigned_to_current_user():
    """
    Get tasks assigned to the current user.

    This function handles the HTTP GET request to retrieve tasks assigned to the current user.
    It expects the JWT token in the request header. If the token is missing or invalid, it returns a JSON response with an error message and the appropriate HTTP status code.

    If the user's tasks are successfully fetched, it returns a JSON response with the tasks and a HTTP status code of 200.

    If there is a ValueError during the execution of the function, it returns a JSON response with the error message and a HTTP status code of 400.

    Returns:
        A JSON response with the tasks and a HTTP status code of 200, or a JSON response with an error message and a HTTP status code of 400 or 401.
    """
    try:
        # Validate the JWT token
        token = validate_jwt()

        if token == 400:
            return jsonify({"error": 'Token is missing in the request.'}), 401
        if token == 401:
            return jsonify({"error": 'Invalid authentication token.'}), 403

        # Retrieve assignedToUid from the token
        assignedToUid = token['id']

        # Fetch tasks assigned to the user
        tasks = get_tasks_assigned_to_user(assignedToUid)

        return jsonify({'tasks': tasks})

    except ValueError as err:
        return jsonify({"error": str(err)}), 400

# Update task route.
@task.route("/tasks/<taskUid>", methods=["PATCH"])
def updateTask(taskUid):
    """
    Update a task.

    This function handles the HTTP PATCH request to update a task. It expects the JWT token in the request header.
    If the token is missing or invalid, it returns a JSON response with an error message and the appropriate HTTP status code.

    It expects the request data to contain the 'done' key with a boolean value.

    If the task is successfully updated, it returns a JSON response with the task UID and a HTTP status code of 200.

    If there is a ValueError during the execution of the function, it returns a JSON response with the error message and a HTTP status code of 400.

    Returns:
        A JSON response with the task UID and a HTTP status code of 200, or a JSON response with an error message and a HTTP status code of 400 or 401.
    """
    try:    
        # Validate the JWT token
        token = validate_jwt() 

        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401
        if token == 401:
           return jsonify({"error": 'Invalid authentication token, please login again'}), 403
        
        # Load the request data
        data = json.loads(request.data)

        # Check if the 'done' key is present in the request data
        if  "done" not in data:
            return jsonify({"error": 'Status done not found in the request'}), 400
       
        # Call the update_task function of the controller function with arguments token as user_information, taskUid as task_id, and data["done"] as done.
        result = update_task(token, taskUid, data["done"])
        
        # Return the task UID in a JSON response with a HTTP status code of 200.
        return  jsonify({"taskUid":taskUid}) , 200

    except ValueError as error:
        # Return a JSON response with the error message and a HTTP status code of 400.
        return jsonify({'error': str(error)}), 400
    except Exception as error:
        # Return a JSON response with the error message and a HTTP status code of 500.
        return jsonify({'error': error}), 500
    
# Delete task route.
@task.route("/tasks/<taskUid>", methods=["DELETE"])
def deleteTask(taskUid):
    """
    Delete a task.

    This function handles the HTTP DELETE request to delete a task. It expects the JWT token in the request header.
    If the token is missing or invalid, it returns a JSON response with an error message and the appropriate HTTP status code.

    If the task is successfully deleted, it returns a JSON response with the number of documents deleted from the task collection of the database and a HTTP status code of 200.

    If there is a ValueError during the execution of the function, it returns a JSON response with the error message and a HTTP status code of 400.

    Returns:
        A JSON response with the number of documents deleted from the task collection of the database and a HTTP status code of 200, or a JSON response with an error message and a HTTP status code of 400 or 401.
    """
    try:
        # Validate the JWT token
        token = validate_jwt()

        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401
        if token == 401:
           return jsonify({"error": 'Invalid authentication token, please login again'}), 403
        
        # Call the delete_task function of the controller function with arguments token as user_information and taskUid as task_id.
        deleted_result = delete_task(user_information = token, task_id = taskUid)
        
        # Return the number of documents deleted from the task collection of the database.
        return jsonify({'tasksAffected': deleted_result.deleted_count}), 200
        
    except ValueError as error:
        # Return a JSON response with the error message and a HTTP status code of 400.
        return jsonify({'error': str(error)}), 400
    except Exception as error:
        # Return a JSON response with the error message and a HTTP status code of 500.
        return jsonify({'error': error}), 500
