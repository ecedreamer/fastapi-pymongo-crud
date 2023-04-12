from datetime import datetime, timedelta, timezone
from fastapi.logger import logger
from passlib.context import CryptContext
from jose import jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "177dcab3e5ddea388686356013aefe887d2639deabcc0683a555afeb4acb2346"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def validate_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        logger.warning(f"validate_access_token; {e}")
        return {}
    return payload
