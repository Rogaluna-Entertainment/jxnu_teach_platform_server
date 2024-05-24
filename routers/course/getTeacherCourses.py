from fastapi import APIRouter, HTTPException, Query, Header
from typing import List, Optional
from pydantic import BaseModel
from utilities import read_entries

router = APIRouter()

class CourseDetail(BaseModel):
    course_id: int
    course_name: str
    creator_name: Optional[str] = None
    course_group_id: Optional[int] = None
    course_cover_url: Optional[str] = None

@router.get("/api/getTeacherCourses", 
            summary="获取教师课程", 
            description="获取教师教学的课程", 
            tags=["Course/Teacher"], 
            response_model=List[CourseDetail])
async def get_teacher_courses(teacher_id: int = Query(..., description="要获取课程的教师的ID"), authorization: str = Header(None)):
    # token = verify_authorization(authorization)
    
    # 从token中获取用户权限老师或学生
    authority = 'teacher'

    # 如果权限不是教师。
    if not authority == 'teacher':
        raise HTTPException(status_code=401, detail="无权访问")
    
    try:
        # 获取教师的所有课程ID
        courses = await read_entries(
            table_name="teacher_courses_mapping_table",
            filters={"teacher_id": teacher_id}
        )
        # 从结果中提取课程ID列表
        course_ids = [course['course_id'] for course in courses]
        
        if course_ids:
            # 使用获取到的课程ID查询课程详细信息
            detailed_courses = await read_entries(
                table_name="unified_courses_table",
                filters={"course_id": course_ids},
                fields=["course_id", "course_name", "creator_id", "course_group_id", "course_cover_url"]
            )

            # 查询每个课程的创建者姓名
            creator_ids = {course['creator_id'] for course in detailed_courses}
            creators = {}
            for creator_id in creator_ids:
                creator_info = await read_entries(
                    table_name="unified_account_table",
                    filters={"account_id": creator_id},
                    fields=["name"]
                )
                if creator_info:
                    creators[creator_id] = creator_info[0]['name']

            # 构建最终的课程详细信息列表，包括教师姓名
            return [
                CourseDetail(
                    course_id=course['course_id'],
                    course_name=course['course_name'],
                    creator_name=creators.get(course['creator_id'], "Unknown"),
                    course_group_id=course['course_group_id'],
                    course_cover_url=course['course_cover_url']
                ) for course in detailed_courses if 'course_id' in course and 'course_name' in course  # 确保至少有这些基础字段
            ]
        return []  # 如果没有课程ID，返回空列表
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询错误: {str(e)}")
