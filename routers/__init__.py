import pkgutil
import importlib
from fastapi import APIRouter

routers = []

# 遍历当前包内所有模块
def load_routers(package):
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
        # 如果是包，则递归遍历
        if is_pkg:
            next_package = importlib.import_module(name)
            load_routers(next_package)
        else:
            # 导入模块
            module = importlib.import_module(name)
            # 检查模块是否有 router 属性
            if hasattr(module, 'router'):
                routers.append(module.router)

# 调用函数，传入当前包
load_routers(__import__(__name__))