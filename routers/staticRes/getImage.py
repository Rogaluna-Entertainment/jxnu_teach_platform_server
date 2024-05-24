from fastapi import APIRouter, HTTPException, Query, Header
from fastapi.responses import FileResponse
import os
from configs import IMAGE_RESOURCE_PATH
from utilities import verify_authorization

router = APIRouter()

@router.get("/api/getImages", 
            summary="获取图片", 
            description="从服务器中获取指定图片", 
            tags=["StaticRes/Image"])
async def get_image(filename: list = Query(..., description="图片文件名"), authorization: str = Header(None)):
    # token = verify_authorization(authorization)

    # 验证token是否合法
    # if not invalid_token(token):
    #     raise HTTPException(status_code=401, detail="无权访问")

    # 构造文件路径
    file_path = os.path.join(IMAGE_RESOURCE_PATH, filename)

    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="图片未找到")

    # 返回图片文件
    return FileResponse(file_path)
