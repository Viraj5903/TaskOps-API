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
    
    #Hi , new code 
    pass

# TODO: Viraj Patel
def delete_task():
    pass