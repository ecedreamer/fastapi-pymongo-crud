from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017"
client = MongoClient(MONGO_URL)
database = client.fastapi_mongo

collections = {
    "articles": database.articles,
    "users": database.users,
    "user_profiles": database.user_profiles,
}
