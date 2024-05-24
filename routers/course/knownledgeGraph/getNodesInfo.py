from fastapi import APIRouter, HTTPException, status, Header
from pydantic import BaseModel
from typing import List, Optional
from utilities import verify_authorization, read_entries

class KnownledgePointInfo(BaseModel):
    knownledge_point_id: int
    course_id: int
    layout: str
    weight: int
    knownledge_point_name: str
    knownledge_point_category: str


router = APIRouter()


@router.get("/api/getNodesInfo", 
            summary="获取知识图谱节点信息", 
            description="获取知识图谱节点信息", 
            tags=["Course/KnownledgeGraph"],
            response_model=List[KnownledgePointInfo])
async def get_nodes_info(authorization: str = Header(None)):
    # payload = verify_authorization(authorization)
    # # 从token中获取用户权限老师或学生
    # authority = payload["user_auth"]

    # 如果无权访问


    # 查询的课程号
    course_id = 123

    try:
        # 构建过滤条件
        filters = {
            'course_id': course_id
        }

        # 从数据库获取所有组
        groups = await read_entries("knownledge_point_table", filters=filters)
        if not groups:
            return []
        knownledgePointInfos = [KnownledgePointInfo(**group) for group in groups]
        
        return knownledgePointInfos
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))