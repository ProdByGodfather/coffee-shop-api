from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status, Header

from account.models import User
from token_config.config import *

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def retrive_user(
    token: str = Header(
        default="Bearer ",
        convert_underscores=False,
        description="JWT in the header"
    )
):
    auth_key = token[7:]
    user = verify_access_token(auth_key)
    is_user = User.get(username = user)
    if not is_user:
        raise HTTPException(401, "Can't access to this section")
    user = User.get(username = user)
    return user.__dict__


def retrive_user_grpc(client_code: str) -> dict:
    user = verify_access_token(client_code)
    user = User.get(username = user)
    if not user:
        return False
    return user.__dict__