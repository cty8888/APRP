import apiClient from './index'



export function getRoot() {
  return apiClient.get('/')
}

// 文件上传接口
export function uploadDocx(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  
  return apiClient.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export default {
  getRoot,
  uploadDocx
}
