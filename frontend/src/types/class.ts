// 班级相关类型定义

export interface ClassCreate {
  name: string
  description?: string
}

export interface ClassUpdate {
  name?: string
  description?: string
}

export interface ClassResponse {
  id: number
  name: string
  class_code: string
  description?: string
  teacher_id: number
  teacher_name: string
  created_at: string
  updated_at: string
  student_count: number
  my_role: 'main_teacher' | 'assistant_teacher' | 'student'
}

export interface ClassWithStudents {
  id: number
  name: string
  teacher_id: number
  created_at: string
  updated_at: string
  student_count: number
  students: Array<{
    id: number
    name: string
    joined_at: string
  }>
}

export interface JoinClassRequest {
  class_id: number
}

export interface ClassSearch {
  search_term: string
}

export interface StudentClassResponse {
  id: number
  student_id: number
  class_id: number
  joined_at: string
}
