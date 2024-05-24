from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
from utilities import verify_authorization, get_file_extension
from configs import ACCOUNT_RESOURCE_PATH, HEADER_IMAGE_NAME

router = APIRouter()

@router.post("/api/uploadProfilePicture", 
            summary="上传头像图片", 
            description="上传头像图片", 
            tags=["Account/Info"])
async def upload_profile_picture(file: UploadFile = File(...)):
    # token = verify_authorization(authorization)

    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # 解算token得到登录账户id（算子）
    operator = '123'
    if operator != '123':
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 设定头像文件保存路径
    save_directory = Path(f"{ACCOUNT_RESOURCE_PATH}/{operator}/private")
    save_directory.mkdir(exist_ok=True)

    # 安全地生成文件名，防止路径遍历
    ext = get_file_extension(file.filename)
    safe_filename = f"{HEADER_IMAGE_NAME}{ext}"
    safe_path = save_directory / safe_filename

    # 将上传的文件保存到磁盘
    try:
        with safe_path.open("wb") as buffer:
            shutil.copyfileobj(await file.read(), buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")

    return JSONResponse(status_code=200, content={"message": "Avatar uploaded successfully", "filename": str(safe_path)})
