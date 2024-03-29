from flask import Blueprint, jsonify, request
import json
from helpers.token_validation import validate_jwt
from controllers.task_controller import create_task

# task = Blueprint("task", __name__, url_prefix="/tasks/")
task = Blueprint("task", __name__)

# TODO: Manpreet Kaur. Create task route.

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