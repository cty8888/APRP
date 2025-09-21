<template>
  <div class="class-students-list">
    <div class="students-header">
      <h3>{{ classInfo.name }} - 学生列表</h3>
      <button @click="$emit('close')" class="btn btn-outline btn-sm">
        关闭
      </button>
    </div>

    <div v-if="isLoading" class="loading">
      加载中...
    </div>

    <div v-else-if="students.length === 0" class="empty-state">
      暂无学生
    </div>

    <div v-else class="students-grid">
      <div 
        v-for="student in students" 
        :key="student.id"
        class="student-card"
      >
        <div class="student-info">
          <h4>{{ student.name }}</h4>
          <p class="student-email">{{ student.email }}</p>
          <p class="join-date">加入时间: {{ formatDate(student.joined_at) }}</p>
        </div>
        <div class="student-actions">
          <button 
            @click="viewStudentSubmissions(student)"
            class="btn btn-outline btn-sm"
          >
            查看提交
          </button>
          <span class="student-role">学生</span>
        </div>
      </div>
    </div>

    <div class="students-footer">
      <p class="student-count">共 {{ students.length }} 名学生</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { classApi } from '../../api'

interface Props {
  classId: number
  classInfo: {
    id: number
    name: string
  }
}

const props = defineProps<Props>()

const emit = defineEmits<{
  close: []
  viewStudentSubmissions: [student: any]
}>()

const students = ref<any[]>([])
const isLoading = ref(false)

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const loadStudents = async () => {
  isLoading.value = true
  try {
    const result = await classApi.getClassStudents(props.classId)
    students.value = result.students || []
  } catch (error) {
    console.error('Failed to load students:', error)
    students.value = []
  } finally {
    isLoading.value = false
  }
}

const viewStudentSubmissions = (student: any) => {
  emit('viewStudentSubmissions', student)
}

onMounted(() => {
  loadStudents()
})
</script>

<style scoped>
.class-students-list {
  background: var(--color-background);
  border-radius: var(--radius-lg);
  padding: var(--spacing-6);
  max-width: 800px;
  max-height: 600px;
  overflow-y: auto;
}

.students-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-6);
  padding-bottom: var(--spacing-4);
  border-bottom: 1px solid var(--color-border);
}

.students-header h3 {
  margin: 0;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.loading, .empty-state {
  text-align: center;
  padding: var(--spacing-8);
  color: var(--color-text-secondary);
  font-size: var(--font-size-lg);
}

.students-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-4);
  margin-bottom: var(--spacing-6);
}

.student-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-4);
  background: var(--color-background-muted);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.student-card:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-sm);
}

.student-info h4 {
  margin: 0 0 var(--spacing-2) 0;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.student-info p {
  margin: var(--spacing-1) 0;
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.student-email {
  font-weight: var(--font-weight-medium);
}

.student-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
}

.student-role {
  padding: var(--spacing-1) var(--spacing-3);
  background: var(--color-primary);
  color: white;
  border-radius: var(--radius-base);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.students-footer {
  text-align: center;
  padding-top: var(--spacing-4);
  border-top: 1px solid var(--color-border);
}

.student-count {
  margin: 0;
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-medium);
}
</style>
