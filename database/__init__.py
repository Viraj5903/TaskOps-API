from .db import Database
import app_config as config

##pip install pymongo

conn = Database(connection_string=config.CONST_MONGO_URL, database_name=config.CONST_DATABASE)
print("conn.database = ", conn.database)
conn.connect()