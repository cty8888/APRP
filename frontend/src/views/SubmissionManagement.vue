<template>
  <div class="submission-management">
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <i class="icon">📋</i>
          提交管理
        </h1>
        <p class="page-subtitle">管理学生作业提交和批改</p>
      </div>
      <div class="header-divider"></div>
    </div>

    <div class="tabs-container">
      <div class="tabs">
        <button 
          :class="['tab', { active: activeTab === 'list' }]"
          @click="activeTab = 'list'"
        >
          <i class="icon">📝</i>
          提交列表
        </button>
        <button 
          :class="['tab', { active: activeTab === 'submit' }]"
          @click="activeTab = 'submit'"
          v-if="shouldShowSubmitTab()"
        >
          <i class="icon">📤</i>
          提交作业
        </button>
      </div>
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
          :studentId="studentId"
          @viewSubmission="handleViewSubmission" 
        />
      </div>

      <!-- 提交作业 -->
      <div v-if="activeTab === 'submit'" class="tab-pane">
        <div class="form-container">
          <SubmitAssignmentForm 
            :assignmentId="assignmentId"
            @success="handleSubmitSuccess" 
          />
        </div>
      </div>
    </div>


    <!-- 批改表单弹窗 -->
    <div v-if="isGrading && selectedSubmission" class="modal-overlay" @click="cancelGrading">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>批改作业</h3>
          <button @click="cancelGrading" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <GradeSubmissionForm 
            :submissionId="selectedSubmission.id"
            @success="handleGradeSuccess"
            @cancel="cancelGrading"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../store/auth'
import { SubmissionList, SubmitAssignmentForm, GradeSubmissionForm } from '../components'
import { submissionApi } from '../api'
import type { StudentSubmissionResponse, TeacherSubmissionResponse } from '../types'

const route = useRoute()
const router = useRouter()
const { user } = useAuth()

const activeTab = ref('list')

// 根据用户角色和参数设置默认标签页
const getDefaultTab = () => {
  // 所有情况都默认显示提交列表
  return 'list'
}
const submissionListRef = ref()
const classId = ref<number | undefined>()
const assignmentId = ref<number | undefined>()
const studentId = ref<number | undefined>()
const isGrading = ref(false)

const getListTitle = () => {
  if (classId.value) return '班级提交'
  if (assignmentId.value) {
    return user?.role === 'teacher' ? '任务提交' : '我的提交记录'
  }
  if (studentId.value) return '学生提交'
  return user?.role === 'teacher' ? '学生提交' : '我的提交'
}

const shouldShowSubmitTab = () => {
  // 学生只有在有具体任务ID时才显示提交作业标签页
  return user?.role === 'student' && assignmentId.value
}


const handleViewSubmission = async (submission: StudentSubmissionResponse | TeacherSubmissionResponse) => {
  // 跳转到新的提交详情页面
  console.log('Navigating to submission detail:', submission.id)
  console.log('Full submission object:', submission)
  router.push(`/submissions/${submission.id}`)
}

const closeModal = () => {
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
  if (route.params.classId) {
    classId.value = parseInt(route.params.classId as string)
  } else if (route.query.classId) {
    classId.value = parseInt(route.query.classId as string)
  }
  
  if (route.params.assignmentId) {
    assignmentId.value = parseInt(route.params.assignmentId as string)
  } else if (route.query.assignmentId) {
    assignmentId.value = parseInt(route.query.assignmentId as string)
  }
  
  if (route.query.studentId) {
    studentId.value = parseInt(route.query.studentId as string)
  }
  
  console.log('SubmissionManagement mounted with params:', {
    classId: classId.value,
    assignmentId: assignmentId.value,
    studentId: studentId.value,
    userRole: user?.role
  })
  
  // 设置默认标签页
  activeTab.value = getDefaultTab()
})

// 监听参数变化，自动刷新数据
watch([classId, assignmentId, studentId], async () => {
  if (submissionListRef.value) {
    await nextTick()
    submissionListRef.value.refreshSubmissions()
  }
}, { immediate: true })

// 监听submissionListRef变化，确保组件挂载后刷新数据
watch(submissionListRef, async (newRef) => {
  if (newRef && (classId.value || assignmentId.value || studentId.value)) {
    await nextTick()
    newRef.refreshSubmissions()
  }
})
</script>

<style scoped>
.submission-management {
  min-height: 100vh;
  background: var(--color-background-light);
}

.page-header {
  background: var(--color-background);
  border-bottom: 1px solid var(--color-border);
  padding: var(--spacing-8) 0;
  margin-bottom: var(--spacing-8);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-6);
  text-align: center;
}

