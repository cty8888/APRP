from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from jose import JWTError

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.utils.auth import (
    verify_password, 
    get_password_hash, 
    create_access_token,
    verify_token
)
from app.core.config import settings
from datetime import timedelta


class AuthService:
    """认证服务类"""
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """验证用户身份"""
        user = db.query(User).filter(User.name == username).first()
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def get_current_user_by_token(token: str, db: Session) -> User:
        """通过token获取当前用户"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = verify_token(token)
            user_id: int = int(payload.get("sub"))
            if user_id is None:
                raise credentials_exception
        except (JWTError, ValueError):
            raise credentials_exception
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        return user

    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> UserResponse:
        """用户注册"""
        # 检查用户名是否已存在
        db_user = db.query(User).filter(User.name == user_data.name).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 创建新用户
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            name=user_data.name,
            password_hash=hashed_password,
            role=user_data.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def login_user(db: Session, username: str, password: str) -> dict:
        """用户登录"""
        # 验证用户
        user = AuthService.authenticate_user(db, username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 创建访问令牌
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.name, "role": user.role.value},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    @staticmethod
    def get_user_profile(user: User) -> UserResponse:
        """获取用户信息"""
        return user

    @staticmethod
    def refresh_user_token(user: User) -> dict:
        """刷新用户令牌"""
        # 创建新的访问令牌
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.name, "role": user.role.value},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    @staticmethod
    def logout_user(user: User) -> dict:
        """用户登出"""
        # 这里可以添加 token 黑名单逻辑
        # 目前只是返回成功消息，因为 JWT 是无状态的
        return {
            "message": "Successfully logged out",
            "user_id": user.id
        }