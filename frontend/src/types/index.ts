// 用户角色枚举
export const UserRole = {
  TEACHER: 'teacher',
  STUDENT: 'student'
} as const

export type UserRole = typeof UserRole[keyof typeof UserRole]

// 用户相关类型
export interface User {
  id: number
  name: string
  role: UserRole
  created_at: string
  updated_at: string
}

export interface UserCreate {
  name: string
  password: string
  role: UserRole
}

export interface UserLogin {
  username: string
  password: string
}

// 认证相关类型
export interface Token {
  access_token: string
  token_type: string
}

export interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
}

// API响应类型
export interface ApiResponse<T = any> {
  data?: T
  message?: string
  error?: string
}

// 表单状态
export interface FormState {
  isLoading: boolean
  error: string | null
}

// 导出其他模块类型
export * from './class'
export * from './assignment'
export * from './submission'