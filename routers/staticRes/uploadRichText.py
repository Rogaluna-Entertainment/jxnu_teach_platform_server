from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Header
from fastapi.responses import JSONResponse
from configs import RICH_TEXT_QUOTE_PATH
from typing import List, Optional
import shutil
from utilities import verify_authorization, save_file

router = APIRouter()

@router.post("/api/uploadRichText", 
            summary="上传富文本", 
            description="将富文本上传到服务器", 
            tags=["StaticRes/RichText"])
async def upload_rich_text(
    content: str = Form(..., description="富文本内容"), 
    files: List[UploadFile] = File(..., description="富文本引用的资源")):

    # 存储上传的文件并生成URL列表
    file_urls = [await save_file(file, RICH_TEXT_QUOTE_PATH) for file in files]

    # 替换内容中的Base64 URLs为实际的文件URLs
    updated_content = await replace_content_urls(content, file_urls)

    return {"message": "Files and content processed successfully", "updated_content": updated_content}

async def replace_content_urls(content: str, file_urls: List[str]):
    # Assume we replace placeholders or specific tags in content with actual URLs
    for url in file_urls:
        content = content.replace("some_placeholder_or_base64_data", url)
    return content