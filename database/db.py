from pymongo import MongoClient

class Database():
    """
    The Database class provides an interface for interacting with MongoDB databases. 
    It handles connection and database object management.
    
    The class maintains a connection to a MongoDB instance/Cluster, and a reference to a specific database within that instance.
    """
    
    # Constructor
    def __init__(self, database_name=None, connection_string=None):
        """
        Constructor for the Database class.

        Initializes the instance variables database_name, connection_string, db_connection, and database to None.

        Args:
            database_name (str): The name of the database.
            connection_string (str): The connection string to the MongoDB instance.

        Raises:
            Exception: If either database_name or connection_string is None.
        """
        # Check if both database_name and connection_string are provided
        if((database_name == None) or (connection_string == None)):
            raise Exception("Mongo DB requires database name and string connection!")
        
        # Set the database name
        self.__database_name = database_name
        # Set the connection string
        self.__connection_string = connection_string
        # Set the database connection object to None
        self.__db_connection = None
        # Set the database object to None
        self.__database = None
    
    # Getter for database object.
    @property
    def database(self):
        """
        Getter for the database object.

        Returns:
            pymongo.database.Database: The database object.
        """
        # Return the database object.
        return self.__database
    
    # Getter for connection object.
    @property
    def db_connection(self):
        """
        Getter for the database connection object.

        Returns:
            pymongo.MongoClient: The database connection object.
        """
        # Return the database connection object.
        return self.__db_connection

    # Method to connect with database.
    def connect(self):
        """ 
        Method to connect with given connection and database.
        
        Raises:
            Exception: If connection to MongoDB fails.
        """
        try:
            # Connection object to MongoDB instance/Cluster. Connecting to a Cluster.
            # __db_connection :  Establishing a connection to a MongoDB server (Cluster (which contains databases.)) (databases). __db_connection is the connection object to the MongoDB instance.
            self.__db_connection = MongoClient(self.__connection_string)
            db_name = str(self.__database_name)
            
            # __database : It is assigned a reference to a specific database within the MongoDB instance, obtained by accessing the __db_connection object and selecting the database specified by the db_name. __database is a reference to a specific database within that MongoDB instance (Here, __db_connection is the MongoDB instance).
            # Database connection object (Connection with database name = self.__database_name). Connecting to {__database_name} database within cluster.
            self.__database =  self.__db_connection[db_name]

        except Exception as err:
            print("Mongo DB connection error!", err)
