<template>
  <div class="edit-class-form">
    <div class="form-header">
      <h2>编辑班级</h2>
      <p class="form-subtitle">修改班级信息</p>
    </div>

    <form @submit.prevent="handleSubmit" class="form">
      <div class="form-group">
        <label for="name" class="form-label">班级名称 *</label>
        <input
          id="name"
          v-model="form.name"
          type="text"
          class="form-input"
          :class="{ 'error': errors.name }"
          placeholder="请输入班级名称"
          required
        />
        <div v-if="errors.name" class="error-message">{{ errors.name }}</div>
      </div>

      <div class="form-group">
        <label for="description" class="form-label">班级描述</label>
        <textarea
          id="description"
          v-model="form.description"
          class="form-textarea"
          :class="{ 'error': errors.description }"
          placeholder="请输入班级描述（可选）"
          rows="4"
        ></textarea>
        <div v-if="errors.description" class="error-message">{{ errors.description }}</div>
      </div>

      <div class="form-actions">
        <button 
          type="button" 
          @click="handleCancel" 
          class="btn btn-outline"
          :disabled="isSubmitting"
        >
          取消
        </button>
        <button 
          type="submit" 
          class="btn btn-primary"
          :disabled="isSubmitting || !isFormValid"
        >
          {{ isSubmitting ? '保存中...' : '保存' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { classApi } from '../../api'
import type { ClassResponse, ClassUpdate } from '../../types'

interface Props {
  classData: ClassResponse
}

const props = defineProps<Props>()

const emit = defineEmits<{
  success: [data: ClassResponse]
  cancel: []
}>()

const form = ref<ClassUpdate>({
  name: '',
  description: ''
})

const errors = ref<Record<string, string>>({})
const isSubmitting = ref(false)

const isFormValid = computed(() => {
  return form.value.name && form.value.name.trim().length > 0
})

const validateForm = () => {
  errors.value = {}
  
  if (!form.value.name || form.value.name.trim().length === 0) {
    errors.value.name = '班级名称不能为空'
  } else if (form.value.name.length > 100) {
    errors.value.name = '班级名称不能超过100个字符'
  }
  
  if (form.value.description && form.value.description.length > 500) {
    errors.value.description = '班级描述不能超过500个字符'
  }
  
  return Object.keys(errors.value).length === 0
}

const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }
  
  isSubmitting.value = true
  
  try {
    const updateData: ClassUpdate = {
      name: form.value.name?.trim() || '',
      description: form.value.description?.trim() || undefined
    }
    
    const updatedClass = await classApi.update(props.classData.id, updateData)
    emit('success', updatedClass)
  } catch (error: any) {
    console.error('Failed to update class:', error)
    if (error.response?.data?.detail) {
      alert(`更新班级失败: ${error.response.data.detail}`)
    } else {
      alert('更新班级失败，请重试')
    }
  } finally {
    isSubmitting.value = false
  }
}

const handleCancel = () => {
  emit('cancel')
}

onMounted(() => {
  // 初始化表单数据
  form.value = {
    name: props.classData.name,
    description: props.classData.description || ''
  }
})
</script>

<style scoped>
.edit-class-form {
  max-width: 500px;
  margin: 0 auto;
  padding: var(--spacing-6);
  background: var(--color-background);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

.form-header {
  text-align: center;
  margin-bottom: var(--spacing-8);
}

.form-header h2 {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-2);
}

.form-subtitle {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  margin: 0;
}

.form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-6);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

.form-label {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
}

.form-input,
.form-textarea {
  padding: var(--spacing-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  transition: all var(--transition-fast);
  background: var(--color-background);
  color: var(--color-text-primary);
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.1);
}

.form-input.error,
.form-textarea.error {
  border-color: #dc3545;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.error-message {
  color: #dc3545;
  font-size: var(--font-size-sm);
  margin-top: var(--spacing-1);
}

.form-actions {
  display: flex;
  gap: var(--spacing-4);
  justify-content: flex-end;
  margin-top: var(--spacing-6);
  padding-top: var(--spacing-6);
  border-top: 1px solid var(--color-border);
}

.form-actions .btn {
  min-width: 100px;
}
</style>
