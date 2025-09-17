<template>
  <div class="upload-page">
    <h1>上传文档</h1>
    <div class="file-upload">
      <div class="upload-area" v-on:click="triggerFileInput">
        <input ref="fileInput" type="file" accept=".docx" v-on:change="handleFileSelect" style="display: none">
        <div v-if="!selectedFile">
          <p>点击选择 .docx 文件</p>
        </div>
        <div v-else>
          <p>已选择: {{ selectedFile.name }}</p>
          <button v-on:click.stop="removeFile">移除</button>
        </div>
      </div>
      
      <div v-if="selectedFile">
        <button v-on:click="uploadFile" :disabled="uploading">
          {{ uploading ? '上传中...' : '分析并查看结果' }}
        </button>
      </div>
      
      <div v-if="error" class="error">
        {{ error }}
      </div>
    </div>
    
    <div v-if="uploadError" class="error">
      {{ uploadError }}
    </div> 
    
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { uploadDocx } from '../api/client'

const router = useRouter()
const uploadError = ref('')

// 文件上传相关状态
const fileInput = ref<HTMLInputElement>()
const selectedFile = ref<File | null>(null)
const uploading = ref(false)
const error = ref('')

// 文件选择相关方法
const triggerFileInput = () => {
  if (uploading.value) return
  if (fileInput.value) fileInput.value.click()
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    selectFile(target.files[0])
  }
}

const selectFile = (file: File) => {
  if (!file.name.endsWith('.docx')) {
    error.value = '请选择 .docx 格式的Word文档'
    return
  }
  
  selectedFile.value = file
  error.value = ''
}

const removeFile = () => {
  selectedFile.value = null
  error.value = ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// 文件上传方法
const uploadFile = async () => {
  if (!selectedFile.value) return
  
  uploading.value = true
  error.value = ''
  uploadError.value = ''
  
  try {
    const response = await uploadDocx(selectedFile.value)
    handleUploadSuccess(response.data)
  } catch (err: any) {
    const errorMessage = err.response?.data?.detail || '上传失败，请重试'
    error.value = errorMessage
    uploadError.value = errorMessage
  } finally {
    uploading.value = false
  }
}

const handleUploadSuccess = (result: any) => {
  // 将结果存储到sessionStorage，然后跳转到结果页面
  sessionStorage.setItem('analysisResult', JSON.stringify(result))
  router.push('/result')
}


</script>

<style scoped>
.upload-page {
  padding: 2rem;
  text-align: center;
}

h1 {
  margin-bottom: 2rem;
}

/* 文件上传区域样式 */
.file-upload {
  margin: 2rem 0;
}

.upload-area {
  border: 2px dashed #ccc;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  background: #f9f9f9;
}

.upload-area:hover {
  border-color: #007bff;
  background: #f0f8ff;
}

.error {
  color: red;
  margin: 1rem 0;
  padding: 0.5rem;
  background: #ffe6e6;
  border: 1px solid #ffcccc;
  border-radius: 4px;
}



button {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 0.5rem;
}

button:hover {
  background: #0056b3;
}

button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}


</style>
