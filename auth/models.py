from typing import Literal

from pydantic import BaseModel
from datetime import datetime


class LoginForm(BaseModel):
    email: str
    password: str


class AuthUser(LoginForm):
    role: Literal["Admin", "Employee"]
    status: str = "active"
    last_logged_in: datetime | None = None


class UserProfile:
    user_id: str
    name: str
    profession: str
    experience: int


class UserProfileForm(LoginForm):
    role: Literal["Admin", "Employee"]
    status: str = "active"
    name: str
    profession: str
    experience: int
