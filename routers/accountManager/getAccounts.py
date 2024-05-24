from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, Field
from typing import List, Optional
from utilities import read_entries, count_entries

router = APIRouter()


class Account(BaseModel):
    account_id: int
    name: Optional[str] = None
    telephone_number: Optional[str] = None
    email: Optional[str] = None
    password: str
    user_type: str


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1, description="当前页码")
    page_size: int = Field(default=10, ge=1, description="每页条目数")


class Pagination(BaseModel):
    page: int = Field(default=1, ge=1, description="当前页码")
    page_size: int = Field(default=10, ge=1, description="每页条目数")
    total: int = Field(description="当前获取的条目数")
    data: List[Account] = Field(default=[], description="分页数据列表")


# 示例："http://localhost:8000/api/accounts/?page=1&page_size=10"
@router.get("/api/getAccounts", 
            summary="获取一组账户", 
            description="获取一组账户的基本信息", 
            tags=["Account/Manager"], 
            response_model=Pagination)
async def get_accounts(pagination: PaginationParams = Depends(), authorization: str = Header(None)):
    # token = verify_authorization(authorization)

    # 从token中获取用户权限
    authority = 'admin'

    # 如果权限不是管理员。
    if not authority == 'admin':
        raise HTTPException(status_code=401, detail="无权访问")

    offset = (pagination.page - 1) * pagination.page_size
    try:
        accounts_data = await read_entries(
            table_name="unified_account_table",
            order_by="account_id ASC",
            limit=pagination.page_size,
            offset=offset
        )
        total_count = await count_entries("unified_account_table")
        accounts = [Account(**account) for account in accounts_data]
        return Pagination(page=pagination.page, page_size=pagination.page_size, total=total_count, data=accounts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
