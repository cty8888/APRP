from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.user import User
from app.schemas.class_schema import (
    ClassCreate, ClassUpdate, ClassResponse, ClassWithStudents, 
    JoinClassRequest, ClassSearch, StudentClassResponse
)
from app.routers.auth import get_current_user
from app.services.class_service import ClassService

router = APIRouter(prefix="/classes", tags=["班级管理"])


@router.post("/", response_model=ClassResponse, summary="教师创建班级")
async def create_class(class_data: ClassCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """教师创建新班级"""
    return ClassService.create_class(db, class_data, current_user)


@router.post("/search", response_model=List[ClassResponse], summary="搜索班级")
async def search_classes(search_data: ClassSearch,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """搜索班级（通过班级名称或班级代码）"""
    return ClassService.search_classes(db, search_data, current_user)


@router.post("/join", response_model=StudentClassResponse, summary="学生加入班级")
async def join_class(join_data: JoinClassRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """学生通过班级ID加入班级"""
    return ClassService.join_class_as_student(db, join_data, current_user)


@router.post("/join-as-teacher", response_model=dict, summary="教师加入班级")
async def join_class_as_teacher(join_data: JoinClassRequest,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """教师通过班级ID加入班级（作为助教）"""
    return ClassService.join_class_as_teacher(db, join_data, current_user)


@router.get("/my-classes", response_model=List[ClassResponse], summary="查看我的班级")
async def get_my_classes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    查看当前用户的班级列表
    教师：查看自己创建的班级 + 自己加入的班级（作为助教）
    学生：查看自己加入的班级
    """
    return ClassService.get_my_classes(db, current_user)


@router.get("/my-created-classes", response_model=List[ClassResponse], summary="查看我创建的班级")
async def get_my_created_classes(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """查看教师创建的班级（仅主教师）"""
    return ClassService.get_my_created_classes(db, current_user)


@router.get("/my-joined-classes", response_model=List[ClassResponse], summary="查看我加入的班级")
async def get_my_joined_classes(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """查看教师加入的班级（作为助教） """
    return ClassService.get_my_joined_classes(db, current_user)


@router.get("/{class_id}/students", response_model=ClassWithStudents, summary="查看班级学生")
async def get_class_students(class_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    查看指定班级的学生列表（仅教师可访问）
    """
    return ClassService.get_class_students(db, class_id, current_user)


@router.put("/{class_id}", response_model=ClassResponse, summary="更新班级")
async def update_class(class_id: int,class_data: ClassUpdate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """更新班级信息（仅创建该班级的教师可操作）"""
    return ClassService.update_class(db, class_id, class_data, current_user)


@router.delete("/{class_id}", summary="删除班级")
async def delete_class(class_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """删除班级（仅创建该班级的教师可操作）"""
    return ClassService.delete_class(db, class_id, current_user)
