from fastapi import APIRouter, HTTPException, status, Header
from fastapi.responses import JSONResponse
from utilities import verify_authorization

router = APIRouter()

@router.get("/api/infoDetail", 
            summary="获取单一账户基本信息", 
            description="获取单个账户的基本信息", 
            tags=["Account/Info"])
async def info_detail(authorization: str = Header(None)):  # 使用Header来要求token头部参数    
    token = verify_authorization(authorization)

    # 解算token得到登录账户id（算子）
    operator = '123'
    if operator != '123':
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # 返回信息
    return JSONResponse(content={
        'message': '登录成功',
        'content': {
            'name': '123',
            'studentId': '123456789',
            'class': '1',
            'speciality': '软件',
            'telephone': '12345',
            'email': '123456@123.com'
        }
    }, status_code=status.HTTP_200_OK)