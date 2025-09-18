<template>
  <div class="home">
    <div class="hero">
      <h1 class="hero-title">欢迎使用APRP平台</h1>
      <p class="hero-subtitle">学术论文评审与评分系统</p>
      
      <!-- 未登录时显示登录注册按钮 -->
      <div v-if="!isAuthenticated" class="hero-actions">
        <router-link to="/login" class="btn btn-primary">立即开始</router-link>
        <div class="auth-links">
          <span>还没有账户？</span>
          <router-link to="/register" class="auth-link">注册新账户</router-link>
        </div>
      </div>
      
      <!-- 已登录时会自动重定向到仪表板，这里不应该显示 -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuth } from '../store/auth'

const { isAuthenticated } = useAuth()
</script>