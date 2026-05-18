from backend.database.mongo_client import (
    users_collection
)

def create_user(user_data):

    existing_user = users_collection.find_one({

        "username": user_data["username"]
    })

    if existing_user:

        return False

    users_collection.insert_one(user_data)

    return True

def get_user(username):

    return users_collection.find_one({

        "username": username
    })