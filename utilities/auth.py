# utilities/auth.py
from fastapi import HTTPException
from secrets import token_urlsafe
import jwt 
from jwt import PyJWTError
from datetime import datetime, timedelta
from typing import Optional
from configs import SECRET_KEY, ALGORITHM


def generate_secret_key(length=64):
    """
        生成SECRET_KEY, SECRET_KEY是固定值, 主要目的是用作签名过程的一部分, 以验证token的真实性和完整性。
    """
    return token_urlsafe(length)


def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_authorization(authorization: str):
    """
    验证Authorization标头并提取令牌。
    如果Authorization标头无效, 则引发HTTPException。
    
    Args:
    - authorization (str): Authorization header value.

    Returns:
    - str: The extracted token.
    """
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = authorization.split(" ")[1]  # Split the string to get the token part.
    return invalid_token(token)


def invalid_token(token):
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        user_auth = payload.get("auth")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token: Unknown Id")
        # 可以在这里添加更多的验证逻辑，例如验证用户权限等
        if user_auth is None: 
            raise HTTPException(status_code=401, detail="Invalid Token: Unknown Auth")
        return {"message": "Valid Token", "user_id": user_id, "user_auth": user_auth}
    except PyJWTError as e:
        raise HTTPException(status_code=403, detail="Could not validate credentials")