import apiClient from './client'
import type { 
  ClassCreate, 
  ClassUpdate, 
  ClassResponse, 
  ClassWithStudents, 
  JoinClassRequest, 
  ClassSearch, 
  StudentClassResponse 
} from '../types/class'

// 班级相关API
export const classApi = {
  // 创建班级
  create: async (classData: ClassCreate): Promise<ClassResponse> => {
    const response = await apiClient.post('/classes/', classData)
    return response.data
  },

  // 搜索班级
  search: async (searchData: ClassSearch): Promise<ClassResponse[]> => {
    const response = await apiClient.post('/classes/search', searchData)
    return response.data
  },

  // 学生加入班级
  joinAsStudent: async (joinData: JoinClassRequest): Promise<StudentClassResponse> => {
    const response = await apiClient.post('/classes/join', joinData)
    return response.data
  },

  // 教师加入班级（作为助教）
  joinAsTeacher: async (joinData: JoinClassRequest): Promise<any> => {
    const response = await apiClient.post('/classes/join-as-teacher', joinData)
    return response.data
  },

  // 获取我的班级
  getMyClasses: async (): Promise<ClassResponse[]> => {
    const response = await apiClient.get('/classes/my-classes')
    return response.data
  },

  // 获取我创建的班级
  getMyCreatedClasses: async (): Promise<ClassResponse[]> => {
    const response = await apiClient.get('/classes/my-created-classes')
    return response.data
  },

  // 获取我加入的班级
  getMyJoinedClasses: async (): Promise<ClassResponse[]> => {
    const response = await apiClient.get('/classes/my-joined-classes')
    return response.data
  },

  // 获取班级学生
  getClassStudents: async (classId: number): Promise<ClassWithStudents> => {
    const response = await apiClient.get(`/classes/${classId}/students`)
    return response.data
  },

  // 更新班级
  update: async (classId: number, classData: ClassUpdate): Promise<ClassResponse> => {
    const response = await apiClient.put(`/classes/${classId}`, classData)
    return response.data
  },

  // 删除班级
  delete: async (classId: number): Promise<void> => {
    await apiClient.delete(`/classes/${classId}`)
  }
}
