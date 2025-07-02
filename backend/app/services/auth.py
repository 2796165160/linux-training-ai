from typing import Optional
from sqlalchemy.orm import Session

from ..models.user import User
from ..utils.security import verify_password, get_password_hash

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """验证用户"""
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_user(db: Session, user_data: dict) -> User:
    """创建用户"""
    hashed_password = get_password_hash(user_data["password"])
    
    # 创建用户对象，包含所有提交的字段
    user = User(
        username=user_data["username"],
        email=user_data["email"],
        hashed_password=hashed_password,
        role=user_data["role"],
        full_name=user_data.get("full_name"),
        school=user_data.get("school"),
        college=user_data.get("college"),
        major=user_data.get("major"),
        class_name=user_data.get("class_name"),
        student_id=user_data.get("student_id")
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

