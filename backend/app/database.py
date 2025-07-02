from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

from .config import settings

logger = logging.getLogger(__name__)

# 创建数据库引擎
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True  # 自动检测连接是否有效
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 检查数据库连接
def check_db_connection():
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"数据库连接成功! 已有表: {tables}")
        return True
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        return False
