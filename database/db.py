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
            self.__db_connection = MongoClient(self.__connection_string)
            db_name = str(self.__database_name)
            self.__database =  self.__db_connection[db_name]

        except Exception as err:
            print("Mongo DB connection error!", err)