from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.database import Base


class UserRole(str, enum.Enum):
    TEACHER = "teacher"
    STUDENT = "student"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    role = Column(Enum(UserRole), nullable=False, comment="用户角色")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    # 教师创建的班级（主教师）
    created_classes = relationship("Class", back_populates="teacher", cascade="all, delete-orphan")
    # 教师加入的班级关系（包括主教师和助教）
    teacher_classes = relationship("TeacherClass", back_populates="teacher", cascade="all, delete-orphan")
    # 教师创建的任务
    created_assignments = relationship("Assignment", foreign_keys="Assignment.teacher_id", cascade="all, delete-orphan")
    # 学生加入的班级关系
    student_classes = relationship("StudentClass", back_populates="student", cascade="all, delete-orphan")
    # 学生的提交
    submissions = relationship("Submission", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', role='{self.role}')>"
