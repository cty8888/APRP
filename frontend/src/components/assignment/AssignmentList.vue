<template>
  <div class="assignment-list">
    <div class="assignment-list-header">
      <h2 class="section-title">
        <i class="icon">📋</i>
        {{ title }}
      </h2>
      <button @click="refreshAssignments" class="btn-refresh" :disabled="isLoading">
        <i class="icon">🔄</i>
        刷新
      </button>
    </div>

    <div v-if="isLoading" class="loading">
      加载中...
    </div>

    <div v-else-if="assignments.length === 0" class="empty-state">
      暂无任务
    </div>

    <div v-else class="assignment-list">
      <div 
        v-for="assignment in assignments" 
        :key="assignment.id" 
        class="assignment-item"
        @click="$emit('selectAssignment', assignment)"
      >
        <div class="assignment-content">
          <div class="assignment-main">
            <h3 class="assignment-title">{{ assignment.title }}</h3>
            <p class="assignment-description">{{ assignment.description || '暂无描述' }}</p>
            <div class="assignment-meta">
              <span class="meta-item">
                <i class="icon">👨‍🏫</i>
                {{ assignment.teacher_name }}
              </span>
              <span class="meta-item">
                <i class="icon">📅</i>
                {{ formatDate(assignment.created_at) }}
              </span>
            </div>
          </div>
          
          <div class="assignment-actions">
            <!-- 学生操作 -->
            <template v-if="user?.role === 'student'">
              <button 
                @click.stop="submitAssignment(assignment)"
                class="btn btn-primary"
              >
                提交作业
              </button>
            </template>
            
            <!-- 老师操作 -->
            <template v-if="user?.role === 'teacher'">
              <button 
                @click.stop="viewSubmissions(assignment)"
                class="btn btn-primary"
              >
                查看提交
              </button>
              <button 
                v-if="canEditAssignment(assignment)"
                @click.stop="editAssignment(assignment)"
                class="btn btn-outline"
              >
                编辑
              </button>
              <button 
                v-if="canEditAssignment(assignment)"
                @click.stop="deleteAssignment(assignment.id)"
                class="btn btn-danger"
              >
                删除
              </button>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { assignmentApi } from '../../api'
import { useAuth } from '../../store/auth'
import type { AssignmentResponse } from '../../types'

interface Props {
  title?: string
  classId?: number
}

const props = withDefaults(defineProps<Props>(), {
  title: '任务列表'
})

const { user } = useAuth()

const emit = defineEmits<{
  selectAssignment: [assignment: AssignmentResponse]
  editAssignment: [assignment: AssignmentResponse]
  assignmentDeleted: [assignmentId: number]
  submitAssignment: [assignment: AssignmentResponse]
  viewSubmissions: [assignment: AssignmentResponse]
}>()

const assignments = ref<AssignmentResponse[]>([])
const isLoading = ref(false)

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const refreshAssignments = async () => {
  isLoading.value = true
  try {
    if (props.classId) {
      assignments.value = await assignmentApi.getClassAssignments(props.classId)
    } else {
      assignments.value = await assignmentApi.getMyAssignments()
    }
  } catch (error) {
    console.error('Failed to load assignments:', error)
  } finally {
    isLoading.value = false
  }
}

const canEditAssignment = (assignment: AssignmentResponse) => {
  // 只有教师可以编辑任务，且必须是任务的创建者
  return user?.role === 'teacher' && assignment.teacher_id === user.id
}

const editAssignment = (assignment: AssignmentResponse) => {
  emit('editAssignment', assignment)
}

const deleteAssignment = async (assignmentId: number) => {
  if (!confirm('确定要删除这个任务吗？此操作不可撤销。')) {
    return
  }
  
  try {
    await assignmentApi.delete(assignmentId)
    // 刷新任务列表
    await refreshAssignments()
    emit('assignmentDeleted', assignmentId)
  } catch (error) {
    console.error('Failed to delete assignment:', error)
    alert('删除任务失败，请重试')
  }
}

const submitAssignment = (assignment: AssignmentResponse) => {
  emit('submitAssignment', assignment)
}

const viewSubmissions = (assignment: AssignmentResponse) => {
  emit('viewSubmissions', assignment)
}

onMounted(() => {
  refreshAssignments()
})

// 暴露刷新方法给父组件
defineExpose({
  refreshAssignments
})
</script>

<style scoped>
.assignment-list-header {
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

.icon {
  font-style: normal;
}

.loading, .empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 1.2rem;
}

.assignment-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.assignment-item {
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-6);
  cursor: pointer;
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-sm);
}

.assignment-item:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.assignment-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--spacing-6);
}

.assignment-main {
  flex: 1;
  min-width: 0;
}

.assignment-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-2) 0;
  line-height: 1.3;
}

.assignment-description {
  color: var(--color-text-secondary);
  font-size: var(--font-size-base);
  margin: 0 0 var(--spacing-4) 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.assignment-meta {
  display: flex;
  gap: var(--spacing-6);
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
}

.meta-item .icon {
  font-size: var(--font-size-base);
}

.assignment-actions {
  display: flex;
  gap: var(--spacing-3);
  flex-shrink: 0;
}

.btn-danger {
  background-color: var(--color-danger);
  color: white;
  border: 1px solid var(--color-danger);
}

.btn-danger:hover:not(:disabled) {
  background-color: var(--color-danger-hover);
  border-color: var(--color-danger-hover);
}

.btn-outline {
  background-color: transparent;
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

.btn-outline:hover:not(:disabled) {
  background-color: var(--color-background-muted);
  border-color: var(--color-text-primary);
}

.btn {
  padding: var(--spacing-3) var(--spacing-4);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  border: 1px solid transparent;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
