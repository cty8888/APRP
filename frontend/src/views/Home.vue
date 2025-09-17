<template>
  <div class="home">
    <h1>APRP 论文评审平台</h1>
    <p>上传Word文档进行智能分析</p>
    
    <div class="actions">
      <button @click="goUpload">上传文档</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goUpload = () => {
  router.push('/upload')
}
</script>

<style scoped>
.home {
  text-align: center;
  padding: 2rem;
}

h1 {
  margin-bottom: 1rem;
}

p {
  margin-bottom: 2rem;
  color: #666;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
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
</style>
