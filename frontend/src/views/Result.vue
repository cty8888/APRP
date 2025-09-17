<template>
  <div class="result-page">
    <div v-if="!analysisResult" class="no-result">
      <h2>没有分析结果</h2>
      <p>请先上传文档进行分析</p>
      <button @click="goUpload">去上传文档</button>
    </div>
    
    <div v-else>
      <h1>分析结果</h1>
      <div class="actions">
        <button @click="goHome">返回主页</button>
        <button @click="goUpload">重新上传</button>
      </div>
      
      <AnalysisResult :result="analysisResult" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AnalysisResult from '../components/AnalysisResult.vue'

const router = useRouter()
const analysisResult = ref(null)

onMounted(() => {
  // 从sessionStorage获取分析结果
  const storedResult = sessionStorage.getItem('analysisResult')
  if (storedResult) {
    try {
      analysisResult.value = JSON.parse(storedResult)
    } catch (error) {
      console.error('解析分析结果失败:', error)
    }
  }
})

const goHome = () => {
  router.push('/')
}

const goUpload = () => {
  // 清除当前结果
  sessionStorage.removeItem('analysisResult')
  router.push('/upload')
}
</script>

<style scoped>
.result-page {
  padding: 2rem;
}

h1 {
  margin-bottom: 1rem;
}

.actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

button {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #0056b3;
}

.no-result {
  text-align: center;
  padding: 2rem;
}

.no-result h2 {
  color: red;
  margin-bottom: 1rem;
}

.no-result p {
  margin-bottom: 2rem;
  color: #666;
}
</style>
