from fastapi import APIRouter, HTTPException, Header
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional
from utilities import update_entry

router = APIRouter()

class AccountUpdate(BaseModel):
    account_id: Optional[int] = None
    name: Optional[str] = None
    telephone_number: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    user_type: Optional[str] = None


class UpdateData(BaseModel):
    accountData: AccountUpdate
    accountId: int


@router.patch("/api/modifyAccount", 
            summary="修改账户信息", 
            description="修改账户信息", 
            tags=["Account/Manager"])
async def modify_account(update_data: UpdateData, authorization: str = Header(None)):
    # token = verify_authorization(authorization)

    # 从token中获取用户权限
    authority = 'admin'

    # 如果权限不是管理员。
    if not authority == 'admin':
        raise HTTPException(status_code=401, detail="无权访问")
    
    account_data = jsonable_encoder(update_data.accountData, exclude_unset=False)
    if not account_data:
        raise HTTPException(status_code=400, detail="没有更新数据")

    conditions = {"account_id": update_data.accountId}
    try:
        await update_entry("unified_account_table", account_data, conditions)
        return {"message": "更新成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新错误: {str(e)}")