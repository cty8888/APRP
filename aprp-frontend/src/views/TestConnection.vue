<template>
  <div class="test-connection">
    <h1>前后端连接测试</h1>
    
    <div class="test-section">
      <h2>后端健康检查</h2>
      <button @click="testHealth" :disabled="loading">
        {{ loading ? '测试中...' : '测试连接' }}
      </button>
      <div v-if="healthResult" class="result">
        <h3>结果:</h3>
        <pre>{{ JSON.stringify(healthResult, null, 2) }}</pre>
      </div>
    </div>

    <div class="test-section">
      <h2>根路径测试</h2>
      <button @click="testRoot" :disabled="loading">
        {{ loading ? '测试中...' : '测试根路径' }}
      </button>
      <div v-if="rootResult" class="result">
        <h3>结果:</h3>
        <pre>{{ JSON.stringify(rootResult, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { healthCheck, getRoot } from '../api/client'

interface ApiResult {
  [key: string]: any
}

const loading = ref(false)
const healthResult = ref<ApiResult | null>(null)
const rootResult = ref<ApiResult | null>(null)

const testHealth = async () => {
  loading.value = true
  try {
    const response = await healthCheck()
    healthResult.value = response.data
  } catch (error: any) {
    healthResult.value = { error: error?.message || 'Unknown error' }
  } finally {
    loading.value = false
  }
}

const testRoot = async () => {
  loading.value = true
  try {
    const response = await getRoot()
    rootResult.value = response.data
  } catch (error: any) {
    rootResult.value = { error: error?.message || 'Unknown error' }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.test-connection {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.test-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 15px;
}

button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}

.result {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  border-left: 4px solid #007bff;
}

pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
