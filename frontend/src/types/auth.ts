// 认证相关类型定义
export const UserRole = {
  TEACHER: 'teacher',
  STUDENT: 'student'
} as const

export type UserRole = typeof UserRole[keyof typeof UserRole]

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
  name: string
  password: string
}

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

export interface FormState {
  isLoading: boolean
  error: string | null
}
