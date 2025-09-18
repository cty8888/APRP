<template>
  <div id="app">
    <Navbar />
    <main class="page">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { watch } from 'vue'
import { Navbar } from './components'
import { useAuth } from './store/auth'
import './styles'

// 创建认证store实例，会自动初始化认证状态
const authStore = useAuth()

// 监听全局认证状态变化
watch(
  () => authStore.isAuthenticated,
  (newValue, oldValue) => {
    console.log('App: Global auth state changed from', oldValue, 'to', newValue)
  },
  { immediate: true }
)
</script>