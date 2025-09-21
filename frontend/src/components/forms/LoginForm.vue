<template>
  <form @submit.prevent="handleLogin" class="auth-form">
    <!-- 错误消息 -->
    <div v-if="error" class="alert alert-error">
      {{ error }}
    </div>

    <!-- 用户名输入 -->
    <div class="form-group">
      <label for="name" class="form-label">用户名</label>
      <input
        id="name"
        v-model="form.name"
        type="text"
        class="form-input"
        placeholder="请输入用户名"
        required
        :disabled="isLoading"
      />
    </div>

    <!-- 密码输入 -->
    <div class="form-group">
      <label for="password" class="form-label">密码</label>
      <input
        id="password"
        v-model="form.password"
        type="password"
        class="form-input"
        placeholder="请输入密码"
        required
        :disabled="isLoading"
      />
    </div>

    <!-- 登录按钮 -->
    <button
      type="submit"
      class="btn btn-primary"
      :disabled="isLoading"
      style="width: 100%;"
    >
      <span v-if="isLoading" class="loading"></span>
      <span v-else>登录</span>
    </button>
  </form>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../../store/auth'

const router = useRouter()
const { login, isLoading } = useAuth()

const form = reactive({
  name: '',
  password: ''
})

const error = ref<string | null>(null)

const handleLogin = async () => {
  error.value = null
  
  if (!form.name || !form.password) {
    error.value = '请填写所有必填字段'
    return
  }

  const result = await login(form.name, form.password)
  
  if (result.success) {
    // 登录成功后跳转到首页或重定向页面
    const redirectTo = router.currentRoute.value.query.redirect as string || '/dashboard'
    console.log('LoginForm: Login successful, redirecting to:', redirectTo)
    await router.push(redirectTo)
  } else {
    error.value = result.error || '登录失败'
  }
}
</script>
