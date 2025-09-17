from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Class(Base):
    """班级表模型"""
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="班级名称")
    class_code = Column(String(20), unique=True, nullable=False, comment="班级代码")
    description = Column(String(500), nullable=True, comment="班级描述")
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="主教师ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    # 班级的主教师
    teacher = relationship("User", back_populates="created_classes")
    # 班级的教师关系（包括主教师和助教）
    teacher_classes = relationship("TeacherClass", back_populates="class_obj", cascade="all, delete-orphan")
    # 班级的学生关系
    student_classes = relationship("StudentClass", back_populates="class_obj", cascade="all, delete-orphan")
    # 班级的任务
    assignments = relationship("Assignment", back_populates="class_obj", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Class(id={self.id}, name='{self.name}', teacher_id={self.teacher_id})>"
