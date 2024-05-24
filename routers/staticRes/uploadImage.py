from fastapi import APIRouter, HTTPException, File, UploadFile, Header
from configs import IMAGE_RESOURCE_PATH, ALLOWED_IMAGE_EXTENSIONS
from utilities import verify_authorization, save_file

router = APIRouter()


@router.post("/api/uploadImage", 
            summary="上传图片", 
            description="将图片上传到服务器", 
            tags=["StaticRes/Image"])
async def upload_image(file: UploadFile = File(..., description="图片文件"), 
                       authorization: str = Header(None),):
    # token = verify_authorization(authorization)

    # 验证token是否合法
    # if not invalid_token(token):
    #     raise HTTPException(status_code=401, detail="无权访问")

    filename = save_file(file, IMAGE_RESOURCE_PATH, ALLOWED_IMAGE_EXTENSIONS)

    return {"filename": filename}