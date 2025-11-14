from pymongo import MongoClient

mongo_client = None
def init_mongo(app):
    global mongo_client
    mongo_uri = app.config["MONGO_URI"]
    db_name = app.config["MONGO_DB_NAME"]
    mongo_client = MongoClient(mongo_uri)
    app.db = mongo_client[db_name]
    return mongo_client
