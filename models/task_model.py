
# Class representing a Task model.
class Task:
    """Class representing a Task model."""
    # Constructor
    def __init__(self):
        self.createdByUid = ""
        self.createdByName = ""
        self.assignedToUid = ""
        self.assignedToName = ""
        self.description = ""
        self.done = False
    
    # Method to display detail about the task.
    def displayDetail(self):
        """Method to display detail about the task."""
        print(f"\nCreated by ID = {self.createdByUid}\nCreated by Name = {self.createdByName}\nAssigned To ID = {self.assignedToUid}\nAssigned To Name = {self.assignedToName}\nDescription = {self.description}\nDone = {self.done}\n")


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