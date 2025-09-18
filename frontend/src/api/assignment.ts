import apiClient from './client'
import type { 
  AssignmentCreate, 
  AssignmentUpdate, 
  AssignmentResponse 
} from '../types/assignment'

// 任务相关API
export const assignmentApi = {
  // 创建任务
  create: async (assignmentData: AssignmentCreate): Promise<AssignmentResponse> => {
    const response = await apiClient.post('/assignments/', assignmentData)
    return response.data
  },

  // 获取班级任务
  getClassAssignments: async (classId: number): Promise<AssignmentResponse[]> => {
    const response = await apiClient.get(`/assignments/class/${classId}`)
    return response.data
  },

  // 获取我创建的任务
  getMyAssignments: async (): Promise<AssignmentResponse[]> => {
    const response = await apiClient.get('/assignments/my-assignments')
    return response.data
  },

  // 更新任务
  update: async (assignmentId: number, assignmentData: AssignmentUpdate): Promise<AssignmentResponse> => {
    const response = await apiClient.put(`/assignments/${assignmentId}`, assignmentData)
    return response.data
  },

  // 删除任务
  delete: async (assignmentId: number): Promise<void> => {
    await apiClient.delete(`/assignments/${assignmentId}`)
  }
}
