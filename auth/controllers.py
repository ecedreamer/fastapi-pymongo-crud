from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from main.logger import logging
from auth.db_helpers import profile_create, authenticate_user
from auth.dependencies import employee_required
from auth.models import UserProfileForm, LoginForm
from auth.utils import create_access_token

router = APIRouter(tags=["User Auth"])


logger = logging.getLogger("auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register")
def register(profile_data: UserProfileForm):
    created_profile = profile_create(profile_data.dict())
    if created_profile.get("status") == "failure":
        return JSONResponse(created_profile, status_code=400)
    return JSONResponse(created_profile, status_code=201)


@router.post("/login")
def login(credentials: LoginForm):
    resp = authenticate_user(credentials.dict())
    if resp.get("status") == "failure":
        logger.warning(f"Failed login attempt from user {credentials.email}; error={resp.get('message')}")
        return JSONResponse(resp, status_code=401)
    user = resp.get("user")
    access_token = create_access_token(user)
    del user["password"]
    logger.warning(f"Successful login from user {credentials.email}")
    return JSONResponse({"access_token": access_token, "user": user}, status_code=200)


@router.get("/profile")
def profile(user: str = Depends(employee_required)):
    if user.get("status") == "failure":
        return JSONResponse(user, status_code=403)
    return JSONResponse(user)
