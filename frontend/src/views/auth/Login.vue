<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1 class="auth-title">登录</h1>
        <p class="auth-subtitle">欢迎回到APRP平台</p>
      </div>

      <LoginForm />

      <!-- 注册链接 -->
      <div class="auth-footer">
        <p>还没有账户？ <router-link to="/register" class="auth-link">立即注册</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import LoginForm from '../../components/forms/LoginForm.vue'
</script>