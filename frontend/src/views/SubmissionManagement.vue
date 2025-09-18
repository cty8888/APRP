<template>
  <div class="submission-management">
    <div class="page-header">
      <h1>提交管理</h1>
    </div>

    <div class="tabs">
      <button 
        :class="['tab', { active: activeTab === 'list' }]"
        @click="activeTab = 'list'"
      >
        提交列表
      </button>
      <button 
        :class="['tab', { active: activeTab === 'submit' }]"
        @click="activeTab = 'submit'"
        v-if="user?.role === 'student'"
      >
        提交作业
      </button>
    </div>

    <div class="tab-content">
      <!-- 提交列表 -->
      <div v-if="activeTab === 'list'" class="tab-pane">
        <SubmissionList 
          ref="submissionListRef"
          :title="getListTitle()"
          :isTeacherView="user?.role === 'teacher'"
          :classId="classId"
          :assignmentId="assignmentId"
          @viewSubmission="handleViewSubmission" 
        />
      </div>

      <!-- 提交作业 -->
      <div v-if="activeTab === 'submit'" class="tab-pane">
        <div class="form-container">
          <SubmitAssignmentForm @success="handleSubmitSuccess" />
        </div>
      </div>
    </div>

    <!-- 提交详情/批改弹窗 -->
    <div v-if="selectedSubmission" class="modal-overlay" @click="closeModal">
      <div class="modal large" @click.stop>
        <div class="modal-header">
          <h3>提交详情</h3>
          <button @click="closeModal" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="submission-details">
            <div class="detail-row">
              <span class="label">学生：</span>
              <span>{{ selectedSubmission.student_name }}</span>
            </div>
            <div class="detail-row">
              <span class="label">任务：</span>
              <span>{{ selectedSubmission.assignment_title }}</span>
            </div>
            <div class="detail-row">
              <span class="label">班级：</span>
              <span>{{ selectedSubmission.class_name }}</span>
            </div>
            <div class="detail-row">
              <span class="label">提交时间：</span>
              <span>{{ formatDate(selectedSubmission.submitted_at) }}</span>
            </div>
            <div class="detail-row">
              <span class="label">状态：</span>
              <span :class="['status', selectedSubmission.is_graded ? 'graded' : 'pending']">
                {{ selectedSubmission.is_graded ? '已批改' : '待批改' }}
              </span>
            </div>
            
            <div v-if="selectedSubmission.is_graded" class="grade-info">
              <div class="detail-row">
                <span class="label">分数：</span>
                <span class="score">{{ selectedSubmission.score }}分</span>
              </div>
              <div v-if="selectedSubmission.report" class="detail-row">
                <span class="label">批改报告：</span>
                <div class="report">{{ selectedSubmission.report }}</div>
              </div>
              <div v-if="selectedSubmission.graded_at" class="detail-row">
                <span class="label">批改时间：</span>
                <span>{{ formatDate(selectedSubmission.graded_at) }}</span>
              </div>
            </div>
          </div>
          
          <div class="modal-actions">
            <button 
              v-if="user?.role === 'teacher' && !isGrading"
              @click="startGrading"
              class="btn btn-primary"
            >
              {{ selectedSubmission.is_graded ? '修改批改' : '开始批改' }}
            </button>
            
            <button 
              v-if="isGrading"
              @click="cancelGrading"
              class="btn btn-outline"
            >
              取消批改
            </button>
          </div>
          
          <!-- 批改表单 -->
          <div v-if="isGrading" class="grading-section">
            <GradeSubmissionForm 
              :submissionId="selectedSubmission.id"
              @success="handleGradeSuccess"
              @cancel="cancelGrading"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from '../store/auth'
import { SubmissionList, SubmitAssignmentForm, GradeSubmissionForm } from '../components'
import { submissionApi } from '../api'
import type { StudentSubmissionResponse, TeacherSubmissionResponse, SubmissionDetailResponse } from '../types'

const route = useRoute()
const { user } = useAuth()

const activeTab = ref('list')
const selectedSubmission = ref<SubmissionDetailResponse | null>(null)
const submissionListRef = ref()
const classId = ref<number | undefined>()
const assignmentId = ref<number | undefined>()
const isGrading = ref(false)

const getListTitle = () => {
  if (classId.value) return '班级提交'
  if (assignmentId.value) return '任务提交'
  return user?.role === 'teacher' ? '学生提交' : '我的提交'
}

const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString('zh-CN')
}

const handleViewSubmission = async (submission: StudentSubmissionResponse | TeacherSubmissionResponse) => {
  try {
    selectedSubmission.value = await submissionApi.getSubmissionDetail(submission.id)
  } catch (error) {
    console.error('Failed to load submission detail:', error)
  }
}

const closeModal = () => {
  selectedSubmission.value = null
  isGrading.value = false
}

const startGrading = () => {
  isGrading.value = true
}

const cancelGrading = () => {
  isGrading.value = false
}

const handleGradeSuccess = async (data: any) => {
  console.log('批改成功:', data)
  isGrading.value = false
  // 刷新提交详情
  if (selectedSubmission.value) {
    try {
      selectedSubmission.value = await submissionApi.getSubmissionDetail(selectedSubmission.value.id)
    } catch (error) {
      console.error('Failed to refresh submission detail:', error)
    }
  }
  // 刷新提交列表
  if (submissionListRef.value) {
    submissionListRef.value.refreshSubmissions()
  }
}

const handleSubmitSuccess = (data: any) => {
  console.log('提交成功:', data)
  activeTab.value = 'list'
  // 刷新提交列表
  if (submissionListRef.value) {
    submissionListRef.value.refreshSubmissions()
  }
}

onMounted(() => {
  // 从路由参数获取参数
  if (route.query.classId) {
    classId.value = parseInt(route.query.classId as string)
  }
  if (route.query.assignmentId) {
    assignmentId.value = parseInt(route.query.assignmentId as string)
  }
})
</script>

<style scoped>
.submission-management {
  padding: 2rem 0;
}

.page-header {
  margin-bottom: 2rem;
}

.tabs {
  display: flex;
  border-bottom: 2px solid #e9ecef;
  margin-bottom: 2rem;
}

.tab {
  background: none;
  border: none;
  padding: 1rem 2rem;
  cursor: pointer;
  font-size: 1.2rem;
  color: #666;
  transition: all 0.2s;
}

.tab:hover {
  color: #007bff;
}

.tab.active {
  color: #007bff;
  border-bottom: 2px solid #007bff;
  margin-bottom: -2px;
}

.form-container {
  max-width: 600px;
  margin: 0 auto;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal.large {
  max-width: 800px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.6rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 1.5rem;
}

.submission-details {
  margin-bottom: 2rem;
}

.detail-row {
  display: flex;
  margin: 1rem 0;
  align-items: flex-start;
}

.detail-row .label {
  font-weight: 600;
  min-width: 120px;
  color: #333;
}

.status {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 500;
}

.status.graded {
  background-color: #d4edda;
  color: #155724;
}

.status.pending {
  background-color: #fff3cd;
  color: #856404;
}

.score {
  color: #28a745;
  font-weight: 600;
  font-size: 1.2rem;
}

.report {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 0.5rem;
  white-space: pre-wrap;
  flex: 1;
}

.grade-info {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.modal-actions .btn {
  flex: 1;
}

.grading-section {
  border-top: 1px solid #e9ecef;
  padding-top: 1.5rem;
  margin-top: 1.5rem;
}
</style>
