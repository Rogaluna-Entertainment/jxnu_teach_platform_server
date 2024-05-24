from fastapi import FastAPI
from routers import routers
from configs import database
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# 设置 CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 可从中接受请求的来源列表
    allow_credentials=True, # 支持 cookies 跨域
    allow_methods=["*"],    # 允许所有方法
    allow_headers=["*"],    # 允许所有头
)


# 定义启动事件处理函数
async def connect_to_db():
    await database.connect()


# 定义关闭事件处理函数
async def close_db_connection():
    await database.disconnect()


# 注册启动和关闭事件
app.add_event_handler("startup", connect_to_db)
app.add_event_handler("shutdown", close_db_connection)


# 注册所有路由
for router in routers:
    app.include_router(router)

# uvicorn main:app --host 0.0.0.0 --port 8000 --reload        