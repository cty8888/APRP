<template>
  <form @submit.prevent="handleSubmit" class="form">
    <h2>提交作业</h2>
    
    <div v-if="error" class="alert alert-error">
      {{ error }}
    </div>

    <div v-if="success" class="alert alert-success">
      {{ success }}
    </div>

    <div class="form-group">
      <label for="assignmentId" class="form-label">选择任务</label>
      <select
        id="assignmentId"
        v-model="selectedAssignmentId"
        class="form-input"
        required
        :disabled="isLoading"
      >
        <option value="">请选择任务</option>
        <option 
          v-for="assignment in pendingAssignments" 
          :key="assignment.id" 
          :value="assignment.id"
        >
          {{ assignment.title }} ({{ assignment.class_name }})
        </option>
      </select>
    </div>

    <div class="form-group">
      <label for="file" class="form-label">上传文件 (仅支持.docx格式)</label>
      <input
        id="file"
        type="file"
        class="form-input"
        accept=".docx"
        required
        :disabled="isLoading"
        @change="handleFileChange"
      />
      <small class="form-hint">请选择Word文档文件(.docx)</small>
    </div>

    <div v-if="selectedFile" class="file-info">
      <p>已选择文件: {{ selectedFile.name }}</p>
      <p>文件大小: {{ formatFileSize(selectedFile.size) }}</p>
    </div>

    <button
      type="submit"
      class="btn btn-primary"
      :disabled="isLoading || !selectedAssignmentId || !selectedFile"
      style="width: 100%;"
    >
      <span v-if="isLoading">提交中...</span>
      <span v-else>提交作业</span>
    </button>
  </form>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { submissionApi } from '../../api'
import type { PendingAssignmentResponse } from '../../types'

const emit = defineEmits<{
  success: [data: any]
}>()

const pendingAssignments = ref<PendingAssignmentResponse[]>([])
const selectedAssignmentId = ref<number | ''>('')
const selectedFile = ref<File | null>(null)
const error = ref<string | null>(null)
const success = ref<string | null>(null)
const isLoading = ref(false)

const loadPendingAssignments = async () => {
  try {
    pendingAssignments.value = await submissionApi.getPendingAssignments()
  } catch (error) {
    console.error('Failed to load pending assignments:', error)
  }
}

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  
  if (file) {
    if (!file.name.toLowerCase().endsWith('.docx')) {
      error.value = '请选择.docx格式的文件'
      target.value = ''
      return
    }
    
    if (file.size > 10 * 1024 * 1024) { // 10MB限制
      error.value = '文件大小不能超过10MB'
      target.value = ''
      return
    }
    
    selectedFile.value = file
    error.value = null
  }
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const handleSubmit = async () => {
  error.value = null
  success.value = null
  
  if (!selectedAssignmentId.value || !selectedFile.value) {
    error.value = '请选择任务和文件'
    return
  }

  isLoading.value = true
  
  try {
    const result = await submissionApi.create(selectedAssignmentId.value as number, selectedFile.value)
    success.value = result.message
    emit('success', result)
    
    // 重置表单
    selectedAssignmentId.value = ''
    selectedFile.value = null
    const fileInput = document.getElementById('file') as HTMLInputElement
    if (fileInput) fileInput.value = ''
    
    // 重新加载待提交任务
    await loadPendingAssignments()
  } catch (err: any) {
    console.error('Submit assignment error:', err)
    error.value = err.response?.data?.detail || '提交作业失败'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadPendingAssignments()
})
</script>

<style scoped>
.form-hint {
  color: #666;
  font-size: 0.9rem;
  margin-top: 0.25rem;
}

.file-info {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.file-info p {
  margin: 0.25rem 0;
  color: #333;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}
</style>
