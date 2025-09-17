from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AssignmentCreate(BaseModel):
    """创建任务的请求模式"""
    title: str = Field(..., min_length=1, max_length=200, description="任务标题")
    description: Optional[str] = Field(None, max_length=2000, description="任务描述")
    class_id: int = Field(..., description="所属班级ID")


class AssignmentUpdate(BaseModel):
    """更新任务的请求模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="任务标题")
    description: Optional[str] = Field(None, max_length=2000, description="任务描述")


class AssignmentResponse(BaseModel):
    """任务响应模式"""
    id: int
    title: str
    description: Optional[str]
    class_id: int
    class_name: str = Field(description="所属班级名称")
    teacher_id: int
    teacher_name: str = Field(description="创建任务的教师姓名")
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


