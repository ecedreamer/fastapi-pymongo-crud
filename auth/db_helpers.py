from auth.utils import get_password_hash, verify_password
from main.db_config import get_collections


UserCollection = get_collections("users")
ProfileCollection = get_collections("user_profiles")


def user_helper(user, del_password=False) -> dict:
    user["id"] = str(user.get("_id"))
    user["last_logged_in"] = str(user.get("last_logged_in"))
    user.pop("_id")
    if del_password:
        del user["password"]
    return user


def profile_helper(profile):
    profile["id"] = str(profile.get("_id"))
    profile.pop("_id")
    return profile


def user_create(user_data):
    user_data["password"] = get_password_hash(user_data.get("password"))
    user_id = UserCollection.insert_one(user_data).inserted_id
    user = UserCollection.find_one({"_id": user_id})
    return user_helper(user, del_password=True)


def user_exists(email, **kwargs) -> bool:
    user = UserCollection.find_one({"email": email, **kwargs})
    return user_helper(user) if user else False


def profile_create(profile_data):
    if user_exists(profile_data.get("email")):
        return {"status": "failure", "message": "User with this email already exists"}
    user_data = {
        "email": profile_data.pop("email"),
        "password": profile_data.pop("password"),
        "role": profile_data.pop("role"),
        "status": profile_data.pop("status"),
    }
    user = user_create(user_data)
    profile_data["user_id"] = user.get("id")
    profile_id = ProfileCollection.insert_one(profile_data).inserted_id
    profile = ProfileCollection.find_one({"_id": profile_id})
    return {"status": "success", "user": user, "profile": profile_helper(profile)}


def authenticate_user(credentials):
    user = user_exists(credentials.get("email"))
    if not user:
        return {"status": "failure", "message": "Invalid user credentials"}
    if not verify_password(credentials.get("password"), user.get("password")):
        return {"status": "failure", "message": "Invalid user credentials"}
    profile = ProfileCollection.find_one({"user_id": user.get("id")})
    del user["last_logged_in"]
    return {"status": "success", "user": user, "profile": profile_helper(profile)}
