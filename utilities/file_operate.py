# utilities/file_utils.py
from pathlib import Path
import os
import uuid
import shutil
from fastapi import HTTPException

def get_file_extension(filename: str) -> str:
    """
    Returns the file extension of a given filename.
    
    Args:
    - filename (str): The name of the file.

    Returns:
    - str: The extension of the file, including the leading period, or an empty string if the file has no extension.
    """
    return Path(filename).suffix


def save_file(upload_file, storage_directory, allowed_extensions=None):
    # 获取文件扩展名并检查是否允许
    file_extension = get_file_extension(upload_file.filename)
    if allowed_extensions is not None:
        if file_extension not in allowed_extensions:
            raise HTTPException(status_code=400, detail="格式非法")

    # 生成唯一文件名
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    # 确保存储目录存在
    os.makedirs(storage_directory, exist_ok=True)

    # 保存文件
    file_path = os.path.join(storage_directory, unique_filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    # 返回存档的文件名
    return unique_filename