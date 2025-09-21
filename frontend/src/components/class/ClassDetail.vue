<template>
  <div class="class-detail">
    <!-- 班级头部信息 -->
    <div class="class-header">
      <div class="class-main-info">
        <h1 class="class-title">{{ classData.name }}</h1>
        <p v-if="classData.description" class="class-description">{{ classData.description }}</p>
        <div class="class-meta">
          <span class="meta-item">
            <i class="icon">🔑</i>
            班级代码: {{ classData.class_code }}
          </span>
          <span class="meta-item">
            <i class="icon">👥</i>
            学生人数: {{ classData.student_count }}人
          </span>
          <span class="meta-item">
            <i class="icon">👨‍🏫</i>
            主教师: {{ classData.teacher_name }}
          </span>
          <span class="meta-item">
            <i class="icon">📅</i>
            创建时间: {{ formatDate(classData.created_at) }}
          </span>
        </div>
      </div>
      
      <div class="class-actions" v-if="canEdit">
        <button 
          @click="editClass"
          class="btn btn-primary btn-lg"
        >
          <i class="icon">✏️</i>
          编辑班级信息
        </button>
      </div>
    </div>

    <!-- 班级统计信息 -->
    <div class="class-stats">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">📚</div>
          <div class="stat-content">
            <div class="stat-label">任务总数</div>
            <div class="stat-value">{{ stats.totalAssignments }}</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">📝</div>
          <div class="stat-content">
            <div class="stat-label">提交总数</div>
            <div class="stat-value">{{ stats.totalSubmissions }}</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">✅</div>
          <div class="stat-content">
            <div class="stat-label">已批改</div>
            <div class="stat-value">{{ stats.gradedSubmissions }}</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon">⏳</div>
          <div class="stat-content">
            <div class="stat-label">待批改</div>
            <div class="stat-value">{{ stats.ungradedSubmissions }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 任务列表 -->
    <div class="assignments-section">
      <div class="section-header">
        <h2 class="section-title">
          <i class="icon">📋</i>
          班级任务
        </h2>
        <button 
          v-if="user?.role === 'teacher'"
          @click="createAssignment"
          class="btn btn-outline"
        >
          <i class="icon">➕</i>
          创建任务
        </button>
      </div>
      
      <div v-if="isLoading" class="loading">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>
      
      <div v-else-if="assignments.length === 0" class="empty-state">
        <div class="empty-icon">📝</div>
        <h3>暂无任务</h3>
        <p>还没有创建任何任务</p>
        <button 
          v-if="user?.role === 'teacher'"
          @click="createAssignment"
          class="btn btn-primary"
        >
          创建第一个任务
        </button>
      </div>
      
      <div v-else class="assignments-list">
        <div 
          v-for="assignment in assignments" 
          :key="assignment.id" 
          class="assignment-item"
          @click="selectAssignment(assignment)"
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
                  <i class="icon">📤</i>
                  提交作业
                </button>
              </template>
              
              <!-- 老师操作 -->
              <template v-if="user?.role === 'teacher'">
                <button 
                  @click.stop="viewSubmissions(assignment)"
                  class="btn btn-primary"
                >
                  <i class="icon">👁️</i>
                  查看提交
                </button>
                <button 
                  v-if="canEditAssignment(assignment)"
                  @click.stop="editAssignment(assignment)"
                  class="btn btn-outline"
                >
                  <i class="icon">✏️</i>
                  编辑
                </button>
                <button 
                  v-if="canEditAssignment(assignment)"
                  @click.stop="deleteAssignment(assignment.id)"
                  class="btn btn-danger"
                >
                  <i class="icon">🗑️</i>
                  删除
                </button>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuth } from '../../store/auth'
import { assignmentApi } from '../../api'
import type { ClassResponse, AssignmentResponse } from '../../types'

interface Props {
  classData: ClassResponse
}

const props = defineProps<Props>()

const emit = defineEmits<{
  editClass: [classData: ClassResponse]
  createAssignment: []
  selectAssignment: [assignment: AssignmentResponse]
  submitAssignment: [assignment: AssignmentResponse]
  viewSubmissions: [assignment: AssignmentResponse]
  editAssignment: [assignment: AssignmentResponse]
  deleteAssignment: [assignmentId: number]
}>()

const { user } = useAuth()

const assignments = ref<AssignmentResponse[]>([])
const isLoading = ref(false)

