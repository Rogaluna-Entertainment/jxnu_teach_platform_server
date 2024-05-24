from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional
from utilities import read_entries, verify_authorization

router = APIRouter()

class GroupNode(BaseModel):
    group_id: int
    parent_group_id: Optional[int]
    group_name: str
    college_id: Optional[int]
    children_group: List['GroupNode'] = []

@router.get("/api/getCourseGroup", 
            summary="获取课程分组", 
            description="获取所有课程的分组", 
            tags=["Course/Teacher"], 
            response_model=List[GroupNode])
async def get_course_group(authorization: str = Header(None)):
    # token = verify_authorization(authorization)

    # 从token中获取用户权限和学院id
    authority = 'teacher'
    college_id = 123
    

    # 如果权限不是教师。
    if not authority == 'teacher':
        raise HTTPException(status_code=401, detail="无权访问")
    
    try:
        # 构建过滤条件，包括公选课
        filters = {}
        if college_id is not 0:
            filters['college_id'] = [college_id, 0]
        else:
            filters['college_id'] = 0

        # 从数据库获取所有组
        groups = await read_entries("course_group_table", filters=filters)
        if not groups:
            return []
        # 转换成字典
        group_dict = {group['group_id']: GroupNode(**group) for group in groups}
        # 构建树状结构
        root_groups = []
        for group in groups:
            parent_id = group['parent_group_id']
            if parent_id != None:
                parent_node = group_dict.get(parent_id)
                if parent_node:
                    parent_node.children_group.append(group_dict[group['group_id']])
            else:
                root_groups.append(group_dict[group['group_id']])
        
        return root_groups
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))