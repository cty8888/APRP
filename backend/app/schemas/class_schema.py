from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ClassCreate(BaseModel):
    """创建班级的请求模式"""
    name: str = Field(..., min_length=1, max_length=100, description="班级名称")
    description: Optional[str] = Field(None, max_length=500, description="班级描述")


class ClassUpdate(BaseModel):
    """更新班级的请求模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="班级名称")
    description: Optional[str] = Field(None, max_length=500, description="班级描述")


class ClassResponse(BaseModel):
    """班级响应模式"""
    id: int
    name: str
    class_code: str = Field(description="班级代码")
    description: Optional[str] = Field(description="班级描述")
    teacher_id: int
    teacher_name: str = Field(description="主教师姓名")
    created_at: datetime
    updated_at: datetime
    student_count: int = Field(default=0, description="学生数量")
    my_role: str = Field(description="我在这个班级的角色: main_teacher/assistant_teacher/student")
    
    class Config:
        from_attributes = True


class ClassWithStudents(BaseModel):
    """包含学生信息的班级响应模式"""
    id: int
    name: str
    teacher_id: int
    created_at: datetime
    updated_at: datetime
    student_count: int = Field(description="学生数量")
    students: List[dict] = Field(description="学生列表")
    
    class Config:
        from_attributes = True


class JoinClassRequest(BaseModel):
    """加入班级的请求模式"""
    class_id: int = Field(..., description="班级ID")


class ClassSearch(BaseModel):
    """搜索班级的请求模式"""
    search_term: str = Field(..., min_length=1, max_length=100, description="搜索关键词（班级名称或班级代码）")


class StudentClassResponse(BaseModel):
    """学生-班级关系响应模式"""
    id: int
    student_id: int
    class_id: int
    joined_at: datetime
    
    class Config:
        from_attributes = True

