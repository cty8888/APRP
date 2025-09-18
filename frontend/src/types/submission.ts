// 提交相关类型定义

export interface SubmissionGrade {
  score: number
  report: string
}

export interface StudentSubmissionResponse {
  id: number
  assignment_title: string
  assignment_id: number
  class_id: number
  class_name: string
  score?: number
  submitted_at: string
  is_graded: boolean
}

export interface TeacherSubmissionResponse {
  id: number
  student_id: number
  student_name: string
  assignment_title: string
  assignment_id: number
  class_id: number
  class_name: string
  score?: number
  submitted_at: string
  is_graded: boolean
}

export interface SubmissionDetailResponse {
  id: number
  student_name: string
  assignment_title: string
  class_id: number
  class_name: string
  file_json?: any
  report?: string
  score?: number
  submitted_at: string
  graded_at?: string
  is_graded: boolean
}

export interface SubmissionCreateResponse {
  id: number
  assignment_title: string
  submitted_at: string
  message: string
}

export interface SubmissionStatistics {
  total_submissions: number
  graded_submissions: number
  ungraded_submissions: number
  average_score?: number
  highest_score?: number
  lowest_score?: number
}

export interface PendingAssignmentResponse {
  id: number
  title: string
  description?: string
  class_id: number
  class_name: string
  teacher_name: string
  created_at: string
  deadline?: string
}
