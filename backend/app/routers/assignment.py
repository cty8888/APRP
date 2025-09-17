from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.user import User
from app.schemas.assignment_schema import (
    AssignmentCreate, AssignmentUpdate, AssignmentResponse
)
from app.routers.auth import get_current_user
from app.services.assignment_service import AssignmentService

router = APIRouter(prefix="/assignments", tags=["任务管理"])


@router.post("/", response_model=AssignmentResponse, summary="创建任务")
async def create_assignment(assignment_data: AssignmentCreate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """教师或助教创建任务"""
    return AssignmentService.create_assignment(db, assignment_data, current_user)


@router.get("/class/{class_id}", response_model=List[AssignmentResponse], summary="查看班级任务")
async def get_class_assignments(class_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """班级内所有成员查看指定班级的任务列表（主教师、助教、学生）"""
    return AssignmentService.get_class_assignments(db, class_id, current_user)


@router.get("/my-assignments", response_model=List[AssignmentResponse], summary="查看我创建的任务")
async def get_my_assignments(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """教师查看自己创建的任务列表"""
    return AssignmentService.get_my_assignments(db, current_user)


@router.put("/{assignment_id}", response_model=AssignmentResponse, summary="更新任务")
async def update_assignment(assignment_id: int,assignment_data: AssignmentUpdate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """更新任务内容（只有创建者可以修改）"""
    return AssignmentService.update_assignment(db, assignment_id, assignment_data, current_user)


@router.delete("/{assignment_id}", summary="删除任务")
async def delete_assignment(assignment_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """删除任务（只有创建者可以删除）"""
    return AssignmentService.delete_assignment(db, assignment_id, current_user)
