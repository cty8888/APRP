from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Assignment(Base):
    """任务表模型"""
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="任务标题")
    description = Column(Text, comment="任务描述")
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False, comment="所属班级ID")
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="创建任务的教师ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    # 任务所属的班级
    class_obj = relationship("Class", back_populates="assignments")
    # 创建任务的教师
    teacher = relationship("User", foreign_keys=[teacher_id], overlaps="created_assignments")
    # 任务的提交
    submissions = relationship("Submission", back_populates="assignment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Assignment(id={self.id}, title='{self.title}', class_id={self.class_id})>"
