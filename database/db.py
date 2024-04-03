from pymongo import MongoClient

class Database():
    
        # Constructor
    def __init__(self, database_name=None, connection_string=None):
        
        if((database_name == None) or (connection_string == None)):
            raise Exception("Mongo DB requires database name and string connection!")
        
        self.__database_name = database_name
        self.__connection_string = connection_string
        self.__db_connection = None
        self.__database = None
    
    # Getter for database object.
    @property
    def database(self):
        return self.__database
    
    # Getter for connection object.
    @property
    def db_connection(self):
        return self.__db_connection

    # Method to connect with database.
    def connect(self):
        """ Method to connect with given connection and database. """
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
