<template>
  <form @submit.prevent="handleSubmit" class="form">
    <h2>编辑任务</h2>
    
    <div v-if="error" class="alert alert-error">
      {{ error }}
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

    <div class="form-actions">
      <button
        type="button"
        @click="$emit('cancel')"
        class="btn btn-outline"
        :disabled="isLoading"
      >
        取消
      </button>
      <button
        type="submit"
        class="btn btn-primary"
        :disabled="isLoading || !form.title?.trim()"
      >
        <span v-if="isLoading">保存中...</span>
        <span v-else>保存修改</span>
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { assignmentApi } from '../../api'
import type { AssignmentResponse, AssignmentUpdate } from '../../types'

interface Props {
  assignment: AssignmentResponse
}

const props = defineProps<Props>()

const emit = defineEmits<{
  success: [assignmentData: AssignmentResponse]
  cancel: []
}>()

const form = reactive<AssignmentUpdate>({
  title: '',
  description: ''
})

const error = ref<string | null>(null)
const isLoading = ref(false)

onMounted(() => {
  // 初始化表单数据
  form.title = props.assignment.title
  form.description = props.assignment.description || ''
})

const handleSubmit = async () => {
  error.value = null
  
  if (!form.title?.trim()) {
    error.value = '请输入任务标题'
    return
  }

  isLoading.value = true
  
  try {
    const result = await assignmentApi.update(props.assignment.id, form)
    emit('success', result)
  } catch (err: any) {
    console.error('Update assignment error:', err)
    error.value = err.response?.data?.detail || '更新任务失败'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.form-actions {
  display: flex;
  gap: var(--spacing-4);
  justify-content: flex-end;
}

.form-actions button {
  min-width: 100px;
}
</style>
