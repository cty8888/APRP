from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from app.models.user import User
from app.models.assignment import Assignment
from app.models.class_model import Class
from app.schemas.assignment_schema import AssignmentCreate, AssignmentUpdate, AssignmentResponse
from app.utils.verify import verify_teacher_permission, verify_student_permission, verify_teacher_class_access, verify_student_class_access, verify_class_member_access


class AssignmentService:
    """任务管理服务类"""

    @staticmethod
    def create_assignment(db: Session, assignment_data: AssignmentCreate, current_user: User) -> AssignmentResponse:
        """创建任务（教师和助教都可以）"""
        # 验证教师权限
        verify_teacher_permission(current_user)
        # 验证对班级的访问权限
        verify_teacher_class_access(db, assignment_data.class_id, current_user)
        # 创建任务
        new_assignment = Assignment(
            title=assignment_data.title,
            description=assignment_data.description,
            class_id=assignment_data.class_id,
            teacher_id=current_user.id
        )
        try:
            db.add(new_assignment)
            db.commit()
            db.refresh(new_assignment)
            # 获取班级信息
            target_class = db.query(Class).filter(Class.id == new_assignment.class_id).first()
            class_name = target_class.name if target_class else "未知班级"
            
            # 构建响应
            return AssignmentResponse(
                id=new_assignment.id,
                title=new_assignment.title,
                description=new_assignment.description,
                class_id=new_assignment.class_id,
                class_name=class_name,
                teacher_id=new_assignment.teacher_id,
                teacher_name=current_user.name,
                created_at=new_assignment.created_at,
                updated_at=new_assignment.updated_at
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"创建任务失败: {str(e)}"
            )

    @staticmethod
    def get_class_assignments(db: Session, class_id: int, current_user: User) -> List[AssignmentResponse]:
        """获取班级任务列表（班级内所有成员都可以查看）"""
        # 验证用户对班级的访问权限（班级内所有成员：主教师、助教、学生）
        verify_class_member_access(db, class_id, current_user)
        # 获取班级的所有任务
        assignments = db.query(Assignment).filter(Assignment.class_id == class_id).order_by(Assignment.created_at.desc()).all()
        # 构建响应
        result = []
        for assignment in assignments:
            # 获取创建任务的教师信息
            teacher = db.query(User).filter(User.id == assignment.teacher_id).first()
            teacher_name = teacher.name if teacher else "未知教师"
            
            # 获取班级信息
            target_class = db.query(Class).filter(Class.id == assignment.class_id).first()
            class_name = target_class.name if target_class else "未知班级"
            
            result.append(AssignmentResponse(
                id=assignment.id,
                title=assignment.title,
                description=assignment.description,
                class_id=assignment.class_id,
                class_name=class_name,
                teacher_id=assignment.teacher_id,
                teacher_name=teacher_name,
                created_at=assignment.created_at,
                updated_at=assignment.updated_at
            ))
        
        return result

    @staticmethod
    def get_my_assignments(db: Session, current_user: User) -> List[AssignmentResponse]:
        """获取我创建的任务列表（教师查看）"""
        # 验证教师权限
        verify_teacher_permission(current_user)
        # 获取我创建的所有任务
        assignments = db.query(Assignment).filter(Assignment.teacher_id == current_user.id).order_by(Assignment.created_at.desc()).all()
        # 构建响应
        result = []
        for assignment in assignments:
            # 获取班级信息
            target_class = db.query(Class).filter(Class.id == assignment.class_id).first()
            class_name = target_class.name if target_class else "未知班级"
            
            result.append(AssignmentResponse(
                id=assignment.id,
                title=assignment.title,
                description=assignment.description,
                class_id=assignment.class_id,
                class_name=class_name,
                teacher_id=assignment.teacher_id,
                teacher_name=current_user.name,
                created_at=assignment.created_at,
                updated_at=assignment.updated_at
            ))
        
        return result

    @staticmethod
    def update_assignment(db: Session, assignment_id: int, assignment_data: AssignmentUpdate, current_user: User) -> AssignmentResponse:
        """更新任务（只有创建者可以修改）"""
        # 验证教师权限
        verify_teacher_permission(current_user)
        
        # 查找任务
        target_assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not target_assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务不存在"
            )
        
        # 验证是否是任务创建者
        if target_assignment.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您只能修改自己创建的任务"
            )
        
        # 检查是否有更新内容
        if not any([assignment_data.title, assignment_data.description is not None]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="请提供要更新的内容"
            )
        
        # 更新任务信息
        if assignment_data.title:
            target_assignment.title = assignment_data.title
        if assignment_data.description is not None:
            target_assignment.description = assignment_data.description
        
        try:
            db.commit()
            db.refresh(target_assignment)
            
            # 获取班级信息
            target_class = db.query(Class).filter(Class.id == target_assignment.class_id).first()
            class_name = target_class.name if target_class else "未知班级"
            
            # 构建响应
            return AssignmentResponse(
                id=target_assignment.id,
                title=target_assignment.title,
                description=target_assignment.description,
                class_id=target_assignment.class_id,
                class_name=class_name,
                teacher_id=target_assignment.teacher_id,
                teacher_name=current_user.name,
                created_at=target_assignment.created_at,
                updated_at=target_assignment.updated_at
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"更新任务失败: {str(e)}"
            )

    @staticmethod
    def delete_assignment(db: Session, assignment_id: int, current_user: User) -> dict:
        """删除任务（只有创建者可以删除）"""
        # 验证教师权限
        verify_teacher_permission(current_user)
        
        # 查找任务
        target_assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not target_assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务不存在"
            )
        
        # 验证是否是任务创建者
        if target_assignment.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您只能删除自己创建的任务"
            )
        
        try:
            # 删除任务（级联删除相关提交）
            db.delete(target_assignment)
            db.commit()
            return {"message": "任务删除成功"}
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"删除任务失败: {str(e)}"
            )
