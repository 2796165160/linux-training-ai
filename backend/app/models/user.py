from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
import datetime

from ..database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)  # "student" or "teacher"

    # 新增用户个人信息字段
    full_name = Column(String(100))  # 姓名
    school = Column(String(100))  # 学校
    college = Column(String(100))  # 学院
    major = Column(String(100))  # 专业
    class_name = Column(String(50))  # 班级
    student_id = Column(String(50))  # 学号
    avatar = Column(String(200))  # 头像URL 


    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # 关系
    tasks = relationship("Task", back_populates="user")
    reports = relationship("Report", back_populates="user")
    templates = relationship("Template", back_populates="user")
