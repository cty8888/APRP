from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class SubmissionGrade(BaseModel):
    """批改提交的请求模式"""
    score: float = Field(..., ge=0, le=100, description="分数（0-100）")
    report: str = Field(..., min_length=1, max_length=2000, description="批改报告")


class StudentSubmissionResponse(BaseModel):
    """学生提交响应模式"""
    id: int
    assignment_title: str = Field(description="任务标题")
    assignment_id: int = Field(description="任务ID")
    class_id: int = Field(description="班级ID")
    class_name: str = Field(description="班级名称")
    score: Optional[float] = Field(description="分数")
    submitted_at: datetime
    is_graded: bool = Field(description="是否已批改")
    
    class Config:
        from_attributes = True


class TeacherSubmissionResponse(BaseModel):
    """教师提交响应模式"""
    id: int
    student_id: int = Field(description="学生ID")
    student_name: str = Field(description="学生姓名")
    assignment_title: str = Field(description="任务标题")
    assignment_id: int = Field(description="任务ID")
    class_id: int = Field(description="班级ID")
    class_name: str = Field(description="班级名称")
    score: Optional[float] = Field(description="分数")
    submitted_at: datetime
    is_graded: bool = Field(description="是否已批改")
    
    class Config:
        from_attributes = True


class SubmissionBasicResponse(BaseModel):
    """提交基础响应模式（通用版，保持向后兼容）"""
    id: int
    student_name: str = Field(description="学生姓名")
    assignment_title: str = Field(description="任务标题")
    class_id: int = Field(description="班级ID")
    class_name: str = Field(description="班级名称")
    score: Optional[float] = Field(description="分数")
    submitted_at: datetime
    is_graded: bool = Field(description="是否已批改")
    
    class Config:
        from_attributes = True


class SubmissionDetailResponse(BaseModel):
    """提交详情响应模式（用于查看详情）"""
    id: int
    student_name: str = Field(description="学生姓名")
    assignment_title: str = Field(description="任务标题")
    class_id: int = Field(description="班级ID")
    class_name: str = Field(description="班级名称")
    file_json: Optional[Dict[str, Any]] = Field(description="文件JSON数据")
    report: Optional[str] = Field(description="批改报告")
    score: Optional[float] = Field(description="分数")
    submitted_at: datetime
    graded_at: Optional[datetime] = Field(description="批改时间")
    is_graded: bool = Field(description="是否已批改")
    
    class Config:
        from_attributes = True


class SubmissionCreateResponse(BaseModel):
    """提交创建响应模式（用于创建提交后返回）"""
    id: int
    assignment_title: str = Field(description="任务标题")
    submitted_at: datetime
    message: str = Field(description="提交成功消息")
    
    class Config:
        from_attributes = True



class SubmissionStatistics(BaseModel):
    """提交统计模式"""
    total_submissions: int = Field(description="总提交数")
    graded_submissions: int = Field(description="已批改数")
    ungraded_submissions: int = Field(description="未批改数")
    average_score: Optional[float] = Field(description="平均分")
    highest_score: Optional[float] = Field(description="最高分")
    lowest_score: Optional[float] = Field(description="最低分")




class PendingAssignmentResponse(BaseModel):
    """待提交任务响应模式"""
    id: int
    title: str = Field(description="任务标题")
    description: Optional[str] = Field(description="任务描述")
    class_id: int = Field(description="班级ID")
    class_name: str = Field(description="班级名称")
    teacher_name: str = Field(description="教师姓名")
    created_at: datetime
    deadline: Optional[datetime] = Field(description="截止时间")
    
    class Config:
        from_attributes = True
