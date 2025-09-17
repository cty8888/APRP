from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """JWT Token 模式"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token 数据模式"""
    user_id: Optional[int] = None
    username: Optional[str] = None
    role: Optional[str] = None
