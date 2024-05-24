from fastapi import APIRouter, HTTPException, status, Header
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
from fastapi.encoders import jsonable_encoder

from utilities import create_entry, verify_authorization


class Course(BaseModel):
    course_name: str
    creator_id: int
    course_group_id: Optional[int] = None
    course_cover_url: Optional[str] = None
    course_gateway_url: Optional[str] = None

router = APIRouter()

@router.post("/api/addCourse", 
            summary="添加课程", 
            description="新建一门课程", 
            tags=["Course/Teacher"], 
            status_code=status.HTTP_201_CREATED)
async def add_course(course: Course, authorization: str = Header(None)):
    payload = verify_authorization(authorization)
    # 从token中获取用户权限老师或学生
    authority = payload["user_auth"]

    # 如果权限不是教师。
    if not authority == 'teacher':
        raise HTTPException(status_code=401, detail="无权访问")

    data = jsonable_encoder(course, exclude_none=True)
    try:
        last_record_id = await create_entry("unified_courses_table", data)
        return {"message": "课程已添加", "course_id": last_record_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"课程添加失败: {str(e)}")