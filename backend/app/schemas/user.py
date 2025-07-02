from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

# 基础用户模式
class UserBase(BaseModel):
    username: str
    email: EmailStr

# 创建用户
class UserCreate(UserBase):
    password: str
    role: str
    full_name: Optional[str] = None
    school: Optional[str] = None
    college: Optional[str] = None
    major: Optional[str] = None
    class_name: Optional[str] = None
    student_id: Optional[str] = None
    
    @validator('role')
    def validate_role(cls, v):
        if v not in ["student", "teacher"]:
            raise ValueError("角色必须是'student'或'teacher'")
        return v
    
    @validator('password')
    def password_complexity(cls, v):
        if len(v) < 6:
            raise ValueError("密码长度至少为6位")
        return v

# 用户登录
class UserLogin(BaseModel):
    username: str
    password: str

# 用户信息更新
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    school: Optional[str] = None
    college: Optional[str] = None
    major: Optional[str] = None
    class_name: Optional[str] = None
    student_id: Optional[str] = None
    avatar: Optional[str] = None

# 用户响应
class UserResponse(UserBase):
    id: int
    role: str
    full_name: Optional[str] = None
    school: Optional[str] = None
    college: Optional[str] = None
    major: Optional[str] = None
    class_name: Optional[str] = None
    student_id: Optional[str] = None
    avatar: Optional[str] = None
    created_at: datetime
    
    class Config:
        orm_mode = True

# JWT令牌
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
