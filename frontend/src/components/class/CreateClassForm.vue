<template>
  <form @submit.prevent="handleSubmit" class="form">
    <h2>创建班级</h2>
    
    <div v-if="error" class="alert alert-error">
      {{ error }}
    </div>

    <div class="form-group">
      <label for="name" class="form-label">班级名称</label>
      <input
        id="name"
        v-model="form.name"
        type="text"
        class="form-input"
        placeholder="请输入班级名称"
        required
        :disabled="isLoading"
      />
    </div>

    <div class="form-group">
      <label for="description" class="form-label">班级描述</label>
      <textarea
        id="description"
        v-model="form.description"
        class="form-input"
        placeholder="请输入班级描述（可选）"
        rows="3"
        :disabled="isLoading"
      ></textarea>
    </div>

    <button
      type="submit"
      class="btn btn-primary"
      :disabled="isLoading"
      style="width: 100%;"
    >
      <span v-if="isLoading">创建中...</span>
      <span v-else>创建班级</span>
    </button>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { classApi } from '../../api'
import type { ClassCreate } from '../../types'

const emit = defineEmits<{
  success: [classData: any]
}>()

const form = reactive<ClassCreate>({
  name: '',
  description: ''
})

const error = ref<string | null>(null)
const isLoading = ref(false)

const handleSubmit = async () => {
  error.value = null
  
  if (!form.name.trim()) {
    error.value = '请输入班级名称'
    return
  }

  isLoading.value = true
  
  try {
    const result = await classApi.create(form)
    emit('success', result)
    
    // 重置表单
    form.name = ''
    form.description = ''
  } catch (err: any) {
    console.error('Create class error:', err)
    error.value = err.response?.data?.detail || '创建班级失败'
  } finally {
    isLoading.value = false
  }
}
</script>
