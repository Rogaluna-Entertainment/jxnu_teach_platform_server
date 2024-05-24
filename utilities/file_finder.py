from pathlib import Path
from typing import List
from configs import ALLOWED_IMAGE_EXTENSIONS

def find_images(image_dir: str, image_name: str, first_only: bool = False) -> List[Path]:
    image_directory = Path(image_dir)
    found_files = []

    for ext in ALLOWED_IMAGE_EXTENSIONS:
        possible_file = image_directory / f"{image_name}.{ext}"
        if possible_file.is_file():
            if first_only:
                return [possible_file]  # 立即返回找到的第一个文件的列表
            found_files.append(possible_file)

    return found_files  # 返回所有找到的文件列表