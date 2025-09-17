from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.database import Base


class TeacherRole(str, enum.Enum):
    """教师角色枚举"""
    MAIN_TEACHER = "main_teacher"  # 主教师
    ASSISTANT_TEACHER = "assistant_teacher"  # 助教


class TeacherClass(Base):
    """教师-班级关系表模型"""
    __tablename__ = "teacher_classes"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="教师ID")
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False, comment="班级ID")
    role = Column(Enum(TeacherRole), nullable=False, comment="教师角色")
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), comment="加入时间")

    # 关系
    # 教师
    teacher = relationship("User", back_populates="teacher_classes")
    # 班级
    class_obj = relationship("Class", back_populates="teacher_classes")

    # 唯一约束：一个教师只能加入一个班级一次
    __table_args__ = (
        UniqueConstraint('teacher_id', 'class_id', name='unique_teacher_class'),
    )

    def __repr__(self):
        return f"<TeacherClass(id={self.id}, teacher_id={self.teacher_id}, class_id={self.class_id}, role='{self.role}')>"
