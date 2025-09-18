// 任务相关类型定义

export interface AssignmentCreate {
  title: string
  description?: string
  class_id: number
}

export interface AssignmentUpdate {
  title?: string
  description?: string
}

export interface AssignmentResponse {
  id: number
  title: string
  description?: string
  class_id: number
  class_name: string
  teacher_id: number
  teacher_name: string
  created_at: string
  updated_at: string
}
