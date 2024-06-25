
# Class representing a User model.
class User:
    """Class representing a User model."""
    # Constructor
    def __init__(self):
        """
        Constructor for the User class.

        Initializes the instance variables name, email and password to empty strings.
        """
        # Name of the user
        self.name = ""
        # Email of the user
        self.email = ""
        # Password of the user
        self.password = ""
    
    # Method to display detail about the user.
    def displayDetail(self):
        """
        Method to display detail about the user.

        This method prints the name, email and password of the user.
        """
        # Print the name of the user
        print(f"\nName = {self.name}")
        
        # Print the email of the user
        print(f"Email = {self.email}")
        
        # Print the password of the user
        print(f"Password = {self.password}")
