import { defineStore } from 'pinia'
import { ref, computed, nextTick } from 'vue'
import { authApi } from '../api'
import type { User, UserCreate, UserLogin } from '../types/auth'

export const useAuth = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isLoading = ref(false)
  // 添加一个强制刷新标志
  const refreshFlag = ref(0)

  const isAuthenticated = computed(() => {
    // 使用refreshFlag确保响应性
    refreshFlag.value
    return !!token.value && !!user.value
  })

  // 强制刷新响应性
  const forceRefresh = () => {
    refreshFlag.value++
  }

  // 登出函数 - 先定义
  const logout = async () => {
    console.log('Store: logout called, clearing state...')
    // 立即清除状态
    user.value = null
    token.value = null
    console.log('Store: state cleared, user:', user.value, 'token:', token.value)
    // 清除本地存储
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    // 调用API清理（如果需要）
    authApi.logout()
    // 强制刷新响应性
    forceRefresh()
    // 确保状态更新被正确处理
    await nextTick()
    console.log('Store: logout completed, isAuthenticated:', isAuthenticated.value)
  }

  // 初始化认证状态
  const initAuth = () => {
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')
    
    if (savedToken && savedUser) {
      try {
        const userData = JSON.parse(savedUser)
        if (userData && userData.id && userData.name && userData.role) {
          token.value = savedToken
          user.value = userData
          // 强制刷新响应性
          forceRefresh()
        } else {
          // 数据格式不正确，清理
          logout()
        }
      } catch (error) {
        console.error('Failed to parse saved user:', error)
        logout()
      }
    } else {
      // 数据不完整，清理
      logout()
    }
  }

  // 登录
  const login = async (name: string, password: string) => {
    isLoading.value = true
    try {
      const loginData: UserLogin = { name, password }
      const response = await authApi.login(loginData)
      token.value = response.access_token
      localStorage.setItem('token', response.access_token)
      
      // 获取用户信息
      const userData = await authApi.getCurrentUser()
      user.value = userData
      localStorage.setItem('user', JSON.stringify(userData))
      
      // 强制刷新响应性
      forceRefresh()
      
      console.log('Store: login successful, user:', user.value, 'token:', token.value)
      
      return { success: true }
    } catch (error: any) {
      console.error('Login error:', error)
      return { 
        success: false, 
        error: error.response?.data?.detail || '登录失败' 
      }
    } finally {
      isLoading.value = false
    }
  }

  // 注册
  const register = async (userData: UserCreate) => {
    isLoading.value = true
    try {
      await authApi.register(userData)
      return { success: true }
    } catch (error: any) {
      console.error('Register error:', error)
      return { 
        success: false, 
        error: error.response?.data?.detail || '注册失败' 
      }
    } finally {
      isLoading.value = false
    }
  }


  // 立即初始化认证状态（在store创建时）
  initAuth()

  return {
    user,
    token,
    isLoading,
    isAuthenticated,
    login,
    register,
    logout,
    initAuth
  }
})