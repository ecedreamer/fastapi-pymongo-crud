from fastapi.logger import logger
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth.db_helpers import user_exists
from auth.utils import validate_access_token

auth_scheme = HTTPBearer()


def login_required(auth_header: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> dict:
    if auth_header.scheme != "Bearer":
        logger.warning(f"login_required; Authentication failed")
        return {"status": "failure", "message": "Invalid access token"}
    payload = validate_access_token(auth_header.credentials)
    if not payload:
        return {"status": "failure", "message": "Invalid access token"}
    user = user_exists(payload.get("email"), status="active")
    if not user:
        return {"status": "failure", "message": "Invalid access token"}
    if user.get("password") != payload.get("password"):
        return {"status": "failure", "message": "Credentials changed"}
    del user["password"]
    return {"status": "success", "user": user}


def employee_required(user=Depends(login_required)) -> bool:
    return user


def admin_required(user=Depends(login_required)) -> bool:
    return user
