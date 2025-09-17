from fastapi import HTTPException, status
from app.models.user import User
from app.models.class_model import Class
from app.models.teacher_class import TeacherClass
from app.models.student_class import StudentClass
from sqlalchemy.orm import Session

def verify_teacher_permission(current_user: User):
    """验证教师权限"""
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有教师可以执行此操作"
        )


def verify_student_permission(current_user: User):
    """验证学生权限"""
    if current_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有学生可以执行此操作"
        )

def verify_teacher_class_access(db: Session, class_id: int, current_user: User) -> None:
    """验证教师对班级的访问权限（主教师或助教）"""
    # 检查班级是否存在
    target_class = db.query(Class).filter(Class.id == class_id).first()
    if not target_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="班级不存在"
        )
        
    # 检查是否是主教师
    if target_class.teacher_id == current_user.id:
        return  # 主教师有权限
        
    # 检查是否是助教
    teacher_relation = db.query(TeacherClass).filter(
        TeacherClass.teacher_id == current_user.id,
        TeacherClass.class_id == class_id
    ).first()
        
    if not teacher_relation:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有权限在此班级创建任务"
        )

def verify_student_class_access(db: Session, class_id: int, current_user: User) -> None:
    """验证学生对班级的访问权限（已加入班级）"""
    # 检查学生是否已加入该班级
    student_relation = db.query(StudentClass).filter(
        StudentClass.student_id == current_user.id,
        StudentClass.class_id == class_id
    ).first()
        
    if not student_relation:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您需要先加入该班级才能查看任务"
        )

def verify_class_member_access(db: Session, class_id: int, current_user: User) -> None:
    """验证用户对班级的访问权限（班级内所有成员：主教师、助教、学生）"""
    # 检查班级是否存在
    target_class = db.query(Class).filter(Class.id == class_id).first()
    if not target_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="班级不存在"
        )
    
    # 检查是否是主教师
    if target_class.teacher_id == current_user.id:
        return  # 主教师有权限
    
    # 检查是否是助教
    teacher_relation = db.query(TeacherClass).filter(
        TeacherClass.teacher_id == current_user.id,
        TeacherClass.class_id == class_id
    ).first()
    if teacher_relation:
        return  # 助教有权限
    
    # 检查是否是学生
    student_relation = db.query(StudentClass).filter(
        StudentClass.student_id == current_user.id,
        StudentClass.class_id == class_id
    ).first()
    if student_relation:
        return  # 学生有权限
    
    # 如果都不是，则没有权限
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="您不是该班级的成员，无法查看班级任务"
    )