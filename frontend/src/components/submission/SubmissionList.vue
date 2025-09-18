<template>
  <div class="submission-list">
    <div class="submission-list-header">
      <h2>{{ title }}</h2>
      <button @click="refreshSubmissions" class="btn btn-outline" :disabled="isLoading">
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
          >
            <td>{{ submission.assignment_title }}</td>
            <td>{{ submission.class_name }}</td>
            <td v-if="isTeacherView">{{ (submission as TeacherSubmissionResponse).student_name }}</td>
            <td>{{ formatDate(submission.submitted_at) }}</td>
            <td>
              <span v-if="submission.score !== null" class="score">
                {{ submission.score }}分
              </span>
              <span v-else class="no-score">未批改</span>
            </td>
            <td>
              <span :class="['status', submission.is_graded ? 'graded' : 'pending']">
                {{ submission.is_graded ? '已批改' : '待批改' }}
              </span>
            </td>
            <td>
              <button 
                @click="$emit('viewSubmission', submission)" 
                class="btn btn-small"
              >
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

const refreshSubmissions = async () => {
  isLoading.value = true
  try {
    if (props.isTeacherView) {
      if (props.assignmentId) {
        submissions.value = await submissionApi.getAssignmentSubmissions(props.assignmentId)
      } else if (props.classId) {
        submissions.value = await submissionApi.getClassSubmissions(props.classId)
      } else if (props.studentId) {
        submissions.value = await submissionApi.getStudentSubmissions(props.studentId)
      }
    } else {
      if (props.classId) {
        submissions.value = await submissionApi.getMySubmissionsByClass(props.classId)
      } else if (props.assignmentId) {
        submissions.value = await submissionApi.getMySubmissionsByAssignment(props.assignmentId)
      } else {
        submissions.value = await submissionApi.getMySubmissions()
      }
    }
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
.submission-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.loading, .empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 1.2rem;
}

.submission-table {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #e9ecef;
}

th {
  background-color: #f8f9fa;
  font-weight: 600;
  font-size: 1.1rem;
}

td {
  font-size: 1rem;
}

.score {
  color: #28a745;
  font-weight: 600;
}

.no-score {
  color: #6c757d;
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

.btn-small {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}
</style>