.page-title {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-2) 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-3);
}

.page-title .icon {
  font-size: var(--font-size-2xl);
}

.page-subtitle {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin: 0;
}

.header-divider {
  height: 4px;
  background: linear-gradient(90deg, var(--color-primary-light), var(--color-primary), var(--color-primary-light));
  margin-top: var(--spacing-6);
  border-radius: 2px;
}

.tabs-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-6);
  margin-bottom: var(--spacing-8);
}

.tabs {
  display: flex;
  background: var(--color-background);
  border-radius: var(--radius-lg);
  padding: var(--spacing-2);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

.tab {
  flex: 1;
  background: none;
  border: none;
  padding: var(--spacing-4) var(--spacing-6);
  cursor: pointer;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
  transition: all var(--transition-fast);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-2);
}

.tab:hover {
  color: var(--color-text-primary);
  background: var(--color-background-muted);
}

.tab.active {
  color: var(--color-primary);
  background: var(--color-primary-light);
  box-shadow: var(--shadow-sm);
}

.tab .icon {
  font-size: var(--font-size-lg);
}

.tab-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-6);
}

.tab-pane {
  background: var(--color-background);
  border-radius: var(--radius-lg);
  padding: var(--spacing-8);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
  min-height: 400px;
}

.form-container {
  max-width: 600px;
  margin: 0 auto;
}

/* 小卡片样式 */
.card-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.submission-card {
  background: var(--color-background);
  border-radius: var(--radius-xl);
  width: 90%;
  max-width: 500px;
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--color-border);
  overflow: hidden;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-6);
  border-bottom: 1px solid var(--color-border);
  background: var(--color-background-muted);
}

.card-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: var(--font-size-2xl);
  cursor: pointer;
  color: var(--color-text-secondary);
  padding: var(--spacing-2);
  border-radius: var(--radius-base);
  transition: all var(--transition-fast);
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: var(--color-text-primary);
  background: var(--color-background-light);
}

.card-content {
  padding: var(--spacing-6);
}

.submission-info {
  margin-bottom: var(--spacing-6);
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-3) 0;
  border-bottom: 1px solid var(--color-border-light);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  min-width: 80px;
}

.student-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-sm);
  flex-shrink: 0;
}

.status-badge {
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  display: inline-block;
}

.status-badge.graded {
  background: var(--color-success-light);
  color: var(--color-success);
}

.status-badge.pending {
  background: var(--color-warning-light);
  color: var(--color-warning);
}

.score-badge {
  background: var(--color-success-light);
  color: var(--color-success);
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  display: inline-block;
}

.no-score-badge {
  background: var(--color-background-muted);
  color: var(--color-text-secondary);
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  display: inline-block;
}

/* 批改报告样式 */
.report-section {
  grid-column: 1 / -1;
  margin-top: var(--spacing-4);
  padding-top: var(--spacing-4);
  border-top: 1px solid var(--color-border-light);
}

.report-content {
  background: var(--color-background-muted);
  border-radius: var(--radius-lg);
  padding: var(--spacing-4);
  margin-top: var(--spacing-2);
  border: 1px solid var(--color-border);
}

.report-text {
  font-size: var(--font-size-base);
  line-height: 1.6;
  color: var(--color-text-primary);
  white-space: pre-wrap;
  word-break: break-word;
}

.report-meta {
  margin-top: var(--spacing-3);
  padding-top: var(--spacing-3);
  border-top: 1px solid var(--color-border-light);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-style: italic;
}

.card-actions {
  display: flex;
  gap: var(--spacing-3);
  padding-top: var(--spacing-4);
  border-top: 1px solid var(--color-border-light);
}

.btn-action {
  flex: 1;
  padding: var(--spacing-3) var(--spacing-4);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-2);
  border: 1px solid transparent;
}

.btn-download {
  background: var(--color-background-muted);
  color: var(--color-text-primary);
  border-color: var(--color-border);
}

.btn-download:hover:not(:disabled) {
  background: var(--color-primary-light);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.btn-grade {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.btn-grade:hover:not(:disabled) {
  background: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.btn-cancel {
  background: var(--color-danger-light);
  color: var(--color-danger);
  border-color: var(--color-danger-light);
}

.btn-cancel:hover:not(:disabled) {
  background: var(--color-danger);
  color: white;
  border-color: var(--color-danger);
}

.btn-action:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.icon {
  font-style: normal;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal {
  background: var(--color-background);
  border-radius: var(--radius-xl);
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--color-border);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-6);
  border-bottom: 1px solid var(--color-border);
}

.modal-header h3 {
  margin: 0;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.modal-body {
  padding: var(--spacing-6);
}
</style>
