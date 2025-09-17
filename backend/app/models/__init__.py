# 导入所有模型，确保它们被注册到 SQLAlchemy
from .user import User
from .class_model import Class
from .assignment import Assignment
from .student_class import StudentClass
from .teacher_class import TeacherClass
from .submission import Submission

__all__ = ["User", "Class", "Assignment", "StudentClass", "TeacherClass", "Submission"]
