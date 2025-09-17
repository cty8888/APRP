from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.user import User
from app.schemas.submission_schema import (
    SubmissionGrade, 
    SubmissionDetailResponse, SubmissionCreateResponse, SubmissionStatistics,
    StudentSubmissionResponse, TeacherSubmissionResponse, PendingAssignmentResponse
)
from app.routers.auth import get_current_user
from app.services.submission_service import SubmissionService

router = APIRouter(prefix="/submissions", tags=["提交管理"])


@router.post("/", response_model=SubmissionCreateResponse, summary="学生上传文件提交")
async def create_submission(assignment_id: int = Form(..., description="任务ID"),file: UploadFile = File(..., description="上传的docx文件"),current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """学生上传文件提交文档（支持重复提交覆盖）"""
    return SubmissionService.create_submission_with_file(db, assignment_id, file, current_user)


@router.get("/my-submissions", response_model=List[StudentSubmissionResponse], summary="查看我的提交")
async def get_my_submissions(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """学生查看自己的提交列表"""
    return SubmissionService.get_my_submissions(db, current_user)

@router.get("/my-submissions/class/{class_id}", response_model=List[StudentSubmissionResponse], summary="按班级查看我的提交")
async def get_my_submissions_by_class(class_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """学生查看指定班级的提交列表"""
    return SubmissionService.get_my_submissions_by_class(db, class_id, current_user)


@router.get("/my-submissions/assignment/{assignment_id}", response_model=List[StudentSubmissionResponse], summary="按任务查看我的提交")
async def get_my_submissions_by_assignment(assignment_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """学生查看指定任务的提交列表"""
    return SubmissionService.get_my_submissions_by_assignment(db, assignment_id, current_user)


@router.get("/my-submissions/pending", response_model=List[PendingAssignmentResponse], summary="查看待提交任务")
async def get_pending_assignments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """学生查看未提交的任务列表"""
    return SubmissionService.get_pending_assignments(db, current_user)


@router.get("/assignment/{assignment_id}", response_model=List[TeacherSubmissionResponse], summary="查看任务提交")
async def get_assignment_submissions(assignment_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """教师查看指定任务的提交列表"""
    return SubmissionService.get_assignment_submissions(db, assignment_id, current_user)


@router.get("/class/{class_id}", response_model=List[TeacherSubmissionResponse], summary="查看班级提交")
async def get_class_submissions(class_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """教师查看指定班级的所有提交"""
    return SubmissionService.get_class_submissions(db, class_id, current_user)


@router.get("/student/{student_id}", response_model=List[TeacherSubmissionResponse], summary="查看学生提交")
async def get_student_submissions(student_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """教师查看指定学生的所有提交"""
    return SubmissionService.get_student_submissions(db, student_id, current_user)


@router.get("/assignment/{assignment_id}/ungraded", response_model=List[TeacherSubmissionResponse], summary="查看未批改提交")
async def get_ungraded_submissions(assignment_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """教师查看未批改的提交"""
    return SubmissionService.get_ungraded_submissions(db, assignment_id, current_user)


@router.get("/{submission_id}", response_model=SubmissionDetailResponse, summary="查看提交详情")
async def get_submission_detail(submission_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """查看提交详情（学生查看自己的，教师查看班级内的）"""
    return SubmissionService.get_submission_detail(db, submission_id, current_user)


@router.put("/{submission_id}/grade", response_model=SubmissionDetailResponse, summary="批改提交")
async def grade_submission(submission_id: int,grade_data: SubmissionGrade,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """教师批改提交"""
    return SubmissionService.grade_submission(db, submission_id, grade_data, current_user)


@router.get("/assignment/{assignment_id}/statistics", response_model=SubmissionStatistics, summary="查看提交统计")
async def get_assignment_statistics(assignment_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    """教师查看指定任务的提交统计"""
    return SubmissionService.get_assignment_statistics(db, assignment_id, current_user)


@router.get("/{submission_id}/download", summary="下载原始文件")
async def download_original_file(submission_id: int,current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """教师下载学生提交的原始文件"""
    return SubmissionService.download_original_file(db, submission_id, current_user)