const canEdit = computed(() => {
  return user?.role === 'teacher' && props.classData.my_role === 'main_teacher'
})

const stats = ref({
  totalAssignments: 0,
  totalSubmissions: 0,
  gradedSubmissions: 0,
  ungradedSubmissions: 0
})

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const canEditAssignment = (assignment: AssignmentResponse) => {
  return user?.role === 'teacher' && assignment.teacher_id === user.id
}

const loadAssignments = async () => {
  isLoading.value = true
  try {
    assignments.value = await assignmentApi.getClassAssignments(props.classData.id)
    stats.value.totalAssignments = assignments.value.length
  } catch (error) {
    console.error('Failed to load assignments:', error)
  } finally {
    isLoading.value = false
  }
}

const editClass = () => {
  emit('editClass', props.classData)
}

const createAssignment = () => {
  emit('createAssignment')
}

const selectAssignment = (assignment: AssignmentResponse) => {
  emit('selectAssignment', assignment)
}

const submitAssignment = (assignment: AssignmentResponse) => {
  emit('submitAssignment', assignment)
}

const viewSubmissions = (assignment: AssignmentResponse) => {
  emit('viewSubmissions', assignment)
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
    await loadAssignments()
    emit('deleteAssignment', assignmentId)
  } catch (error) {
    console.error('Failed to delete assignment:', error)
    alert('删除任务失败，请重试')
  }
}

onMounted(() => {
  loadAssignments()
})
</script>

<style scoped>
.class-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-6);
}

.class-header {
  background: var(--color-background);
  border-radius: var(--radius-xl);
  padding: var(--spacing-8);
  margin-bottom: var(--spacing-8);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--spacing-6);
}

.class-main-info {
  flex: 1;
}

.class-title {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-3) 0;
  line-height: 1.2;
}

.class-description {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin: 0 0 var(--spacing-6) 0;
  line-height: 1.5;
}

.class-meta {
  display: flex;
  gap: var(--spacing-6);
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  color: var(--color-text-secondary);
  font-size: var(--font-size-base);
}

.meta-item .icon {
  font-size: var(--font-size-lg);
}

.class-actions {
  flex-shrink: 0;
}

.class-stats {
  background: var(--color-background);
  border-radius: var(--radius-xl);
  padding: var(--spacing-8);
  margin-bottom: var(--spacing-8);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-6);
}

.stat-card {
  background: var(--color-background-light);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-6);
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
  transition: all var(--transition-fast);
}

.stat-card:hover {
  background: var(--color-background-muted);
  border-color: var(--color-primary-light);
  transform: translateY(-1px);
}

.stat-icon {
  font-size: var(--font-size-3xl);
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary-light);
  border-radius: var(--radius-lg);
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-1);
  font-weight: var(--font-weight-medium);
}

.stat-value {
  font-size: var(--font-size-2xl);
  color: var(--color-text-primary);
  font-weight: var(--font-weight-bold);
}

.assignments-section {
  background: var(--color-background);
  border-radius: var(--radius-xl);
  padding: var(--spacing-8);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-6);
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

.loading {
  text-align: center;
  padding: var(--spacing-12);
  color: var(--color-text-secondary);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--color-border);
  border-top: 4px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto var(--spacing-4);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: var(--spacing-12);
  color: var(--color-text-secondary);
}

.empty-icon {
  font-size: var(--font-size-6xl);
  margin-bottom: var(--spacing-4);
}

.empty-state h3 {
  font-size: var(--font-size-xl);
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-2) 0;
}

.empty-state p {
  margin: 0 0 var(--spacing-6) 0;
}

.assignments-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
}

.assignment-item {
  background: var(--color-background-light);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-6);
  cursor: pointer;
  transition: all var(--transition-fast);
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

.assignment-actions {
  display: flex;
  gap: var(--spacing-3);
  flex-shrink: 0;
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
  gap: var(--spacing-2);
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

.btn-outline {
  background-color: transparent;
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

.btn-outline:hover:not(:disabled) {
  background-color: var(--color-background-muted);
  border-color: var(--color-text-primary);
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

.btn-lg {
  padding: var(--spacing-4) var(--spacing-6);
  font-size: var(--font-size-base);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.icon {
  font-style: normal;
}

@media (max-width: 768px) {
  .class-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .class-meta {
    flex-direction: column;
    gap: var(--spacing-3);
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .assignment-content {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .assignment-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>
