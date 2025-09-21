import axios, { type AxiosInstance, type AxiosResponse } from 'axios'

// 创建axios实例
const apiBaseUrl = (import.meta as any).env?.VITE_API_BASE_URL || 'http://localhost:8000'
const apiClient: AxiosInstance = axios.create({
  baseURL: apiBaseUrl, // 后端API地址
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器 - 添加认证token
apiClient.interceptors.request.use(
  async (config) => {
    try {
      // 优先从 Pinia store 获取 token
      const { useAuth } = await import('../store/auth')
      const authStore = useAuth()
      
      // 检查并刷新即将过期的token
      await authStore.checkAndRefreshToken()
      
      const token = authStore.getCurrentToken()
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
        console.log('🔑 Token added to request:', config.url, 'Token:', token.substring(0, 20) + '...')
      } else {
        console.log('⚠️ No token available for request:', config.url)
      }
    } catch (_) {
      // 如果 store 不可用，回退到 localStorage
      const token = localStorage.getItem('auth_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
        console.log('🔑 Using localStorage token for request:', config.url)
      } else {
        console.log('⚠️ No token in localStorage for request:', config.url)
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  async (error) => {
    if (error.response?.status === 401) {
      // 避免在 logout 请求时触发循环调用
      const isLogoutRequest = error.config?.url?.includes('/auth/logout')
      
      if (!isLogoutRequest) {
        // 同步 Pinia 状态清理认证信息（懒加载避免循环依赖）
        try {
          const { useAuth } = await import('../store/auth')
          const authStore = useAuth()
          // 直接清理状态，不调用 logout API
          authStore.clearAuthState()
        } catch (_) {
          // 如果 store 不可用，手动清理 localStorage
          localStorage.removeItem('auth_token')
          localStorage.removeItem('auth_user')
          localStorage.removeItem('auth_token_expiry')
        }
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient