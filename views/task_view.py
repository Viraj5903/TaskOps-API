from flask import Blueprint, jsonify, request
import json
from helpers.token_validation import validate_jwt
from controllers.task_controller import create_task

# task = Blueprint("task", __name__, url_prefix="/tasks/")
task = Blueprint("task", __name__)

# TODO: Manpreet Kaur. Create task route.
@task.route("/tasks/", methods=["POST"])
def createTask():
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
        return jsonify({'id': str(created_task.inserted_id)})
    
    except ValueError as err:
        return jsonify({"error": str(err)}), 400


# TODO: Dil Raval. Get tasks created by the user route.

# TODO: Aryan Handa. Get tasks assigned to the user route.

# TODO: Payal Rangra. Update task route.

# TODO: Viraj Patel. Delete task route.
@task.route("/tasks/<taskUid>", methods=["DELETE"])
def deleteTask(taskUid):
    try:
        
        # Validating the user.
        token = validate_jwt()

        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401
        if token == 401:
           return jsonify({"error": 'Invalid authentication token, please login again'}), 403
        
        user_information = token

    except ValueError:
        return jsonify({'error': 'Error creating task.'}), 500
    except Exception as error:
        return jsonify({'error': error}), 500