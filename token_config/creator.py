from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status, Header, Request

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


async def retrive_user(
    token: str = Header(
        default=None,  # پیش‌فرض برای هدر "Authorization"
        convert_underscores=False,
        description="JWT in the Authorization header"
    ),
    request: Request = None  # دریافت درخواست (Request) برای استفاده از پارامترهای query یا body
):
    # ابتدا تلاش می‌کنیم توکن را از هدر بگیریم
    if not token or token == "Bearer ":
        # اگر توکن در هدر نبود، از بدنه درخواست استفاده می‌کنیم
        body = await request.json()  # نیاز به await برای دریافت body به‌صورت async
        token_from_request = body.get("token")  # توکن را از body دریافت می‌کنیم
        if not token_from_request:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing in both Authorization header and request body"
            )
        token = token_from_request

    # جدا کردن مقدار توکن از Bearer
    if token.startswith("Bearer "):
        auth_key = token[len("Bearer "):].strip()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token must be prefixed with 'Bearer '"
        )

    if not auth_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing after 'Bearer '"
        )

    # تأیید اعتبار توکن
    user = verify_access_token(auth_key)

    # بررسی وجود کاربر در پایگاه داده
    is_user = User.get(username=user)
    if not is_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to access this section"
        )

    return is_user.__dict__