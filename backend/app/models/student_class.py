from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class StudentClass(Base):
    """学生-班级关系表模型"""
    __tablename__ = "student_classes"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="学生ID")
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False, comment="班级ID")
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), comment="加入时间")

    # 关系
    # 学生
    student = relationship("User", back_populates="student_classes")
    # 班级
    class_obj = relationship("Class", back_populates="student_classes")

    # 唯一约束：一个学生只能加入一个班级一次
    __table_args__ = (
        UniqueConstraint('student_id', 'class_id', name='unique_student_class'),
    )

    def __repr__(self):
        return f"<StudentClass(id={self.id}, student_id={self.student_id}, class_id={self.class_id})>"
