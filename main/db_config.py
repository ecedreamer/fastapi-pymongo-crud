import os

from pymongo import MongoClient

MONGO_URL = os.environ.get('MONGO_URI')
if not MONGO_URL:
    MONGO_URL = "mongodb://127.0.0.1:27017"


def get_collections(collection):
    client = MongoClient(MONGO_URL)
    database = client.fastapi_mongo
    collections = {
        "articles": database.articles,
        "users": database.users,
        "user_profiles": database.user_profiles,
    }
    return collections.get(collection)
