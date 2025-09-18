import axios, { type AxiosInstance, type AxiosResponse } from 'axios'

// 创建axios实例
const apiClient: AxiosInstance = axios.create({
  baseURL: 'http://localhost:8000', // 后端API地址
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器 - 添加认证token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
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
  (error) => {
    if (error.response?.status === 401) {
      // 清除本地存储的token
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // 使用路由重定向而不是直接修改location
      // 注意：这里不能直接使用router，因为这是在模块级别
      // 让路由守卫处理重定向逻辑
    }
    return Promise.reject(error)
  }
)

export default apiClient