from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import Token
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["authentication"])
# OAuth2 密码持有者
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    """获取当前用户"""
    return AuthService.get_current_user_by_token(token, db)
 
@router.post("/register", response_model=UserResponse,summary="用户注册")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    return AuthService.register_user(db, user)


@router.post("/login", response_model=Token,summary="用户登录")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """用户登录"""
    return AuthService.login_user(db, form_data.username, form_data.password)
    
@router.get("/dashboard", response_model=UserResponse,summary="获取当前用户信息")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    """获取当前用户信息"""
    return AuthService.get_user_profile(current_user)

@router.post("/refresh", response_model=Token, summary="刷新访问令牌")
async def refresh_token(current_user: Annotated[User, Depends(get_current_user)]):
    """刷新访问令牌"""
    return AuthService.refresh_user_token(current_user)

@router.post("/logout", summary="用户登出")
async def logout_user(current_user: Annotated[User, Depends(get_current_user)]):
    """用户登出"""
    return AuthService.logout_user(current_user)




