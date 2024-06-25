# Import the necessary modules.

from models.task_model import Task
from database.__init__ import conn
from bson.objectid import ObjectId
import app_config as config

def create_task(task_info):
    """
    Create a new task in the database.

    Args:
        task_info (dict): A dictionary containing the task information.
            Required keys:
                - 'created_by_uid': The ID of the user who created the task.
                - 'assigned_to_uid': The ID of the user to whom the task is assigned.
                - 'description': The description of the task.

    Returns:
        pymongo.results.InsertOneResult: The result of the insert operation.

    Raises:
        ValueError: If the user information is invalid.
    """
    try:
        # Find the users by their IDs
        created_by_user = conn.database[config.CONST_USER_COLLECTION].find_one(
            {'_id': ObjectId(task_info['created_by_uid'])})
        assigned_to_user = conn.database[config.CONST_USER_COLLECTION].find_one(
            {'_id': ObjectId(task_info['assigned_to_uid'])})
        
        # Check if the user information is valid
        if not created_by_user or not assigned_to_user:
            raise ValueError('Invalid user information')
        
        # Create a new task object
        new_task = Task()
        new_task.createdByUid = task_info['created_by_uid']  # Set the created by user ID
        new_task.createdByName = created_by_user['name']  # Set the created by user name
        new_task.assignedToUid = task_info['assigned_to_uid']  # Set the assigned to user ID
        new_task.assignedToName = assigned_to_user['name']  # Set the assigned to user name
        new_task.description = task_info['description']  # Set the description of the task
        
        # Save the task to the database
        created_task = conn.database[config.CONST_TASK_COLLECTION].insert_one(new_task.__dict__)
        
        return created_task
    
    except ValueError as err:  # If there is an invalid user information, raise a ValueError
        raise ValueError(str(err))
    except Exception as err:  # If there is any other exception, raise a ValueError
        raise ValueError(str(err))

def get_task_created_by_user(user_id):
    """
    Get tasks created by the user.

    This function retrieves tasks created by the user with the given user ID.

    Args:
        user_id (str): The ID of the user.

    Returns:
        list: A list of tasks created by the user, with each task's '_id' field converted to a string.

    Raises:
        ValueError: If there is an error in fetching the tasks.
    """
    try:
        # Connect to the tasks collection of the database.
        task_collection = conn.database.get_collection(config.CONST_TASK_COLLECTION)

        # Retrieve tasks created by the user.
        # Find tasks where the 'createdByUid' field matches the given user ID.
        task_list = list(task_collection.find({"createdByUid": user_id}))

        # Convert the '_id' field of each task to a string.
        # This is done to ensure that the '_id' field is serialized as a string when returned.
        for task in task_list:
            task["_id"] = str(task["_id"])

        return task_list  # Return the list of tasks created by the user
    
    except Exception as error:
        # Raise a ValueError with an appropriate error message if there is an error in fetching the tasks.
        raise ValueError("Error on trying to fetch tasks created by user.", error)

def get_tasks_assigned_to_user(assignedToUid):
    """
    Get tasks assigned to the user.

    This function retrieves tasks assigned to the user with the given assignedToUid.

    Args:
        assignedToUid (str): The ID of the user.

    Returns:
        list: A list of tasks assigned to the user, with each task's '_id' field converted to a string.

    Raises:
        ValueError: If there is an error in fetching the tasks.
    """
    try:
        # Retrieve tasks assigned to the user
        tasks = conn.database[config.CONST_TASK_COLLECTION].find(
            {"assignedToUid": assignedToUid})  # Find tasks assigned to the user

        # Convert the tasks to a list
        user_tasks = list(tasks)

        # Convert the '_id' field of each task to a string
        for task in user_tasks:
            task["_id"] = str(task["_id"])  # Convert task ID to string

        return user_tasks  # Return the list of tasks assigned to the user
    
    except Exception as err:
        # Raise a ValueError with an appropriate error message if there is an error in fetching the tasks.
        raise ValueError("Error fetching tasks assigned to user: ", err)

def update_task(user_info, task_id, done):
    """
    Update the status of a task in the database.

    Args:
        user_info (dict): A dictionary containing user-related information retrieved from the token, including the user's ID.
        task_id (str): The ID of the task to be updated.
        done (bool): The new status of the task.

    Returns:
        pymongo.results.UpdateResult: The result of the update operation.

    Raises:
        ValueError: If the task is not found or the user is not authorized to update the task.
    """
    try:
        # Connect to the tasks collection of the database.
        task_collection = conn.database[config.CONST_TASK_COLLECTION]

        # Find the task with _id = task_id.
        current_task = task_collection.find_one({"_id": ObjectId(task_id)})

        # Check if the task exists.
        if current_task is None:
            raise ValueError('Task not found')

        # Check if the user is authorized to update the task.
        if str(current_task['assignedToUid']) != str(user_info["id"]):
            raise ValueError('Users can only change status when task is assigned to them.')

        # Update the 'done' field of the task with _id = task_id to the new status.
        # The $set operator is used to update the value of the 'done' field.
        updated_result = task_collection.update_one(
            {"_id": ObjectId(task_id)},  # Query to find the task
            {"$set": {"done": done}}  # Update operation to set the 'done' field
        )

        # Return the result of the update operation.
        return updated_result

    except Exception as err:
        # Raise a ValueError with an appropriate error message if there is an error in updating the task.
        raise ValueError('Error on updating task: ' f'{err}')

def delete_task(user_information, task_id):
    """Delete a task from the database.

    Args:
        user_information (dict): A dictionary containing user-related information retrieved from the token, including the user's ID.
        task_id (str): The ID of the task to be deleted.

    Returns:
        pymongo.results.DeleteResult: The result of the delete operation.

    Raises:
        ValueError: If the task is not found or the user is not authorized to delete the task.
    """
    try: 
        
        # Extract the current user ID from the user_information dictionary.
        current_user_id = user_information["id"]
        
        # Using db_connection property
        # task_collection = conn.db_connection[config.CONST_DATABASE][config.CONST_TASK_COLLECTION]
        # task_collection = conn.db_connection.get_database(config.CONST_DATABASE).get_collection(config.CONST_TASK_COLLECTION)
        
        # task_collection = conn.database[config.CONST_TASK_COLLECTION]
        
        # Connect to the tasks collection of the database.
        task_collection = conn.database.get_collection(config.CONST_TASK_COLLECTION)
        
        # Find the task with _id = task_id.
        current_task = task_collection.find_one({'_id': ObjectId(task_id)})
        
        # Check if the task exists.
        # print("Current_task = ", current_task)
        
        # Checking whether given taskUid is valid(present in the database) or not. If not then raise error .
        if (current_task == None):
            raise ValueError(f"Task not found with id = {str(task_id)} in the database.")
               
        # Checking whether createdByUid of the task is equal to the uid of the user making the request.
        if str(current_task["createdByUid"]) != current_user_id:
            raise ValueError('Users can only delete when task is created by them.')
         
        # Delete the task with _id = {task_id} from task collection of the database.
        deleted_result = task_collection.delete_one({"_id": ObjectId(task_id)})
        
        # Return the delete_result.
        return deleted_result
        
    except Exception as error:
        raise ValueError('Error on deleting task: ' f'{error}')
    