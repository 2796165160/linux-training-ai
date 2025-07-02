from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 创建模板
class TemplateCreate(BaseModel):
    name: str
    content: str

# 模板响应
class TemplateResponse(BaseModel):
    id: int
    name: str
    content: str
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
