# 导入所有模式
from .user import UserCreate, UserLogin, UserResponse
from .auth import Token, TokenData
from .class_schema import (
    ClassCreate, ClassUpdate, ClassResponse, ClassWithStudents, 
    JoinClassRequest, ClassSearch, StudentClassResponse
)

__all__ = [
    "UserCreate", "UserLogin", "UserResponse", "Token", "TokenData",
    "ClassCreate", "ClassUpdate", "ClassResponse", "ClassWithStudents", 
    "JoinClassRequest", "ClassSearch", "StudentClassResponse"
]
