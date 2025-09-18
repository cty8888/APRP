<template>
  <form @submit.prevent="handleSubmit" class="form">
    <h2>批改作业</h2>
    
    <div v-if="error" class="alert alert-error">
      {{ error }}
    </div>

    <div v-if="success" class="alert alert-success">
      {{ success }}
    </div>

    <div class="submission-info">
      <h3>作业信息</h3>
      <p><strong>学生：</strong>{{ submissionDetail?.student_name }}</p>
      <p><strong>任务：</strong>{{ submissionDetail?.assignment_title }}</p>
      <p><strong>班级：</strong>{{ submissionDetail?.class_name }}</p>
      <p><strong>提交时间：</strong>{{ formatDate(submissionDetail?.submitted_at) }}</p>
    </div>

    <div class="form-group">
      <label for="score" class="form-label">分数 (0-100)</label>
      <input
        id="score"
        v-model.number="form.score"
        type="number"
        class="form-input"
        min="0"
        max="100"
        step="0.1"
        placeholder="请输入分数"
        required
        :disabled="isLoading"
      />
    </div>

    <div class="form-group">
      <label for="report" class="form-label">批改报告</label>
      <textarea
        id="report"
        v-model="form.report"
        class="form-input"
        placeholder="请输入批改意见和建议"
        rows="6"
        required
        :disabled="isLoading"
      ></textarea>
    </div>

    <div class="form-actions">
      <button
        type="submit"
        class="btn btn-primary"
        :disabled="isLoading"
      >
        <span v-if="isLoading">保存中...</span>
        <span v-else>保存批改</span>
      </button>
      
      <button
        type="button"
        @click="$emit('cancel')"
        class="btn btn-outline"
        :disabled="isLoading"
      >
        取消
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { submissionApi } from '../../api'
import type { SubmissionGrade, SubmissionDetailResponse } from '../../types'

interface Props {
  submissionId: number
}

const props = defineProps<Props>()

const emit = defineEmits<{
  success: [data: any]
  cancel: []
}>()

const form = reactive<SubmissionGrade>({
  score: 0,
  report: ''
})

const submissionDetail = ref<SubmissionDetailResponse | null>(null)
const error = ref<string | null>(null)
const success = ref<string | null>(null)
const isLoading = ref(false)

const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString('zh-CN')
}

const loadSubmissionDetail = async () => {
  try {
    submissionDetail.value = await submissionApi.getSubmissionDetail(props.submissionId)
    
    // 如果已经批改过，填充现有数据
    if (submissionDetail.value.is_graded) {
      form.score = submissionDetail.value.score || 0
      form.report = submissionDetail.value.report || ''
    }
  } catch (error) {
    console.error('Failed to load submission detail:', error)
  }
}

const handleSubmit = async () => {
  error.value = null
  success.value = null
  
  if (form.score < 0 || form.score > 100) {
    error.value = '分数必须在0-100之间'
    return
  }
  
  if (!form.report.trim()) {
    error.value = '请输入批改报告'
    return
  }

  isLoading.value = true
  
  try {
    const result = await submissionApi.gradeSubmission(props.submissionId, form)
    success.value = '批改保存成功'
    emit('success', result)
  } catch (err: any) {
    console.error('Grade submission error:', err)
    error.value = err.response?.data?.detail || '保存批改失败'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadSubmissionDetail()
})
</script>

<style scoped>
.submission-info {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.submission-info h3 {
  margin-bottom: 1rem;
  color: #333;
}

.submission-info p {
  margin: 0.5rem 0;
  color: #666;
  font-size: 1.1rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
}

.form-actions button {
  flex: 1;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}
</style>
