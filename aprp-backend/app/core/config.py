from pydantic_settings import BaseSettings

#定义配置类，会生成Conifg类对应的相关对象
class Settings(BaseSettings):
    # 数据库配置 
    database_url: str = "sqlite:///./aprp.db"
    
    class Config: #用来告诉Pydantic从哪个文件加载相关配置
        env_file = ".env"


settings = Settings()
