<template>
  <form @submit.prevent="handleSubmit" class="form">
    <h2>加入班级</h2>
    
    <div v-if="error" class="alert alert-error">
      {{ error }}
    </div>

    <div class="form-group">
      <label for="classId" class="form-label">班级ID</label>
      <input
        id="classId"
        v-model.number="form.class_id"
        type="number"
        class="form-input"
        placeholder="请输入班级ID"
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
        <span v-if="isLoading">加入中...</span>
        <span v-else>加入班级</span>
      </button>
      
      <button
        type="button"
        @click="handleJoinAsTeacher"
        class="btn btn-outline"
        :disabled="isLoading"
      >
        <span v-if="isLoading">加入中...</span>
        <span v-else>作为助教加入</span>
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { classApi } from '../../api'
import type { JoinClassRequest } from '../../types'

const emit = defineEmits<{
  success: [data: any]
}>()

const form = reactive<JoinClassRequest>({
  class_id: 0
})

const error = ref<string | null>(null)
const isLoading = ref(false)

const handleSubmit = async () => {
  error.value = null
  
  if (!form.class_id || form.class_id <= 0) {
    error.value = '请输入有效的班级ID'
    return
  }

  isLoading.value = true
  
  try {
    const result = await classApi.joinAsStudent(form)
    emit('success', result)
    form.class_id = 0
  } catch (err: any) {
    console.error('Join class error:', err)
    error.value = err.response?.data?.detail || '加入班级失败'
  } finally {
    isLoading.value = false
  }
}

const handleJoinAsTeacher = async () => {
  error.value = null
  
  if (!form.class_id || form.class_id <= 0) {
    error.value = '请输入有效的班级ID'
    return
  }

  isLoading.value = true
  
  try {
    const result = await classApi.joinAsTeacher(form)
    emit('success', result)
    form.class_id = 0
  } catch (err: any) {
    console.error('Join class as teacher error:', err)
    error.value = err.response?.data?.detail || '加入班级失败'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.form-actions {
  display: flex;
  gap: 1rem;
}

.form-actions button {
  flex: 1;
}
</style>
