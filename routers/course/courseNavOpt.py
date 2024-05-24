from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import List, Dict, Optional
from utilities import verify_authorization


router = APIRouter()


class CourseOption(BaseModel):
    index: str
    icon: Optional[str] = None  
    title: str
    name: Optional[str] = None
    children: Optional[List['CourseOption']] = None


class CourseNavigation(BaseModel):
    defaultActive: str
    options: List[CourseOption]


class CourseResponse(BaseModel):
    message: str
    content: CourseNavigation


class CourseNavRequest(BaseModel):
    courseId: str


@router.post("/api/courseNavOpt", 
            summary="获取课程导航选项", 
            description="不同的课程所拥有功能，比如说英语课程有口语，那么就要有额外的口语选项。", 
            tags=["Course"], 
            response_model=CourseResponse)
async def course_nav_opt(request: CourseNavRequest, authorization: str = Header(None)):   
    payload = verify_authorization(authorization)
    # 从token中获取用户权限老师或学生
    authority = payload["user_auth"]

    # 通过课程id及权限获取课程选项信息。
    if not request.courseId:
        raise HTTPException(status_code=400, detail="Course ID is required")

    if authority == 'student':
        options_data = [
            CourseOption(
                index="1", icon="el-icon-document", title="任务", name="task"
            ),
            CourseOption(
                index="2", icon="el-icon-s-management", title="章节", name="chapter"
            ),
            CourseOption(
                index="3", icon="el-icon-s-grid", title="学习资源", name="resource"
            ),
            CourseOption(
                index="4", icon="el-icon-s-custom", title="答疑", name="answering"
            ),
            CourseOption(
                index="5", icon="el-icon-document-copy", title="作业", name="homework"
            ),
            CourseOption(
                index="6", icon="el-icon-tickets", title="测评", name="examination"
            ),
            CourseOption(
                index="7", icon="el-icon-share", title="学习图谱", name="knowledgeGraph"
            ),
            CourseOption(
                index="8", icon="el-icon-s-comment", title="口语测评", name="oralTest"
            ),
            CourseOption(
                index="9", icon="el-icon-s-opportunity", title="个人推荐",
                children=[
                    CourseOption(index="9-1", title="推荐任务", name="recommendTask"),
                    CourseOption(index="9-2", title="推荐资源", name="recommendResource"),
                ]
            )
        ]
    elif authority == 'teacher':
        options_data = [
            CourseOption(
                index="1", icon="el-icon-document", title="任务管理", name="task"
            ),
            CourseOption(
                index="2", icon="el-icon-s-management", title="章节管理", name="chapter"
            ),
            CourseOption(
                index="3", icon="el-icon-s-grid", title="学习资源管理", name="resource"
            ),
            CourseOption(
                index="4", icon="el-icon-s-grid", title="题库", name="questionBank"
            ),
            CourseOption(
                index="5", icon="el-icon-s-custom", title="答疑", name="answering"
            ),
            CourseOption(
                index="6", icon="el-icon-document-copy", title="作业管理", name="homework"
            ),
            CourseOption(
                index="7", icon="el-icon-tickets", title="测评管理", name="examination"
            ),
            CourseOption(
                index="8", icon="el-icon-share", title="学习图谱", name="knowledgeGraph"
            ),
            CourseOption(
                index="9", icon="el-icon-s-comment", title="学生口语测评", name="oralTest"
            ),
            CourseOption(
                index="10", icon="el-icon-coin", title="班级管理", name="classManager"
            )
        ]

    response_content = CourseNavigation(defaultActive="1", options=options_data)

    # 返回课程的导航选项信息
    return CourseResponse(
        message="成功",
        content=response_content
    )