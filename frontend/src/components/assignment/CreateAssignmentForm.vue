<template>
  <form @submit.prevent="handleSubmit" class="form">
    <h2>创建任务</h2>
    
    <div v-if="error" class="alert alert-error">
      {{ error }}
    </div>

    <div class="form-group">
      <label for="classId" class="form-label">选择班级</label>
      <select
        id="classId"
        v-model="form.class_id"
        class="form-input"
        required
        :disabled="isLoading"
      >
        <option value="">请选择班级</option>
        <option 
          v-for="classItem in classes" 
          :key="classItem.id" 
          :value="classItem.id"
        >
          {{ classItem.name }}
        </option>
      </select>
    </div>

    <div class="form-group">
      <label for="title" class="form-label">任务标题</label>
      <input
        id="title"
        v-model="form.title"
        type="text"
        class="form-input"
        placeholder="请输入任务标题"
        required
        :disabled="isLoading"
      />
    </div>

    <div class="form-group">
      <label for="description" class="form-label">任务描述</label>
      <textarea
        id="description"
        v-model="form.description"
        class="form-input"
        placeholder="请输入任务描述（可选）"
        rows="4"
        :disabled="isLoading"
      ></textarea>
    </div>

    <button
      type="submit"
      class="btn btn-primary"
      :disabled="isLoading || !form.class_id"
      style="width: 100%;"
    >
      <span v-if="isLoading">创建中...</span>
      <span v-else>创建任务</span>
    </button>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { assignmentApi, classApi } from '../../api'
import type { AssignmentCreate, ClassResponse } from '../../types'

const emit = defineEmits<{
  success: [assignmentData: any]
}>()

const form = reactive<AssignmentCreate>({
  title: '',
  description: '',
  class_id: 0
})

const classes = ref<ClassResponse[]>([])
const error = ref<string | null>(null)
const isLoading = ref(false)

const loadClasses = async () => {
  try {
    // 只加载我创建的班级或我是助教的班级
    const [createdClasses, joinedClasses] = await Promise.all([
      classApi.getMyCreatedClasses(),
      classApi.getMyJoinedClasses()
    ])
    classes.value = [...createdClasses, ...joinedClasses]
  } catch (error) {
    console.error('Failed to load classes:', error)
  }
}

const handleSubmit = async () => {
  error.value = null
  
  if (!form.title.trim()) {
    error.value = '请输入任务标题'
    return
  }
  
  if (!form.class_id) {
    error.value = '请选择班级'
    return
  }

  isLoading.value = true
  
  try {
    const result = await assignmentApi.create(form)
    emit('success', result)
    
    // 重置表单
    form.title = ''
    form.description = ''
    form.class_id = 0
  } catch (err: any) {
    console.error('Create assignment error:', err)
    error.value = err.response?.data?.detail || '创建任务失败'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadClasses()
})
</script>
