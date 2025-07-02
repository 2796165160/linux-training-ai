from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserResponse
from ..utils.security import get_current_user, get_current_active_teacher
from ..config import settings

router = APIRouter(prefix=f"{settings.API_V1_STR}/users", tags=["用户"])

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user

@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_teacher)
):
    """获取所有用户列表（仅教师可用）"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users
