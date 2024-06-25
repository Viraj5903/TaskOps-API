# Import the necessary modules.

from .db import Database
import app_config as config

##pip install pymongo

# Create an instance of the Database class and initialize it with the MongoDB connection string and the database name retrieved from the app_config module.
conn = Database(connection_string=config.CONST_MONGO_URL, database_name=config.CONST_DATABASE)

# Print the database object of the connection object.
# This is used for debugging purposes.
print("conn.database = ", conn.database)

# Connect to the MongoDB database using the connection object.
# This establishes the connection with the MongoDB server/cluster.
conn.connect()
