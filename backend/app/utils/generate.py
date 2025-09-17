from datetime import datetime
import random
import string
from sqlalchemy.orm import Session
from app.models.class_model import Class


def generate_class_code(db: Session) -> str:
    """生成唯一的班级代码"""
    while True:
         # 生成格式：CLS + 年份后两位 + 随机6位大写字母数字
        year_suffix = str(datetime.now().year)[-2:]
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        class_code = f"CLS{year_suffix}{random_part}"
        # 检查是否已存在
        existing = db.query(Class).filter(Class.class_code == class_code).first()
        if not existing:
            return class_code