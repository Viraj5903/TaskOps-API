from models.task_model import Task
from database.__init__ import conn
from bson.objectid import ObjectId
import app_config as config

# TODO: Manpreet Kaur
def create_task():
    pass

# TODO: Dil Raval
def get_task_created_by_user():
    pass

# TODO: Aryan Handa
def get_tasks_assigned_to_user():
    pass

# TODO: Payal Rangra
def update_task(user_info , task_id ,  done ):
    
    try:
        task_collection=conn.database[config.CONST_TASK_COLLECTION]
        
        current_task = task_collection.find_one({"_id":ObjectId(task_id)})
        if(current_task==None):  
            return "No such task exists."
        
        if str(current_task['assignedToUid'])!=str(user_info["id"]):
            raise ValueError('Users can only change status when task is assigned to them.')
        
        updated_result = task_collection.update_one({"_id":ObjectId(task_id)}, {"$set": {"done": done}})
        
        return updated_result
    except Exception as err:
        raise ValueError("Error on updating task.", err)

# TODO: Viraj Patel
def delete_task():
    pass