import apiClient from './index'


// 系统相关接口
export function healthCheck() {
  return apiClient.get('/health')
}

export function getRoot() {
  return apiClient.get('/')
}

export default {
  healthCheck,
  getRoot
}
