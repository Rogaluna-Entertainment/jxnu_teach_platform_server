from fastapi import APIRouter, HTTPException, Header
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError
from typing import Optional
from utilities import create_entry, verify_authorization

router = APIRouter()


class Account(BaseModel):
    name: str
    telephone_number: str
    email: Optional[str] = None
    password: str
    user_type: str


class StudentInfo(BaseModel):
    college_id: int
    speciality_id: int
    class_id: int
    student_id: int


class TeacherInfo(BaseModel):
    college_id: int
    teacher_id: int


class AdminInfo(BaseModel):
    admin_id: int


class AccountRequest(BaseModel):
    account: Account
    student_info: Optional[StudentInfo] = None
    teacher_info: Optional[TeacherInfo] = None
    admin_info: Optional[AdminInfo] = None
    

@router.post("/api/addAccount", 
            summary="添加账户", 
            description="添加账户", 
            tags=["Account/Manager"])
async def add_account(request: AccountRequest, authorization: str = Header(None)):
    # token = verify_authorization(authorization)

    # 从token中获取用户权限
    authority = 'admin'

    # 如果权限不是管理员。
    if not authority == 'admin':
        raise HTTPException(status_code=401, detail="无权访问")

    try:
        account_data = jsonable_encoder(request.account)
        account_id = await create_entry('unified_account_table', account_data)
        
        if request.account.user_type == 'student' and request.student_info:
            student_data = jsonable_encoder(request.student_info)
            student_data['account_id'] = account_id
            await create_entry('student_info_table', student_data)
        elif request.account.user_type == 'teacher' and request.teacher_info:
            teacher_data = jsonable_encoder(request.teacher_info)
            teacher_data['account_id'] = account_id
            await create_entry('teacher_info_table', teacher_data)
        elif request.account.user_type == 'admin' and request.admin_info:
            admin_data = jsonable_encoder(request.admin_info)
            admin_data['account_id'] = account_id
            await create_entry('admin_info_table', admin_data)

        return {"message": "账户已添加", "account_id": account_id}
    except ValidationError as ve:
        raise HTTPException(status_code=400, detail=f"校验错误: {ve}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加错误: {e}")