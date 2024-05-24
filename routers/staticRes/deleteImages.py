from fastapi import APIRouter, Query, Header
from configs import IMAGE_RESOURCE_PATH
import os
from utilities import verify_authorization

router = APIRouter()

@router.delete("/api/deleteImages", 
            summary="删除图片", 
            description="将指定图片从服务器中删除", 
            tags=["StaticRes/Image"])
async def delete_images(filenames: list = Query(..., description="图片文件名列表"), authorization: str = Header(None)):
    # token = verify_authorization(authorization)

    # 验证token是否合法
    # if not invalid_token(token):
    #     raise HTTPException(status_code=401, detail="无权访问")

    response = []
    for filename in filenames:
        file_path = os.path.join(IMAGE_RESOURCE_PATH, filename)
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