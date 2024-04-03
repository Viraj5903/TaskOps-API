from models.task_model import Task
from database.__init__ import conn
from bson.objectid import ObjectId
import app_config as config

# TODO: Manpreet Kaur
def create_task(task_info):
    try:
        # Access the database to get user information
        created_by_user = conn.database[config.CONST_USER_COLLECTION].find_one({'_id': ObjectId(task_info['created_by_uid'])})
        assigned_to_user = conn.database[config.CONST_USER_COLLECTION].find_one({'_id': ObjectId(task_info['assigned_to_uid'])})
        
        # print("created_by_user", created_by_user)
        # print("assigned_to_user", assigned_to_user)
        
        if not created_by_user or not assigned_to_user:
            raise ValueError('Invalid user information')
        
        # Create a new task object
        new_task = Task()
        new_task.createdByUid = task_info['created_by_uid']
        new_task.createdByName = created_by_user['name']
        new_task.assignedToUid = task_info['assigned_to_uid']
        new_task.assignedToName = assigned_to_user['name']
        new_task.description = task_info['description']
        
        # Save the task to the database
        created_task = conn.database[config.CONST_TASK_COLLECTION].insert_one(new_task.__dict__)
        
        return created_task
    
    except ValueError as err:
        raise ValueError(str(err))
    except Exception as err:
        raise ValueError(str(err))

# TODO: Dil Raval
def get_task_created_by_user():
    pass

# TODO: Aryan Handa
def get_tasks_assigned_to_user():
    pass

# TODO: Payal Rangra
def update_task():
    pass

# TODO: Viraj Patel
def delete_task(user_information, task_id):
    """Delete a task from the database.

    Args:
        user_information (dict): A dictionary containing user-related information retrieved from the token, including the user's ID.
        task_id (str): The ID of the task to be deleted.
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
        
        """ 
        # Check if the task exists.
        print("Current_task = ", current_task)
        
        # Checking whether given taskUid is valid(present in the database) or not. If not then return "Invalid Task".
        if (current_task == None):
            raise ValueError
        """        
        # Checking whether createdByUid of the task is equal to the uid of the user making the request.
        if str(current_task["createdByUid"]) != current_user_id:
            raise ValueError('Users can only delete when task is created by them.')
        
         
        # Delete the task with _id = {task_id} from task collection of the database.
        deleted_result = task_collection.delete_one({"_id": ObjectId(task_id)})
        
        # Return the delete_result.
        return deleted_result
        
    except Exception as error:
        # raise ValueError(f"Error on deleting task: {error}")
        raise ValueError(error)