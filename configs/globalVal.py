import os

SECRET_KEY = "52rr1zvg0ILSarSvZlDMS-JTn6Fq6bBXhwQP2YMDIdiNW618hQDNXnxOoOcgbnVwc1LuHR6AmukP1893_fIb3g"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = {
    "days": 0,
    "hours": 0,
    "minutes": 3000,
    "secondes": 0
} # 访问令牌过期时限

PROJECT_ROOT_PATH = 'D:\\Project\\jxnu_teach_platform\\server'

ROOT_RESOURCE_PATH = os.path.join(PROJECT_ROOT_PATH, 'resources')
ACCOUNT_RESOURCE_PATH = os.path.join(ROOT_RESOURCE_PATH, 'accounts')

HEADER_IMAGE_NAME = 'header'

IMAGE_RESOURCE_PATH = os.path.join(ROOT_RESOURCE_PATH, 'images')
VIDEO_RESOURCE_PATH = os.path.join(ROOT_RESOURCE_PATH, 'videos')
RICH_TEXT_RESOURCE_PATH = os.path.join(ROOT_RESOURCE_PATH, 'richTexts')

RICH_TEXT_QUOTE_PATH = os.path.join(RICH_TEXT_RESOURCE_PATH, 'quotes')

ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']
ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov']
