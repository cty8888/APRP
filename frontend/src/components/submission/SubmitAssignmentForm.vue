<template>
  <form @submit.prevent="handleSubmit" class="form">
    <h2>提交作业</h2>
    
    <div v-if="error" class="alert alert-error">
      {{ error }}
    </div>

    <div v-if="success" class="alert alert-success">
      {{ success }}
    </div>

    <div v-if="assignmentInfo" class="assignment-info">
      <h3>{{ assignmentInfo.title }}</h3>
      <p class="assignment-class">{{ assignmentInfo.class_name }}</p>
      <p v-if="assignmentInfo.description" class="assignment-description">{{ assignmentInfo.description }}</p>
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
      :disabled="isLoading || !selectedFile"
      style="width: 100%;"
    >
      <span v-if="isLoading">提交中...</span>
      <span v-else>提交作业</span>
    </button>
  </form>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { submissionApi, assignmentApi } from '../../api'
import type { AssignmentResponse } from '../../types'

interface Props {
  assignmentId?: number
}

const props = defineProps<Props>()

const emit = defineEmits<{
  success: [data: any]
}>()

const assignmentInfo = ref<AssignmentResponse | null>(null)
const selectedFile = ref<File | null>(null)
const error = ref<string | null>(null)
const success = ref<string | null>(null)
const isLoading = ref(false)

const loadAssignmentInfo = async () => {
  if (!props.assignmentId) return
  
  try {
    assignmentInfo.value = await assignmentApi.getAssignmentDetail(props.assignmentId)
  } catch (error) {
    console.error('Failed to load assignment info:', error)
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
  
  if (!props.assignmentId || !selectedFile.value) {
    error.value = '请选择文件'
    return
  }

  isLoading.value = true
  
  try {
    const result = await submissionApi.create(props.assignmentId, selectedFile.value)
    success.value = result.message
    emit('success', result)
    
    // 重置表单
    selectedFile.value = null
    const fileInput = document.getElementById('file') as HTMLInputElement
    if (fileInput) fileInput.value = ''
  } catch (err: any) {
    console.error('Submit assignment error:', err)
    error.value = err.response?.data?.detail || '提交作业失败'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadAssignmentInfo()
})
</script>

<style scoped>
.assignment-info {
  background: var(--color-background-muted);
  padding: var(--spacing-6);
  border-radius: var(--radius-lg);
  margin-bottom: var(--spacing-6);
  border: 1px solid var(--color-border);
}

.assignment-info h3 {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-2) 0;
}

.assignment-class {
  color: var(--color-text-secondary);
  font-size: var(--font-size-base);
  margin: 0 0 var(--spacing-2) 0;
}

.assignment-description {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  margin: 0;
  line-height: 1.5;
}

.form-hint {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  margin-top: var(--spacing-2);
}

.file-info {
  background: var(--color-background-muted);
  padding: var(--spacing-4);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-4);
  border: 1px solid var(--color-border);
}

.file-info p {
  margin: var(--spacing-1) 0;
  color: var(--color-text-primary);
  font-size: var(--font-size-sm);
}

.alert-success {
  background-color: var(--color-success-light);
  color: var(--color-success);
  border: 1px solid var(--color-success);
}
</style>
