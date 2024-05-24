from fastapi import APIRouter, HTTPException, status, Header
from pydantic import BaseModel
from typing import List, Optional
from utilities import verify_authorization, read_entries

class KnownledgePointLink(BaseModel):
    start_node: int
    end_node: int
    link_name: str
    course_id: int


router = APIRouter()


@router.get("/api/getNodesLink", 
            summary="获取知识图谱节点信息", 
            description="获取知识图谱节点信息", 
            tags=["Course/KnownledgeGraph"],
            response_model=List[KnownledgePointLink])
async def get_nodes_link(authorization: str = Header(None)):
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
        groups = await read_entries("knownledge_point_link_table", filters=filters)
        if not groups:
            return []
        knownledgePointLinks = [KnownledgePointLink(**group) for group in groups]
        
        return knownledgePointLinks
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))