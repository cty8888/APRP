from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    """用户基础模式"""
    name: str
    role: UserRole


class UserCreate(UserBase):
    """用户注册模式"""
    password: str


class UserLogin(BaseModel):
    """用户登录模式"""
    name: str
    password: str


class UserResponse(UserBase):
    """用户响应模式"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserInDB(UserResponse):
    """数据库中的用户模式（包含密码哈希）"""
    password_hash: str
