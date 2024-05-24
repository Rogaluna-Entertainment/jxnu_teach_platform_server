from fastapi import APIRouter, HTTPException, Query, Header
from fastapi.responses import FileResponse
import os
from configs import VIDEO_RESOURCE_PATH
from utilities import verify_authorization

router = APIRouter()

@router.get("/api/getVideo", 
            summary="获取视频", 
            description="从服务器上获取指定视频", 
            tags=["StaticRes/Video"])
async def get_video(filename: str = Query(..., description="视频文件名"), 
                    authorization: str = Header(None)):
    # token = verify_authorization(authorization)

    # 验证token是否合法
    # if not invalid_token(token):
    #     raise HTTPException(status_code=401, detail="无权访问")

    # 构造文件路径
    file_path = os.path.join(VIDEO_RESOURCE_PATH, filename)

    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="视频未找到")

    # 返回视频文件
    return FileResponse(file_path)
