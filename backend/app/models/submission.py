from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Float, UniqueConstraint, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Submission(Base):
    """提交表模型"""
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="学生ID")
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False, comment="任务ID")
    original_file = Column(LargeBinary, comment="原始文件内容")
    file_name = Column(Text, comment="原始文件名")
    file_json = Column(Text, comment="文件JSON数据（教师查看用）")
    report = Column(Text, comment="批改报告")
    score = Column(Float, comment="分数")
    submitted_at = Column(DateTime(timezone=True), server_default=func.now(), comment="提交时间")
    graded_at = Column(DateTime(timezone=True), comment="批改时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关系
    # 提交的学生
    student = relationship("User", back_populates="submissions")
    # 提交的任务
    assignment = relationship("Assignment", back_populates="submissions")

    # 唯一约束：一个学生对一个任务只能提交一次
    __table_args__ = (
        UniqueConstraint('student_id', 'assignment_id', name='unique_student_assignment'),
    )

    @property
    def is_graded(self):
        """判断是否已批改"""
        return self.score is not None and self.report is not None

    def __repr__(self):
        return f"<Submission(id={self.id}, student_id={self.student_id}, assignment_id={self.assignment_id}, score={self.score})>"
