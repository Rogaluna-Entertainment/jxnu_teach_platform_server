from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List
from utilities import find_images, verify_authorization
from configs import ACCOUNT_RESOURCE_PATH, HEADER_IMAGE_NAME

router = APIRouter()

@router.get("/api/profilePicture", 
            summary="获取头像图片", 
            description="获取头像图片", 
            tags=["Account/Info"])
async def profile_picture(authorization: str = Header(None)):
    # token = verify_authorization(authorization)

    # 解算token得到登录账户id（算子）
    operator = '123'
    if operator != '123':
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    avatar_path = Path(f"{ACCOUNT_RESOURCE_PATH}/{operator}/private")

    files = find_images(avatar_path, HEADER_IMAGE_NAME, True)
    if not files:
        raise HTTPException(status_code=404, detail="Avatar not found")
    
    return FileResponse(files[0])