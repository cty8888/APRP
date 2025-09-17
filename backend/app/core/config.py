import os

class Settings:
    """应用配置类"""
    
    # JWT配置
    SECRET_KEY: str = "2Pn&IMvLdT*IOFXytzidFO^D^6FzBbvHr%jAr2jQj9LCOdL0OxecWtmTkYsBwhh!"
    ALGORITHM: str =  "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 数据库配置
    DATABASE_URL: str =  "sqlite:///./aprp.db"
    
    # CORS配置
    ALLOWED_ORIGINS: list = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

# 创建全局配置实例
settings = Settings()