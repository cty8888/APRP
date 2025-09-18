<template>
  <nav class="navbar" v-if="isAuthenticated">
    <div class="container">
      <div class="navbar-content">
        <router-link to="/dashboard" class="navbar-brand">
          APRP
        </router-link>
        <div class="navbar-nav">
          <router-link to="/dashboard" class="nav-link">仪表板</router-link>
          
          <!-- 教师导航 -->
          <template v-if="user?.role === 'teacher'">
            <router-link to="/classes" class="nav-link">班级管理</router-link>
          </template>
          
          <!-- 学生导航 -->
          <template v-else>
            <router-link to="/my-classes" class="nav-link">我的班级</router-link>
          </template>
          
          <div class="navbar-user">
            <span class="user-info">{{ user?.name }} ({{ user?.role === 'teacher' ? '教师' : '学生' }})</span>
            <button @click="handleLogout" class="btn btn-outline btn-sm">登出</button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue'
import { useAuth } from '../../store/auth'
import { useRouter } from 'vue-router'

const authStore = useAuth()
const { user, logout } = authStore
const router = useRouter()

// 使用computed确保响应性
const isAuthenticated = computed(() => authStore.isAuthenticated)

// 监听认证状态变化，用于调试
watch(isAuthenticated, (newValue, oldValue) => {
  console.log('Navbar: isAuthenticated changed from', oldValue, 'to', newValue)
}, { immediate: true })

const handleLogout = async () => {
  console.log('Navbar: handleLogout called')
  try {
    await logout()
    console.log('Navbar: logout completed, redirecting...')
    // 立即跳转到登录页
    await router.push('/login')
  } catch (error) {
    console.error('Logout error:', error)
    // 即使出错也要跳转到登录页
    await router.push('/login')
  }
}
</script>
