<template>
  <div class="assignment-list">
    <div class="assignment-list-header">
      <h2>{{ title }}</h2>
      <button @click="refreshAssignments" class="btn btn-outline" :disabled="isLoading">
        刷新
      </button>
    </div>

    <div v-if="isLoading" class="loading">
      加载中...
    </div>

    <div v-else-if="assignments.length === 0" class="empty-state">
      暂无任务
    </div>

    <div v-else class="assignment-grid">
      <div 
        v-for="assignment in assignments" 
        :key="assignment.id" 
        class="assignment-card"
        @click="$emit('selectAssignment', assignment)"
      >
        <div class="assignment-card-header">
          <h3>{{ assignment.title }}</h3>
          <span class="assignment-class">{{ assignment.class_name }}</span>
        </div>
        
        <div class="assignment-card-body">
          <p v-if="assignment.description">{{ assignment.description }}</p>
          <div class="assignment-meta">
            <span>教师: {{ assignment.teacher_name }}</span>
            <span>创建时间: {{ formatDate(assignment.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { assignmentApi } from '../../api'
import type { AssignmentResponse } from '../../types'

interface Props {
  title?: string
  classId?: number
}

const props = withDefaults(defineProps<Props>(), {
  title: '任务列表'
})

defineEmits<{
  selectAssignment: [assignment: AssignmentResponse]
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
  margin-bottom: 2rem;
}

.loading, .empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 1.2rem;
}

.assignment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.assignment-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.assignment-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.assignment-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.assignment-card-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.4rem;
}

.assignment-class {
  background: #28a745;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.9rem;
}

.assignment-card-body p {
  color: #666;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.assignment-meta {
  display: flex;
  justify-content: space-between;
}

.assignment-meta span {
  color: #888;
  font-size: 1rem;
}
</style>
