from fastapi import APIRouter, File, UploadFile, HTTPException, Header
from configs import VIDEO_RESOURCE_PATH, ALLOWED_VIDEO_EXTENSIONS
from utilities import verify_authorization, save_file

router = APIRouter()

@router.post("/api/uploadVideo", 
            summary="上传视频", 
            description="将视频上传到服务器", 
            tags=["StaticRes/Video"])
async def upload_video(file: UploadFile = File(..., description="视频文件"), authorization: str = Header(None)):
    # token = verify_authorization(authorization)

    # 验证token是否合法
    # if not invalid_token(token):
    #     raise HTTPException(status_code=401, detail="无权访问")

    filename = save_file(file, VIDEO_RESOURCE_PATH, ALLOWED_VIDEO_EXTENSIONS)

    return {"filename": filename}
