from flask import current_app
def users_collection():
    return current_app.db["users"]
