<template>
  <div class="submission-list">
    <div class="submission-list-header">
      <h2 class="section-title">
        <i class="icon">📋</i>
        {{ title }}
      </h2>
      <button @click="refreshSubmissions" class="btn-refresh" :disabled="isLoading">
        <i class="icon">🔄</i>
        刷新
      </button>
    </div>

    <div v-if="isLoading" class="loading">
      加载中...
    </div>

    <div v-else-if="submissions.length === 0" class="empty-state">
      暂无提交记录
    </div>

    <div v-else class="submission-table">
      <table>
        <thead>
          <tr>
            <th>任务名称</th>
            <th>班级</th>
            <th v-if="isTeacherView">学生</th>
            <th>提交时间</th>
            <th>分数</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="submission in submissions" 
            :key="submission.id"
            class="table-row"
          >
            <td class="text-center">{{ submission.assignment_title }}</td>
            <td class="text-center">{{ submission.class_name }}</td>
            <td v-if="isTeacherView" class="text-center">
              <div class="student-info">
                <div class="avatar">{{ getInitials((submission as TeacherSubmissionResponse).student_name) }}</div>
                <span>{{ (submission as TeacherSubmissionResponse).student_name }}</span>
              </div>
            </td>
            <td class="text-center">{{ formatDate(submission.submitted_at) }}</td>
            <td class="text-center">
              <span v-if="submission.score !== null" class="score-badge">
                {{ submission.score }}分
              </span>
              <span v-else class="no-score-badge">未批改</span>
            </td>
            <td class="text-center">
              <span :class="['status-badge', submission.is_graded ? 'graded' : 'pending']">
                {{ submission.is_graded ? '已批改' : '待批改' }}
              </span>
            </td>
            <td class="text-center">
              <button 
                @click="$emit('viewSubmission', submission)" 
                class="btn-detail"
              >
                <i class="icon">👁️</i>
                查看详情
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { submissionApi } from '../../api'
import type { StudentSubmissionResponse, TeacherSubmissionResponse } from '../../types'

interface Props {
  title?: string
  isTeacherView?: boolean
  classId?: number
  assignmentId?: number
  studentId?: number
}

const props = withDefaults(defineProps<Props>(), {
  title: '提交列表',
  isTeacherView: false
})

defineEmits<{
  viewSubmission: [submission: StudentSubmissionResponse | TeacherSubmissionResponse]
}>()

const submissions = ref<(StudentSubmissionResponse | TeacherSubmissionResponse)[]>([])
const isLoading = ref(false)

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

const getInitials = (name: string) => {
  if (!name) return '?'
  return name.charAt(0).toUpperCase()
}

const refreshSubmissions = async () => {
  isLoading.value = true
  try {
    console.log('SubmissionList refreshSubmissions:', {
      isTeacherView: props.isTeacherView,
      classId: props.classId,
      assignmentId: props.assignmentId,
      studentId: props.studentId
    })
    
    if (props.isTeacherView) {
      if (props.assignmentId) {
        console.log('Teacher: Loading assignment submissions for assignmentId:', props.assignmentId)
        submissions.value = await submissionApi.getAssignmentSubmissions(props.assignmentId)
      } else if (props.classId) {
        console.log('Teacher: Loading class submissions for classId:', props.classId)
        submissions.value = await submissionApi.getClassSubmissions(props.classId)
      } else if (props.studentId) {
        console.log('Teacher: Loading student submissions for studentId:', props.studentId)
        submissions.value = await submissionApi.getStudentSubmissions(props.studentId)
      }
    } else {
      if (props.assignmentId) {
        console.log('Student: Loading my submissions for assignmentId:', props.assignmentId)
        submissions.value = await submissionApi.getMySubmissionsByAssignment(props.assignmentId)
      } else if (props.classId) {
        console.log('Student: Loading my submissions for classId:', props.classId)
        submissions.value = await submissionApi.getMySubmissionsByClass(props.classId)
      } else {
        console.log('Student: Loading all my submissions')
        submissions.value = await submissionApi.getMySubmissions()
      }
    }
    
    console.log('Loaded submissions:', submissions.value.length, 'items')
  } catch (error) {
    console.error('Failed to load submissions:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  refreshSubmissions()
})

// 暴露刷新方法给父组件
defineExpose({
  refreshSubmissions
})
</script>

<style scoped>
.submission-list {
  background: var(--color-background);
  border-radius: var(--radius-xl);
  padding: var(--spacing-8);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

.submission-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-8);
  padding-bottom: var(--spacing-4);
  border-bottom: 2px solid var(--color-border-light);
}

.section-title {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin: 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
}

.section-title .icon {
  font-size: var(--font-size-xl);
}

.btn-refresh {
  background: var(--color-background-muted);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-3) var(--spacing-4);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-2);
  height: 40px;
}

.btn-refresh:hover:not(:disabled) {
  background: var(--color-primary-light);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.btn-refresh:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading, .empty-state {
  text-align: center;
  padding: var(--spacing-12);
  color: var(--color-text-secondary);
  font-size: var(--font-size-lg);
}

.submission-table {
  background: var(--color-background);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: var(--spacing-6);
  text-align: center;
  border-bottom: 1px solid var(--color-border-light);
}

th {
  background: var(--color-background-muted);
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-base);
  color: var(--color-text-primary);
}

.table-row {
  transition: all var(--transition-fast);
}

.table-row:hover {
  background: var(--color-background-light);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.text-center {
  text-align: center;
}

.student-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
  justify-content: center;
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

.btn-detail {
  background: var(--color-primary);
  color: white;
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-md);
  padding: var(--spacing-2) var(--spacing-4);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-2);
}

.btn-detail:hover:not(:disabled) {
  background: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.btn-detail:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.icon {
  font-style: normal;
}
</style>
