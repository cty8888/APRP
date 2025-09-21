import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '../api'
import type { User, UserCreate, UserLogin } from '../types/auth'

// 常量定义
const TOKEN_KEY = 'auth_token'
const USER_KEY = 'auth_user'
const TOKEN_EXPIRY_KEY = 'auth_token_expiry'

export const useAuth = defineStore('auth', () => {
  // 状态定义
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isLoading = ref(false)
  const tokenExpiry = ref<number | null>(null)

  // 计算属性
  const isAuthenticated = computed(() => {
    if (!token.value || !user.value) return false
    
    // 检查token是否过期
    if (tokenExpiry.value && Date.now() > tokenExpiry.value) {
      clearAuth()
      return false
    }
    
    return true
  })

  // 检查token是否即将过期（提前5分钟刷新）
  const isTokenExpiringSoon = computed(() => {
    if (!tokenExpiry.value) return false
    const fiveMinutes = 5 * 60 * 1000
    return Date.now() > (tokenExpiry.value - fiveMinutes)
  })

  // 私有方法：清理认证信息
  const clearAuth = () => {
    user.value = null
    token.value = null
    tokenExpiry.value = null
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    localStorage.removeItem(TOKEN_EXPIRY_KEY)
  }

  // 私有方法：保存认证信息
  const saveAuth = (tokenData: string, userData: User, expiryTime?: number) => {
    token.value = tokenData
    user.value = userData
    
    localStorage.setItem(TOKEN_KEY, tokenData)
    localStorage.setItem(USER_KEY, JSON.stringify(userData))
    
    if (expiryTime) {
      tokenExpiry.value = expiryTime
      localStorage.setItem(TOKEN_EXPIRY_KEY, expiryTime.toString())
    }
  }

  // 私有方法：验证存储的认证信息
  const validateStoredAuth = (): boolean => {
    const storedToken = localStorage.getItem(TOKEN_KEY)
    const storedUser = localStorage.getItem(USER_KEY)
    const storedExpiry = localStorage.getItem(TOKEN_EXPIRY_KEY)
    
    if (!storedToken || !storedUser) return false
    
    // 检查token是否过期
    if (storedExpiry) {
      const expiryTime = parseInt(storedExpiry)
      if (Date.now() > expiryTime) {
        clearAuth()
        return false
      }
      tokenExpiry.value = expiryTime
    }
    
    try {
      const userData = JSON.parse(storedUser)
      if (!userData?.id || !userData?.name || !userData?.role) {
        return false
      }
      
      token.value = storedToken
      user.value = userData
      return true
    } catch {
      return false
    }
  }

  // 初始化认证状态
  const initAuth = () => {
    if (!validateStoredAuth()) {
      clearAuth()
    } else {
      // 如果token即将过期，尝试刷新
      if (isTokenExpiringSoon.value) {
        refreshToken()
      }
    }
  }

  // 登录
  const login = async (name: string, password: string) => {
    isLoading.value = true
    try {
      const loginData: UserLogin = { name, password }
      const response = await authApi.login(loginData)
      
      // 先临时保存token以便后续请求使用
      token.value = response.access_token
      localStorage.setItem(TOKEN_KEY, response.access_token)
      
      console.log('🔑 Token saved, now fetching user data...')
      
      // 现在获取用户信息（此时token已经可用）
      const userData = await authApi.getCurrentUser()
      
      console.log('✅ User data fetched successfully:', userData)
      
      // 计算token过期时间（后端配置为30分钟）
      const expiryTime = Date.now() + (30 * 60 * 1000)
      
      // 完整保存认证信息
      saveAuth(response.access_token, userData, expiryTime)
      
      return { success: true }
    } catch (error: any) {
      console.error('Login error:', error)
      clearAuth()
      
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

  // 登出
  const logout = async () => {
    try {
      // 调用后端登出API
      await authApi.logout()
      console.log('Successfully logged out from server')
    } catch (error) {
      console.error('Logout API error:', error)
      // 即使后端登出失败，也要清理本地状态
    } finally {
      // 无论API调用是否成功，都清理本地状态
      clearAuth()
    }
  }

  // 刷新token
  const refreshToken = async () => {
    if (!token.value) return false
    
    try {
      // 调用后端刷新令牌API
      const response = await authApi.refreshToken()
      
      if (response.access_token) {
        // 计算新的过期时间
        const expiryTime = Date.now() + (30 * 60 * 1000) // 30分钟
        
        // 保存新的令牌
        saveAuth(response.access_token, user.value!, expiryTime)
        
        return true
      }
      return false
    } catch (error) {
      console.error('Token refresh failed:', error)
      clearAuth()
      return false
    }
  }

  // 获取当前token（供API client使用）
  const getCurrentToken = (): string | null => {
    // 直接返回token，不依赖isAuthenticated状态
    // 因为在登录过程中，user可能还未加载，但token已经可用
    if (token.value) {
      // 检查token是否过期
      if (tokenExpiry.value && Date.now() > tokenExpiry.value) {
        clearAuth()
        return null
      }
      return token.value
    }
    return null
  }

  // 检查并刷新即将过期的token
  const checkAndRefreshToken = async (): Promise<boolean> => {
    if (isTokenExpiringSoon.value && token.value) {
      try {
        const success = await refreshToken()
        return success
      } catch (error) {
        console.error('Auto refresh token failed:', error)
        return false
      }
    }
    return true
  }

  // 检查权限
  const hasRole = (role: string) => {
    return user.value?.role === role
  }

  const isTeacher = computed(() => hasRole('teacher'))
  const isStudent = computed(() => hasRole('student'))

  // 初始化
  initAuth()

  // 清理认证状态（供 API client 使用，避免循环调用）
  const clearAuthState = () => {
    clearAuth()
  }

  return {
    // 状态
    user,
    token,
    isLoading,
    isAuthenticated,
    isTokenExpiringSoon,
    isTeacher,
    isStudent,
    
    // 方法
    login,
    register,
    logout,
    refreshToken,
    hasRole,
    getCurrentToken,
    checkAndRefreshToken,
    clearAuthState,
    initAuth
  }
})