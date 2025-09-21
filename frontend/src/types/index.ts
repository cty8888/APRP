// API响应类型
export interface ApiResponse<T = any> {
  data?: T
  message?: string
  error?: string
}

// 导出其他模块类型
export * from './auth'
export * from './class'
export * from './assignment'
export * from './submission'