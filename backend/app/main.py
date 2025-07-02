import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os

# 添加父目录到路径以方便导入
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .config import settings
from .database import Base, engine, check_db_connection
from .routers import auth, users, tasks, templates, reports

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log"),
    ]
)

logger = logging.getLogger(__name__)

# 检查数据库连接
if not check_db_connection():
    logger.error("数据库连接失败，应用将退出")
    sys.exit(1)

# 创建表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI实训报告生成系统 API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(templates.router)
app.include_router(reports.router)

@app.get("/")
async def root():
    return {"message": f"欢迎使用{settings.PROJECT_NAME} API"}

@app.get("/health")
async def health_check():
    """健康检查"""
    if not check_db_connection():
        raise HTTPException(status_code=500, detail="数据库连接失败")
    return {"status": "healthy"}


@app.get("/api/config-test")
async def config_test():
    """测试配置是否正确加载"""
    return {
        "TEMPLATE_DIR": settings.TEMPLATE_DIR if hasattr(settings, "TEMPLATE_DIR") else "NOT SET",
        "API_V1_STR": settings.API_V1_STR,
        "PROJECT_NAME": settings.PROJECT_NAME
    }
    
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
