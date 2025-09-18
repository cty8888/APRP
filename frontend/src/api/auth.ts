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

  // 登出（可用于调用后端登出API，目前为空实现）
  logout: () => {
    // 如果后端有登出接口，可以在这里调用
    // 本地存储的清理由store负责
  }
}
