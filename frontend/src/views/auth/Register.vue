<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1 class="auth-title">注册</h1>
        <p class="auth-subtitle">创建您的APRP账户</p>
      </div>

      <RegisterForm />

      <!-- 登录链接 -->
      <div class="auth-footer">
        <p>已有账户？ <router-link to="/login" class="auth-link">立即登录</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import RegisterForm from '../../components/forms/RegisterForm.vue'
</script>