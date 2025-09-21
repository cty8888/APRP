import apiClient from './client'
import type { User, UserCreate, UserLogin, Token } from '../types/auth'

// 认证相关API
export const authApi = {
  // 用户注册
  register: async (userData: UserCreate): Promise<User> => {
    const response = await apiClient.post('/auth/register', userData)
    return response.data
  },

  // 用户登录
  login: async (loginData: UserLogin): Promise<Token> => {
    const formData = new FormData()
    formData.append('username', loginData.name)
    formData.append('password', loginData.password)
    
    const response = await apiClient.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  // 获取当前用户信息
  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get('/auth/dashboard')
    return response.data
  },

  // 刷新访问令牌
  refreshToken: async (): Promise<Token> => {
    const response = await apiClient.post('/auth/refresh')
    return response.data
  },

  // 用户登出
  logout: async (): Promise<{ message: string; user_id: number }> => {
    const response = await apiClient.post('/auth/logout')
    return response.data
  }
}
