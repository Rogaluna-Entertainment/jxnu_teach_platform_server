from fastapi import APIRouter, Query, Header
from configs import VIDEO_RESOURCE_PATH
import os
from utilities import verify_authorization

router = APIRouter()

@router.delete("/api/deleteVideos", 
            summary="删除视频", 
            description="将指定视频从服务器中删除", 
            tags=["StaticRes/Video"])
async def delete_videos(filenames: list = Query(..., description="视频文件名列表"), authorization: str = Header(None)):
    # token = verify_authorization(authorization)

    # 验证token是否合法
    # if not invalid_token(token):
    #     raise HTTPException(status_code=401, detail="无权访问")

    response = []
    for filename in filenames:
        file_path = os.path.join(VIDEO_RESOURCE_PATH, filename)
        status = {"filename": filename}
        if not os.path.exists(file_path):
            status["status"] = "不存在"
        else:
            try:
                os.remove(file_path)
                status["status"] = "删除成功"
            except Exception as e:
                status["status"] = "删除错误"
        response.append(status)

    return response
