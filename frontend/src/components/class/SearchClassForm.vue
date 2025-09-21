<template>
  <form @submit.prevent="handleSubmit" class="form">
    <h2>搜索班级</h2>
    
    <div v-if="error" class="alert alert-error">
      {{ error }}
    </div>

    <div class="form-group">
      <label for="searchTerm" class="form-label">搜索关键词</label>
      <input
        id="searchTerm"
        v-model="form.search_term"
        type="text"
        class="form-input"
        placeholder="请输入班级名称或班级代码"
        required
        :disabled="isLoading"
      />
    </div>

    <div class="form-actions">
      <button
        type="submit"
        class="btn btn-primary"
        :disabled="isLoading"
      >
        <span v-if="isLoading">搜索中...</span>
        <span v-else>搜索班级</span>
      </button>
    </div>

    <!-- 搜索结果 -->
    <div v-if="searchResults.length > 0" class="search-results">
      <h3>搜索结果</h3>
      <div class="result-list">
        <div 
          v-for="classItem in searchResults" 
          :key="classItem.id"
          class="result-item"
        >
          <div class="result-content">
            <h4>{{ classItem.name }}</h4>
            <p class="class-code">班级代码: {{ classItem.class_code }}</p>
            <p class="description">{{ classItem.description || '暂无描述' }}</p>
            <p class="teacher">教师: {{ classItem.teacher_name }}</p>
          </div>
          <div class="result-actions">
            <button 
              @click="joinClass(classItem.id)"
              class="btn btn-outline btn-sm"
              :disabled="isLoading"
            >
              {{ user?.role === 'teacher' ? '作为助教加入' : '加入班级' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="hasSearched && searchResults.length === 0" class="no-results">
      <p>未找到相关班级</p>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { classApi } from '../../api'
import { useAuth } from '../../store/auth'
import type { ClassResponse, ClassSearch } from '../../types'

const emit = defineEmits<{
  success: [data: any]
}>()

const { user } = useAuth()

const form = reactive<ClassSearch>({
  search_term: ''
})

const searchResults = ref<ClassResponse[]>([])
const error = ref<string | null>(null)
const isLoading = ref(false)
const hasSearched = ref(false)

const handleSubmit = async () => {
  error.value = null
  
  if (!form.search_term.trim()) {
    error.value = '请输入搜索关键词'
    return
  }

  isLoading.value = true
  hasSearched.value = true
  
  try {
    const results = await classApi.search(form)
    searchResults.value = results
  } catch (err: any) {
    console.error('Search classes error:', err)
    error.value = err.response?.data?.detail || '搜索班级失败'
    searchResults.value = []
  } finally {
    isLoading.value = false
  }
}

const joinClass = async (classId: number) => {
  try {
    isLoading.value = true
    
    // 根据用户角色选择加入方式
    const result = user?.role === 'teacher' 
      ? await classApi.joinAsTeacher({ class_id: classId })
      : await classApi.joinAsStudent({ class_id: classId })
    
    emit('success', result)
    // 清空搜索结果
    searchResults.value = []
    form.search_term = ''
    hasSearched.value = false
  } catch (err: any) {
    console.error('Join class error:', err)
    error.value = err.response?.data?.detail || '加入班级失败'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.search-results {
  margin-top: var(--spacing-8);
}

.search-results h3 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-4);
}

.result-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-4);
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
}

.result-item:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-sm);
}

.result-content h4 {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-2) 0;
}

.result-content p {
  margin: var(--spacing-1) 0;
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.class-code {
  font-weight: var(--font-weight-medium);
  color: var(--color-primary);
}

.no-results {
  text-align: center;
  padding: var(--spacing-8);
  color: var(--color-text-secondary);
  font-size: var(--font-size-lg);
}
</style>
