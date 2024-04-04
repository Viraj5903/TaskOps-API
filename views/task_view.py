from flask import Blueprint, jsonify, request
import json
from helpers.token_validation import validate_jwt
from controllers.task_controller import create_task, get_tasks_assigned_to_user, get_task_created_by_user, update_task, delete_task

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
# Define the route for getting tasks assigned to the user
@task.route("/tasks/assignedto/", methods=["GET"])
def get_tasks_assigned_to_current_user():
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
        return jsonify({'error': str(err)}), 500

# TODO: Payal Rangra. Update task route.
@task.route("/tasks/<taskUid>", methods=["PATCH"])
def updatetask(taskUid):
    try:    
        # Validating the user.
        token = validate_jwt() 

        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401
        if token == 401:
           return jsonify({"error": 'Invalid authentication token, please login again'}), 403
        
        
        
        data = json.loads(request.data)
        if  "done" not in data:
            return jsonify({"error": 'Status done not found in the request'}), 400
       
        result = update_task(token, taskUid, data["done"])
        
        if result=="No such task exists." :
            return jsonify({"Error":"Task does not exist"}), 404
        
        return  jsonify({"taskUid":taskUid}) , 200

    except ValueError as error:
        return jsonify({'error': f'Error on updating  the task. {error}'}), 500
    except Exception as error:
        return jsonify({'error': error}), 500
    
# TODO: Viraj Patel. Delete task route.
@task.route("/tasks/<taskUid>", methods=["DELETE"])
def deleteTask(taskUid):
    try:
        
        # print(taskUid)
        # print(type(taskUid))
                
        # Validating the user.
        token = validate_jwt()

        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401
        if token == 401:
           return jsonify({"error": 'Invalid authentication token, please login again'}), 403
        
        # Checking whether the taskUid length is equal to 24 or not.
        if len(taskUid) != 24:
            return jsonify({"error": f"Not task found with task_id = {taskUid}. It length must be equal to 24 characters."}), 404
        
        # Printing the user_information which we extract from the token.
        # print("Token = ", token)
        
        # user_information = token
        
        # Calling the delete_task function of the controller function with arguments user_information as token and task_id as taskUid.
        deleted_result = delete_task(token, taskUid)
        
        # Return the number of documents deleted from the task collection of the database.
        return jsonify({'tasksAffected': deleted_result.deleted_count}), 200
        
    except ValueError as error:
        return jsonify({'error': f'Error on deleting task. Error = {error}'}), 500
    except Exception as error:
        return jsonify({'error': error}), 500
