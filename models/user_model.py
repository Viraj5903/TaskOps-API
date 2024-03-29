
# Class representing a User model.
class User:
    """Class representing a User model."""
    # Constructor
    def __init__(self):
        self.name = ""
        self.email = ""
        self.password = ""
    
    # Method to display detail about the user.
    def displayDetail(self):
        """Method to display detail about the user."""
        print(f"\nName = {self.name}\nEmail = {self.email}\nPassword = {self.password}")