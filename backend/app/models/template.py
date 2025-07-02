from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
import datetime


from ..database import Base

class Template(Base):
    __tablename__ = "templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # 新增字段
    file_path = Column(String(255), nullable=True)  # 存储文件路径
    original_filename = Column(String(255), nullable=True)  # 原始文件名
    is_docx = Column(Boolean, default=False)  # 是否为DOCX模板
    
    # 关系
    user = relationship("User", back_populates="templates")
    reports = relationship("Report", back_populates="template")
