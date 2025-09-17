from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from app.models.user import User
from app.models.class_model import Class
from app.models.student_class import StudentClass
from app.models.teacher_class import TeacherClass, TeacherRole
from app.schemas.class_schema import (
    ClassCreate, ClassUpdate, ClassResponse, ClassWithStudents, 
    ClassSearch, StudentClassResponse, JoinClassRequest
)
from app.utils.verify import verify_teacher_permission, verify_student_permission
from app.utils.generate import generate_class_code

class ClassService:
    """班级管理服务类"""
    @staticmethod
    def create_class(db: Session, class_data: ClassCreate, current_user: User) -> ClassResponse:
        """教师创建新班级"""
        # 验证教师权限
        verify_teacher_permission(current_user)
        
        # 检查同一教师下班级名称是否已存在
        existing_class = db.query(Class).filter(
            Class.name == class_data.name,
            Class.teacher_id == current_user.id
        ).first()
        if existing_class:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="您已经创建了同名的班级，请使用其他名称"
            )
        
        # 生成唯一的班级代码
        class_code = generate_class_code(db)
        
        # 创建新班级
        new_class = Class(
            name=class_data.name,
            class_code=class_code,
            description=class_data.description,
            teacher_id=current_user.id
        )
        try:
            db.add(new_class)
            db.commit()
            db.refresh(new_class)
            
            # 构建完整响应
            teacher_name = current_user.name
            student_count = 0  # 新创建的班级没有学生
            
            return ClassResponse(
                id=new_class.id,
                name=new_class.name,
                class_code=new_class.class_code,
                description=new_class.description,
                teacher_id=new_class.teacher_id,
                teacher_name=teacher_name,
                created_at=new_class.created_at,
                updated_at=new_class.updated_at,
                student_count=student_count,
                my_role="main_teacher"
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"创建班级失败: {str(e)}"
            )

    @staticmethod
    def search_classes(db: Session, search_data: ClassSearch, current_user: User) -> List[ClassResponse]:
        """搜索班级"""
        search_term = search_data.search_term.strip()
        
        # 搜索班级（支持班级名称和班级代码的模糊搜索）
        classes = db.query(Class).filter(
            (Class.name.ilike(f"%{search_term}%")) |
            (Class.class_code.ilike(f"%{search_term}%"))
        ).limit(20).all()  # 限制返回数量
        # 构建响应
        result = []
        for cls in classes:
            # 获取主教师信息
            teacher = db.query(User).filter(User.id == cls.teacher_id).first()
            teacher_name = teacher.name if teacher else "未知教师"
            
            # 获取学生数量
            student_count = db.query(StudentClass).filter(StudentClass.class_id == cls.id).count()
            
            # 确定用户是否已加入这个班级
            my_role = "none"
            if current_user.role == "student":
                student_relation = db.query(StudentClass).filter(
                    StudentClass.student_id == current_user.id,
                    StudentClass.class_id == cls.id
                ).first()
                if student_relation:
                    my_role = "student"
            elif current_user.role == "teacher":
                if cls.teacher_id == current_user.id:
                    my_role = "main_teacher"
                else:
                    teacher_relation = db.query(TeacherClass).filter(
                        TeacherClass.teacher_id == current_user.id,
                        TeacherClass.class_id == cls.id
                    ).first()
                    if teacher_relation:
                        my_role = "assistant_teacher"
            
            result.append(ClassResponse(
                id=cls.id,
                name=cls.name,
                class_code=cls.class_code,
                description=cls.description,
                teacher_id=cls.teacher_id,
                teacher_name=teacher_name,
                created_at=cls.created_at,
                updated_at=cls.updated_at,
                student_count=student_count,
                my_role=my_role
            ))
        
        return result

    @staticmethod
    def join_class_as_student(db: Session, 
    join_data: JoinClassRequest, current_user: User) -> StudentClassResponse:
        """学生加入班级"""
        # 验证学生权限
        verify_student_permission(current_user)
        # 查找班级
        target_class = db.query(Class).filter(Class.id == join_data.class_id).first()
        if not target_class:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="班级不存在"
            )
        
        # 检查是否已经加入该班级
        existing_relation = db.query(StudentClass).filter(
            StudentClass.student_id == current_user.id,
            StudentClass.class_id == join_data.class_id
        ).first()
        
        if existing_relation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="您已经加入该班级"
            )
        
        # 创建学生-班级关系
        new_relation = StudentClass(
            student_id=current_user.id,
            class_id=join_data.class_id
        )
        
        try:
            db.add(new_relation)
            db.commit()
            db.refresh(new_relation)
            return new_relation
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"加入班级失败: {str(e)}"
            )

    @staticmethod
    def join_class_as_teacher(db: Session, join_data: JoinClassRequest, current_user: User) -> dict:
        """教师加入班级（作为助教）"""
        # 验证教师权限
        verify_teacher_permission(current_user)
        
        # 查找班级
        target_class = db.query(Class).filter(Class.id == join_data.class_id).first()
        if not target_class:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="班级不存在"
            )
        
        # 检查是否已经加入该班级
        existing_relation = db.query(TeacherClass).filter(
            TeacherClass.teacher_id == current_user.id,
            TeacherClass.class_id == join_data.class_id
        ).first()
        
        if existing_relation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="您已经加入该班级"
            )
        
        # 检查是否是班级创建者（主教师）
        if target_class.teacher_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="您是班级创建者，无需重复加入"
            )
        
        # 创建教师-班级关系（作为助教）
        new_relation = TeacherClass(
            teacher_id=current_user.id,
            class_id=join_data.class_id,
            role=TeacherRole.ASSISTANT_TEACHER
        )
        
        try:
            db.add(new_relation)
            db.commit()
            db.refresh(new_relation)
            return {
                "message": "成功加入班级",
                "class_name": target_class.name,
                "role": "assistant_teacher"
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"加入班级失败: {str(e)}"
            )

    @staticmethod
    def get_my_classes(db: Session, current_user: User) -> List[ClassResponse]:
        """查看当前用户的班级列表"""
        if current_user.role == "teacher":
            # 教师查看自己创建的班级（作为主教师）
            created_classes = db.query(Class).filter(Class.teacher_id == current_user.id).all()
            
            # 教师查看自己加入的班级（作为助教）
            joined_classes = db.query(Class).join(TeacherClass).filter(
                TeacherClass.teacher_id == current_user.id
            ).all()
            
            # 合并并去重（避免主教师重复显示自己创建的班级）
            all_classes = created_classes + joined_classes
            unique_classes = []
            seen_ids = set()
            for cls in all_classes:
                if cls.id not in seen_ids:
                    unique_classes.append(cls)
                    seen_ids.add(cls.id)
            
            classes = unique_classes
        elif current_user.role == "student":
            # 学生查看自己加入的班级
            classes = db.query(Class).join(StudentClass).filter(StudentClass.student_id == current_user.id).all()
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无效的用户角色"
            )
        
        # 构建完整的响应数据
        result = []
        for cls in classes:
            # 获取主教师信息
            teacher = db.query(User).filter(User.id == cls.teacher_id).first()
            teacher_name = teacher.name if teacher else "未知教师"
            
            # 获取学生数量
            student_count = db.query(StudentClass).filter(StudentClass.class_id == cls.id).count()
            
            # 确定用户在这个班级的角色
            my_role = "student" if current_user.role == "student" else "main_teacher"
            if current_user.role == "teacher" and cls.teacher_id != current_user.id:
                # 检查是否是助教
                teacher_relation = db.query(TeacherClass).filter(
                    TeacherClass.teacher_id == current_user.id,
                    TeacherClass.class_id == cls.id
                ).first()
                if teacher_relation:
                    my_role = "assistant_teacher"
            
            result.append(ClassResponse(
                id=cls.id,
                name=cls.name,
                class_code=cls.class_code,
                description=cls.description,
                teacher_id=cls.teacher_id,
                teacher_name=teacher_name,
                created_at=cls.created_at,
                updated_at=cls.updated_at,
                student_count=student_count,
                my_role=my_role
            ))
        
        return result

    @staticmethod
    def get_my_created_classes(db: Session, current_user: User) -> List[ClassResponse]:
        """查看教师创建的班级（仅主教师）"""
        verify_teacher_permission(current_user)
        
        # 教师查看自己创建的班级（作为主教师）
        classes = db.query(Class).filter(Class.teacher_id == current_user.id).all()
        
        # 构建完整的响应数据
        result = []
        for cls in classes:
            # 获取学生数量
            student_count = db.query(StudentClass).filter(StudentClass.class_id == cls.id).count()
            
            result.append(ClassResponse(
                id=cls.id,
                name=cls.name,
                class_code=cls.class_code,
                description=cls.description,
                teacher_id=cls.teacher_id,
                teacher_name=current_user.name,
                created_at=cls.created_at,
                updated_at=cls.updated_at,
                student_count=student_count,
                my_role="main_teacher"
            ))
        
        return result

    @staticmethod
    def get_my_joined_classes(db: Session, current_user: User) -> List[ClassResponse]:
        """查看教师加入的班级（作为助教）"""
        verify_teacher_permission(current_user)
        
        # 教师查看自己加入的班级（作为助教）
        classes = db.query(Class).join(TeacherClass).filter(TeacherClass.teacher_id == current_user.id).all()
        
        # 构建完整的响应数据
        result = []
        for cls in classes:
            # 获取主教师信息
            teacher = db.query(User).filter(User.id == cls.teacher_id).first()
            teacher_name = teacher.name if teacher else "未知教师"
            
            # 获取学生数量
            student_count = db.query(StudentClass).filter(StudentClass.class_id == cls.id).count()
            
            result.append(ClassResponse(
                id=cls.id,
                name=cls.name,
                class_code=cls.class_code,
                description=cls.description,
                teacher_id=cls.teacher_id,
                teacher_name=teacher_name,
                created_at=cls.created_at,
                updated_at=cls.updated_at,
                student_count=student_count,
                my_role="assistant_teacher"
            ))
        
        return result


    @staticmethod
    def get_class_students(db: Session, class_id: int, current_user: User) -> ClassWithStudents:
        """查看指定班级的学生列表（仅教师可访问）"""
        # 验证教师权限
        verify_teacher_permission(current_user)
        
        # 查找班级并验证权限
        target_class = db.query(Class).filter(Class.id == class_id).first()
        if not target_class:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="班级不存在"
            )
        
        if target_class.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您只能查看自己创建的班级"
            )
        
        # 获取班级学生信息
        student_relations = db.query(StudentClass).filter(
            StudentClass.class_id == class_id
        ).all()
        
        students = []
        for relation in student_relations:
            student = db.query(User).filter(User.id == relation.student_id).first()
            if student:
                students.append({
                    "id": student.id,
                    "name": student.name,
                    "joined_at": relation.joined_at
                })
        
        return ClassWithStudents(
            id=target_class.id,
            name=target_class.name,
            teacher_id=target_class.teacher_id,
            created_at=target_class.created_at,
            updated_at=target_class.updated_at,
            student_count=len(students),
            students=students
        )

    @staticmethod
    def update_class(db: Session, class_id: int, class_data: ClassUpdate, current_user: User) -> ClassResponse:
        """更新班级信息（仅创建该班级的教师可操作）"""
        # 验证教师权限
        verify_teacher_permission(current_user)
        
        # 查找班级并验证权限
        target_class = db.query(Class).filter(Class.id == class_id).first()
        if not target_class:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="班级不存在"
            )
        
        if target_class.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您只能更新自己创建的班级"
            )
        
        # 检查是否有更新内容
        if not any([class_data.name, class_data.description is not None]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="请提供要更新的内容"
            )
        
        # 如果要更新名称，检查同一教师下班级名称是否已存在
        if class_data.name and class_data.name != target_class.name:
            existing_class = db.query(Class).filter(
                Class.name == class_data.name,
                Class.teacher_id == current_user.id,
                Class.id != class_id
            ).first()
            if existing_class:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="您已经创建了同名的班级，请使用其他名称"
                )
        
        # 更新班级信息
        if class_data.name:
            target_class.name = class_data.name
        if class_data.description is not None:
            target_class.description = class_data.description
        
        try:
            db.commit()
            db.refresh(target_class)
            
            # 构建完整响应
            teacher = db.query(User).filter(User.id == target_class.teacher_id).first()
            teacher_name = teacher.name if teacher else "未知教师"
            student_count = db.query(StudentClass).filter(StudentClass.class_id == target_class.id).count()
            
            return ClassResponse(
                id=target_class.id,
                name=target_class.name,
                class_code=target_class.class_code,
                description=target_class.description,
                teacher_id=target_class.teacher_id,
                teacher_name=teacher_name,
                created_at=target_class.created_at,
                updated_at=target_class.updated_at,
                student_count=student_count,
                my_role="main_teacher"
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"更新班级失败: {str(e)}"
            )

    @staticmethod
    def delete_class(db: Session, class_id: int, current_user: User) -> dict:
        """删除班级（仅创建该班级的教师可操作）"""
        # 验证教师权限
        verify_teacher_permission(current_user)
        
        # 查找班级并验证权限
        target_class = db.query(Class).filter(Class.id == class_id).first()
        if not target_class:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="班级不存在"
            )
        
        if target_class.teacher_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您只能删除自己创建的班级"
            )
        
        try:
            # 删除班级（级联删除相关关系）
            db.delete(target_class)
            db.commit()
            return {"message": "班级删除成功"}
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"删除班级失败: {str(e)}"
            )
