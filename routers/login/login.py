from fastapi import APIRouter, status, HTTPException, Body, Response
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from typing import Optional
from utilities import read_entries, create_token
from datetime import datetime, timedelta
from configs import ACCESS_TOKEN_EXPIRE

router = APIRouter()

class Account(BaseModel):
    account_id: int
    name: Optional[str] = None
    telephone_number: Optional[str] = None
    email: Optional[str] = None
    password: str
    user_type: str

class LoginData(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


# 密码上下文配置，用于密码的验证和加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/api/login", 
            summary="登录账户", 
            description="登录账户", 
            tags=["Login/Login"])
async def login(data: LoginData, response: Response):
    username = data.username
    password = data.password

    try:
        # 读取账户数据
        accounts_data = await read_entries('unified_account_table', filters={'telephone_number': username}, limit=1)
        if not accounts_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="账户不存在")
        account_instance = Account(**accounts_data[0]) # 得到账户数据实例

        # 使用passlib的context验证密码
        # pwd_context.verify(password, account_instance.password)
        if password == account_instance.password:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE["minutes"])
            access_token = create_token(
                data={
                    "id": account_instance.account_id,
                    "auth": account_instance.user_type
                }, expires_delta=access_token_expires
            )
            
            return JSONResponse(content={
                'message': '登录成功',
                'authority': account_instance.user_type,
                'username': account_instance.name,
                'token': f"{access_token}",
                'accountId': account_instance.account_id
            }, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={
                'message': '密码错误',
                'authority': 'none',
                'username': '',
                'token': '123',
                'accountId': ''
            }, status_code=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))