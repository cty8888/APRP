<template>
  <div class="class-list">
    <div class="class-list-header">
      <h2>我的班级</h2>
      <button @click="refreshClasses" class="btn btn-outline" :disabled="isLoading">
        刷新
      </button>
    </div>

    <div v-if="isLoading" class="loading">
      加载中...
    </div>

    <div v-else-if="classes.length === 0" class="empty-state">
      暂无班级
    </div>

    <div v-else class="class-grid">
      <div 
        v-for="classItem in classes" 
        :key="classItem.id" 
        class="class-card"
        @click="$emit('selectClass', classItem)"
      >
        <div class="class-card-header">
          <h3>{{ classItem.name }}</h3>
          <span class="class-role">{{ getRoleText(classItem.my_role) }}</span>
        </div>
        
        <div class="class-card-body">
          <p v-if="classItem.description">{{ classItem.description }}</p>
          <div class="class-info">
            <span>班级代码: {{ classItem.class_code }}</span>
            <span>学生数量: {{ classItem.student_count }}</span>
          </div>
          <div class="class-meta">
            <span>教师: {{ classItem.teacher_name }}</span>
            <span>创建时间: {{ formatDate(classItem.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { classApi } from '../../api'
import type { ClassResponse } from '../../types'

defineEmits<{
  selectClass: [classItem: ClassResponse]
}>()

const classes = ref<ClassResponse[]>([])
const isLoading = ref(false)

const getRoleText = (role: string) => {
  switch (role) {
    case 'main_teacher': return '主教师'
    case 'assistant_teacher': return '助教'
    case 'student': return '学生'
    default: return role
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const refreshClasses = async () => {
  isLoading.value = true
  try {
    classes.value = await classApi.getMyClasses()
  } catch (error) {
    console.error('Failed to load classes:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  refreshClasses()
})

// 暴露刷新方法给父组件
defineExpose({
  refreshClasses
})
</script>

<style scoped>
.class-list-header {
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

.class-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.class-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.class-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.class-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.class-card-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.4rem;
}

.class-role {
  background: #007bff;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.9rem;
}

.class-card-body p {
  color: #666;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.class-info, .class-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.class-info span, .class-meta span {
  color: #888;
  font-size: 1rem;
}
</style>
