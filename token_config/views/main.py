from fastapi import APIRouter, HTTPException
from extensions.password_hasher import verify_password 
from account.models import User
from token_config.creator import create_access_token, create_refresh_token, verify_access_token

router = APIRouter()

@router.post("/login")
def login(username: str, password: str):
    # get user from database
    user = User.get(username=username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # make tokens
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    
