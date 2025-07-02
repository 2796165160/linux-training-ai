from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 创建任务
class TaskCreate(BaseModel):
    title: str
    description: str

# 任务响应
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
