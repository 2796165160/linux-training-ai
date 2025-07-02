import os
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 基本配置
    PROJECT_NAME: str = "AI实训报告生成系统"
    API_V1_STR: str = "/api"
    DEBUG: bool = True
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 模板文件存储路径
    TEMPLATE_DIR: str = "/home/ai_report_system/templates/docx"

    # 数据库配置
    POSTGRES_SERVER: str = os.environ.get("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER", "cc")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD", "123456")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB", "ai_report_system")
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    
    # JWT认证配置
    JWT_SECRET: str = os.environ.get("JWT_SECRET", "YOUR_SECRET_KEY_HERE")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 天
    
    # 通义千问API配置
    QWEN_API_KEY: str = os.environ.get("QWEN_API_KEY", "sk-68d5ae53963644de917adc922a07e95e")
    QWEN_API_URL: str = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    
    # CORS配置
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"

settings = Settings()
