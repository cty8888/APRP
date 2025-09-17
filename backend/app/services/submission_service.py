from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile, Response
from typing import List
from sqlalchemy import func
from io import BytesIO
from app.models.student_class import StudentClass
from app.models.user import User
from app.models.class_model import Class
from app.models.assignment import Assignment
from app.models.submission import Submission
from app.schemas.submission_schema import (
    SubmissionGrade, 
    SubmissionDetailResponse, SubmissionCreateResponse, SubmissionStatistics,
    StudentSubmissionResponse, TeacherSubmissionResponse, PendingAssignmentResponse
)
from app.utils.verify import verify_student_permission, verify_teacher_permission, verify_class_member_access
from app.utils.parser_utils import parse_docx


class SubmissionService:
    """提交管理服务类"""

    @staticmethod
    def get_my_submissions(db: Session, current_user: User) -> List[StudentSubmissionResponse]:
        """学生查看自己的提交列表"""
        # 验证学生权限
        verify_student_permission(current_user)
        
        # 获取学生的所有提交
        submissions = db.query(Submission).filter(
            Submission.student_id == current_user.id
        ).order_by(Submission.submitted_at.desc()).all()
        
        # 构建响应
        result = []
        for submission in submissions:
            # 获取任务信息
            assignment = db.query(Assignment).filter(Assignment.id == submission.assignment_id).first()
            assignment_title = assignment.title if assignment else "未知任务"
            
            # 获取班级信息
            class_obj = db.query(Class).filter(Class.id == assignment.class_id).first() if assignment else None
            class_id = class_obj.id if class_obj else 0
            class_name = class_obj.name if class_obj else "未知班级"
            
            result.append(StudentSubmissionResponse(
                id=submission.id,
                assignment_title=assignment_title,
                assignment_id=submission.assignment_id,
                class_id=class_id,
                class_name=class_name,
                score=submission.score,
                submitted_at=submission.submitted_at,
                is_graded=submission.is_graded
            ))
        
        return result

    @staticmethod
    def create_submission_with_file(db: Session, assignment_id: int, file: UploadFile, current_user: User) -> SubmissionCreateResponse:
        """学生通过文件上传提交文档"""
        # 验证学生权限
        verify_student_permission(current_user)
        
        # 验证文件格式
        if not file.filename.endswith(".docx"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="目前只支持docx文件"
            )
        
        # 查找任务
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务不存在"
            )
        
        # 验证学生是否在任务所属的班级中
        verify_class_member_access(db, assignment.class_id, current_user)
        
        # 读取并解析文件
        try:
            content = file.file.read()
            file_obj = BytesIO(content)
            file_json = parse_docx(file_obj)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"文件解析失败: {str(e)}"
            )
        
        # 检查是否已经提交过（重复提交覆盖）
        existing_submission = db.query(Submission).filter(
            Submission.student_id == current_user.id,
            Submission.assignment_id == assignment_id
        ).first()
        
        if existing_submission:
            # 更新现有提交（更新原始文件和解析数据，保留批改信息）
            existing_submission.original_file = content
            existing_submission.file_name = file.filename
            existing_submission.file_json = file_json
            
            try:
                db.commit()
                db.refresh(existing_submission)
                submission = existing_submission
            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"更新提交失败: {str(e)}"
                )
        else:
            # 创建新提交
            new_submission = Submission(
                student_id=current_user.id,
                assignment_id=assignment_id,
                original_file=content,
                file_name=file.filename,
                file_json=file_json
            )
            
            try:
                db.add(new_submission)
                db.commit()
                db.refresh(new_submission)
                submission = new_submission
            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"创建提交失败: {str(e)}"
                )
        
        # 构建响应
        return SubmissionCreateResponse(
            id=submission.id,
            assignment_title=assignment.title,
            submitted_at=submission.submitted_at,
            message="提交成功" if not existing_submission else "提交已更新"
        )

    @staticmethod
    def get_assignment_submissions(db: Session, assignment_id: int, current_user: User) -> List[TeacherSubmissionResponse]:
        """教师查看指定任务的提交列表"""
        # 验证教师权限
        verify_teacher_permission(current_user)
        
        # 查找任务
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务不存在"
            )
        
        # 验证教师对班级的访问权限
        verify_class_member_access(db, assignment.class_id, current_user)
        
        # 获取任务的所有提交
        submissions = db.query(Submission).filter(
            Submission.assignment_id == assignment_id
        ).order_by(Submission.submitted_at.desc()).all()
        
        # 获取班级信息
        class_obj = db.query(Class).filter(Class.id == assignment.class_id).first()
        class_id = class_obj.id if class_obj else 0
        class_name = class_obj.name if class_obj else "未知班级"
        
        # 构建响应
        result = []
        for submission in submissions:
            # 获取学生信息
            student = db.query(User).filter(User.id == submission.student_id).first()
            student_name = student.name if student else "未知学生"
            
            result.append(TeacherSubmissionResponse(
                id=submission.id,
                student_id=submission.student_id,
                student_name=student_name,
                assignment_title=assignment.title,
                assignment_id=submission.assignment_id,
                class_id=class_id,
                class_name=class_name,
                score=submission.score,
                submitted_at=submission.submitted_at,
                is_graded=submission.is_graded
            ))
        
        return result

    @staticmethod
    def get_submission_detail(db: Session, submission_id: int, current_user: User) -> SubmissionDetailResponse:
        """获取提交详情"""
        # 查找提交
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="提交不存在"
            )
        
        # 获取任务信息
        assignment = db.query(Assignment).filter(Assignment.id == submission.assignment_id).first()
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务不存在"
            )
        
        # 验证权限：学生只能查看自己的提交，教师可以查看班级内的所有提交
        if current_user.role == "student":
            if submission.student_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="您只能查看自己的提交"
                )
        elif current_user.role == "teacher":
            verify_class_member_access(db, assignment.class_id, current_user)
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无效的用户角色"
            )
        
        # 获取学生信息
        student = db.query(User).filter(User.id == submission.student_id).first()
        student_name = student.name if student else "未知学生"
        
        # 获取班级信息
        from app.models.class_model import Class
        class_obj = db.query(Class).filter(Class.id == assignment.class_id).first()
        class_id = class_obj.id if class_obj else 0
        class_name = class_obj.name if class_obj else "未知班级"
        
        # 构建响应
        return SubmissionDetailResponse(
            id=submission.id,
            student_name=student_name,
            assignment_title=assignment.title,
            class_id=class_id,
            class_name=class_name,
            file_json=submission.file_json,
            report=submission.report,
            score=submission.score,
            submitted_at=submission.submitted_at,
            graded_at=submission.graded_at,
            is_graded=submission.is_graded
        )

    @staticmethod
    def grade_submission(db: Session, submission_id: int, grade_data: SubmissionGrade, current_user: User) -> SubmissionDetailResponse:
        """教师批改提交"""
        # 验证教师权限
        verify_teacher_permission(current_user)
        # 查找提交
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="提交不存在"
            )
        
        # 获取任务信息
        assignment = db.query(Assignment).filter(Assignment.id == submission.assignment_id).first()
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务不存在"
            )
        
        # 验证教师对班级的访问权限
        verify_class_member_access(db, assignment.class_id, current_user)
        
        # 更新提交的分数和报告
        submission.score = grade_data.score
        submission.report = grade_data.report
        submission.graded_at = func.now()
        
        try:
            db.commit()
            db.refresh(submission)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"批改提交失败: {str(e)}"
            )
        
        # 获取学生信息
        student = db.query(User).filter(User.id == submission.student_id).first()
        student_name = student.name if student else "未知学生"
        
        class_obj = db.query(Class).filter(Class.id == assignment.class_id).first()
        class_id = class_obj.id if class_obj else 0
        class_name = class_obj.name if class_obj else "未知班级"
        
        # 构建响应
        return SubmissionDetailResponse(
            id=submission.id,
            student_name=student_name,
            assignment_title=assignment.title,
            class_id=class_id,
            class_name=class_name,
            file_json=submission.file_json,
            report=submission.report,
            score=submission.score,
            submitted_at=submission.submitted_at,
            graded_at=submission.graded_at,
            is_graded=submission.is_graded
        )

    @staticmethod
    def get_assignment_statistics(db: Session, assignment_id: int, current_user: User) -> SubmissionStatistics:
        """获取任务提交统计"""
        # 验证教师权限
        verify_teacher_permission(current_user)
        
        # 查找任务
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务不存在"
            )
        
        # 验证教师对班级的访问权限
        verify_class_member_access(db, assignment.class_id, current_user)
        
        # 获取统计信息
        total_submissions = db.query(Submission).filter(Submission.assignment_id == assignment_id).count()
        graded_submissions = db.query(Submission).filter(
            Submission.assignment_id == assignment_id,
            Submission.score.isnot(None)
        ).count()
        ungraded_submissions = total_submissions - graded_submissions
        
        # 计算分数统计
        score_stats = db.query(
            func.avg(Submission.score).label('avg_score'),
            func.max(Submission.score).label('max_score'),
            func.min(Submission.score).label('min_score')
        ).filter(
            Submission.assignment_id == assignment_id,
            Submission.score.isnot(None)
        ).first()
        
        return SubmissionStatistics(
            total_submissions=total_submissions,
            graded_submissions=graded_submissions,
            ungraded_submissions=ungraded_submissions,
            average_score=float(score_stats.avg_score) if score_stats.avg_score else None,
            highest_score=float(score_stats.max_score) if score_stats.max_score else None,
            lowest_score=float(score_stats.min_score) if score_stats.min_score else None
        )

    @staticmethod
    def download_original_file(db: Session, submission_id: int, current_user: User) -> Response:
        """教师下载学生提交的原始文件"""
        # 验证教师权限
        verify_teacher_permission(current_user)
        
        # 查找提交
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="提交不存在"
            )
        
        # 获取任务信息
        assignment = db.query(Assignment).filter(Assignment.id == submission.assignment_id).first()
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务不存在"
            )
        
        # 验证教师对班级的访问权限
        verify_class_member_access(db, assignment.class_id, current_user)
        
        if not submission.original_file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="原始文件不存在"
            )
        
        # 返回文件下载响应
        return Response(
            content=submission.original_file,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename={submission.file_name or 'submission.docx'}"
            }
        )

    
    @staticmethod
    def get_my_submissions_by_class(db: Session, class_id: int, current_user: User) -> List[StudentSubmissionResponse]:
        """学生查看指定班级的提交列表"""
        verify_student_permission(current_user)
        
        # 验证学生是否在该班级中
        student_class = db.query(StudentClass).filter(
            StudentClass.student_id == current_user.id,
            StudentClass.class_id == class_id
        ).first()
        if not student_class:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="您不是该班级的学生"
            )
        
        # 获取该班级的提交
        submissions = db.query(Submission).join(Assignment).filter(
            Submission.student_id == current_user.id,
            Assignment.class_id == class_id
        ).order_by(Submission.submitted_at.desc()).all()
        
        result = []
        for submission in submissions:
            assignment = db.query(Assignment).filter(Assignment.id == submission.assignment_id).first()
            assignment_title = assignment.title if assignment else "未知任务"
            
            class_obj = db.query(Class).filter(Class.id == class_id).first()
            class_name = class_obj.name if class_obj else "未知班级"
            
            result.append(StudentSubmissionResponse(
                id=submission.id,
                assignment_title=assignment_title,
                assignment_id=submission.assignment_id,
                class_id=class_id,
                class_name=class_name,
                score=submission.score,
                submitted_at=submission.submitted_at,
                is_graded=submission.is_graded
            ))
        
        return result

    @staticmethod
    def get_my_submissions_by_assignment(db: Session, assignment_id: int, current_user: User) -> List[StudentSubmissionResponse]:
        """学生查看指定任务的提交列表"""
        verify_student_permission(current_user)
        
        # 获取任务信息
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务不存在"
            )
        
        # 验证学生是否在任务所属的班级中
        verify_class_member_access(db, assignment.class_id, current_user)
        
        # 获取该任务的提交
        submissions = db.query(Submission).filter(
            Submission.student_id == current_user.id,
            Submission.assignment_id == assignment_id
        ).order_by(Submission.submitted_at.desc()).all()
        
        result = []
        for submission in submissions:
            class_obj = db.query(Class).filter(Class.id == assignment.class_id).first()
            class_name = class_obj.name if class_obj else "未知班级"
            
            result.append(StudentSubmissionResponse(
                id=submission.id,
                assignment_title=assignment.title,
                assignment_id=submission.assignment_id,
                class_id=assignment.class_id,
                class_name=class_name,
                score=submission.score,
                submitted_at=submission.submitted_at,
                is_graded=submission.is_graded
            ))
        
        return result

    @staticmethod
    def get_pending_assignments(db: Session, current_user: User) -> List[PendingAssignmentResponse]:
        """学生查看未提交的任务列表"""
        verify_student_permission(current_user)
        
        # 获取学生加入的所有班级
        student_classes = db.query(StudentClass).filter(StudentClass.student_id == current_user.id).all()
        class_ids = [sc.class_id for sc in student_classes]
        
        if not class_ids:
            return []
        
        # 获取这些班级的所有任务
        all_assignments = db.query(Assignment).filter(Assignment.class_id.in_(class_ids)).all()
        
        # 获取学生已提交的任务ID
        submitted_assignment_ids = db.query(Submission.assignment_id).filter(
            Submission.student_id == current_user.id
        ).all()
        submitted_ids = [sa[0] for sa in submitted_assignment_ids]
        
        # 筛选未提交的任务
        pending_assignments = [a for a in all_assignments if a.id not in submitted_ids]
        
        result = []
        for assignment in pending_assignments:
            class_obj = db.query(Class).filter(Class.id == assignment.class_id).first()
            class_name = class_obj.name if class_obj else "未知班级"
            
            # 获取教师信息
            teacher = db.query(User).filter(User.id == assignment.teacher_id).first()
            teacher_name = teacher.name if teacher else "未知教师"
            
            result.append(PendingAssignmentResponse(
                id=assignment.id,
                title=assignment.title,
                description=assignment.description,
                class_id=assignment.class_id,
                class_name=class_name,
                teacher_name=teacher_name,
                created_at=assignment.created_at,
                deadline=None  # 目前模型中没有截止时间字段
            ))
        
        return result
    
    @staticmethod
    def get_class_submissions(db: Session, class_id: int, current_user: User) -> List[TeacherSubmissionResponse]:
        """教师查看指定班级的所有提交"""
        verify_teacher_permission(current_user)
        
        # 验证教师对班级的访问权限
        verify_class_member_access(db, class_id, current_user)
        
        # 获取该班级的所有提交
        submissions = db.query(Submission).join(Assignment).filter(
            Assignment.class_id == class_id
        ).order_by(Submission.submitted_at.desc()).all()
        
        result = []
        for submission in submissions:
            assignment = db.query(Assignment).filter(Assignment.id == submission.assignment_id).first()
            student = db.query(User).filter(User.id == submission.student_id).first()
            class_obj = db.query(Class).filter(Class.id == class_id).first()
            
            result.append(TeacherSubmissionResponse(
                id=submission.id,
                student_id=submission.student_id,
                student_name=student.name if student else "未知学生",
                assignment_title=assignment.title if assignment else "未知任务",
                assignment_id=submission.assignment_id,
                class_id=class_id,
                class_name=class_obj.name if class_obj else "未知班级",
                score=submission.score,
                submitted_at=submission.submitted_at,
                is_graded=submission.is_graded
            ))
        
        return result

    @staticmethod
    def get_student_submissions(db: Session, student_id: int, current_user: User) -> List[TeacherSubmissionResponse]:
        """教师查看指定学生的所有提交"""
        verify_teacher_permission(current_user)
        
        # 获取学生的所有提交
        submissions = db.query(Submission).filter(Submission.student_id == student_id).all()
        
        result = []
        for submission in submissions:
            assignment = db.query(Assignment).filter(Assignment.id == submission.assignment_id).first()
            if not assignment:
                continue
                
            # 验证教师对班级的访问权限
            try:
                verify_class_member_access(db, assignment.class_id, current_user)
            except HTTPException:
                continue  # 跳过没有权限的提交
            
            student = db.query(User).filter(User.id == submission.student_id).first()
            class_obj = db.query(Class).filter(Class.id == assignment.class_id).first()
            
            result.append(TeacherSubmissionResponse(
                id=submission.id,
                student_id=submission.student_id,
                student_name=student.name if student else "未知学生",
                assignment_title=assignment.title,
                assignment_id=submission.assignment_id,
                class_id=assignment.class_id,
                class_name=class_obj.name if class_obj else "未知班级",
                score=submission.score,
                submitted_at=submission.submitted_at,
                is_graded=submission.is_graded
            ))
        
        return result

    @staticmethod
    def get_ungraded_submissions(db: Session, assignment_id: int, current_user: User) -> List[TeacherSubmissionResponse]:
        """教师查看未批改的提交"""
        verify_teacher_permission(current_user)
        
        # 获取任务信息
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务不存在"
            )
        
        # 验证教师对班级的访问权限
        verify_class_member_access(db, assignment.class_id, current_user)
        
        # 获取未批改的提交
        submissions = db.query(Submission).filter(
            Submission.assignment_id == assignment_id,
            Submission.score.is_(None)
        ).order_by(Submission.submitted_at.desc()).all()
        
        result = []
        for submission in submissions:
            student = db.query(User).filter(User.id == submission.student_id).first()
            class_obj = db.query(Class).filter(Class.id == assignment.class_id).first()
            
            result.append(TeacherSubmissionResponse(
                id=submission.id,
                student_id=submission.student_id,
                student_name=student.name if student else "未知学生",
                assignment_title=assignment.title,
                assignment_id=submission.assignment_id,
                class_id=assignment.class_id,
                class_name=class_obj.name if class_obj else "未知班级",
                score=submission.score,
                submitted_at=submission.submitted_at,
                is_graded=submission.is_graded
            ))
        
        return result

