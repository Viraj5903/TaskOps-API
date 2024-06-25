
# Class representing a Task model.
class Task:
    """Class representing a Task model."""
    # Constructor
    def __init__(self):
        """
        Constructor for the Task class.

        Initializes the instance variables createdByUid, createdByName, assignedToUid, assignedToName, description and done to empty strings and False respectively.
        """
        # UID of the user who created the task
        self.createdByUid = ""
        # Name of the user who created the task
        self.createdByName = ""
        # UID of the user to whom the task is assigned
        self.assignedToUid = ""
        # Name of the user to whom the task is assigned
        self.assignedToName = ""
        # Description of the task
        self.description = ""
        # Flag indicating if the task is done or not
        self.done = False
    
    # Method to display detail about the task.
    def displayDetail(self):
        """
        Method to display detail about the task.

        This method prints the createdByUid, createdByName, assignedToUid, assignedToName, description and done of the task.
        """
        # Print the createdByUid of the task
        print(f"\nCreated by ID = {self.createdByUid}")
        
        # Print the createdByName of the task
        print(f"Created by Name = {self.createdByName}")
        
        # Print the assignedToUid of the task
        print(f"Assigned To ID = {self.assignedToUid}")
        
        # Print the assignedToName of the task
        print(f"Assigned To Name = {self.assignedToName}")
        
        # Print the description of the task
        print(f"Description = {self.description}")
        
        # Print the done status of the task
        print(f"Done = {self.done}\n")


# Object example 
""" 
task1 = Task()
task1.createdByUid = 1
task1.createdByName = "ABC"
task1.assignedToUid = 11
task1.assignedToName = "XYZ"
task1.description = "Task project"

task1.displayDetail()
 """