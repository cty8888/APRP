import apiClient from './client'
import type { 
  SubmissionGrade,
  SubmissionDetailResponse,
  SubmissionCreateResponse,
  SubmissionStatistics,
  StudentSubmissionResponse,
  TeacherSubmissionResponse,
  PendingAssignmentResponse
} from '../types/submission'

// 提交相关API
export const submissionApi = {
  // 学生上传文件提交
  create: async (assignmentId: number, file: File): Promise<SubmissionCreateResponse> => {
    const formData = new FormData()
    formData.append('assignment_id', assignmentId.toString())
    formData.append('file', file)
    
    const response = await apiClient.post('/submissions/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // 获取我的提交
  getMySubmissions: async (): Promise<StudentSubmissionResponse[]> => {
    const response = await apiClient.get('/submissions/my-submissions')
    return response.data
  },

  // 按班级获取我的提交
  getMySubmissionsByClass: async (classId: number): Promise<StudentSubmissionResponse[]> => {
    const response = await apiClient.get(`/submissions/my-submissions/class/${classId}`)
    return response.data
  },

  // 按任务获取我的提交
  getMySubmissionsByAssignment: async (assignmentId: number): Promise<StudentSubmissionResponse[]> => {
    const response = await apiClient.get(`/submissions/my-submissions/assignment/${assignmentId}`)
    return response.data
  },

  // 获取待提交任务
  getPendingAssignments: async (): Promise<PendingAssignmentResponse[]> => {
    const response = await apiClient.get('/submissions/my-submissions/pending')
    return response.data
  },

  // 获取任务提交（教师）
  getAssignmentSubmissions: async (assignmentId: number): Promise<TeacherSubmissionResponse[]> => {
    const response = await apiClient.get(`/submissions/assignment/${assignmentId}`)
    return response.data
  },

  // 获取班级提交（教师）
  getClassSubmissions: async (classId: number): Promise<TeacherSubmissionResponse[]> => {
    const response = await apiClient.get(`/submissions/class/${classId}`)
    return response.data
  },

  // 获取学生提交（教师）
  getStudentSubmissions: async (studentId: number): Promise<TeacherSubmissionResponse[]> => {
    const response = await apiClient.get(`/submissions/student/${studentId}`)
    return response.data
  },

  // 获取未批改提交
  getUngradedSubmissions: async (assignmentId: number): Promise<TeacherSubmissionResponse[]> => {
    const response = await apiClient.get(`/submissions/assignment/${assignmentId}/ungraded`)
    return response.data
  },

  // 获取提交详情
  getSubmissionDetail: async (submissionId: number): Promise<SubmissionDetailResponse> => {
    const response = await apiClient.get(`/submissions/${submissionId}`)
    return response.data
  },

  // 批改提交
  gradeSubmission: async (submissionId: number, gradeData: SubmissionGrade): Promise<SubmissionDetailResponse> => {
    const response = await apiClient.put(`/submissions/${submissionId}/grade`, gradeData)
    return response.data
  },

  // 获取提交统计
  getAssignmentStatistics: async (assignmentId: number): Promise<SubmissionStatistics> => {
    const response = await apiClient.get(`/submissions/assignment/${assignmentId}/statistics`)
    return response.data
  },

  // 下载原始文件
  downloadOriginalFile: async (submissionId: number): Promise<Blob> => {
    const response = await apiClient.get(`/submissions/${submissionId}/download`, {
      responseType: 'blob'
    })
    return response.data
  }
}
