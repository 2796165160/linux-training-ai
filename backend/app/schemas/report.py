from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 创建报告
class ReportCreate(BaseModel):
    task_id: int
    template_id: Optional[int] = None

# 更新报告
class ReportUpdate(BaseModel):
    content: str

# 报告响应
class ReportResponse(BaseModel):
    id: int
    title: str
    content: str
    task_id: int
    user_id: int
    template_id: Optional[int]
    created_at: datetime
    
    class Config:
        orm_mode = True
