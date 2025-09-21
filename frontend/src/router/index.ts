import { createRouter, createWebHistory } from 'vue-router'
import routes from './routes'
import { storeToRefs } from 'pinia'

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, _from, next) => {
  // 导入store以获取最新的认证状态
  const { useAuth } = await import('../store/auth')
  const authStore = useAuth()
  const { isAuthenticated, user } = storeToRefs(authStore)
  
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    if (!isAuthenticated.value) {
      next(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
      return
    }
    
    // 检查角色权限
    if (to.meta.roles && Array.isArray(to.meta.roles)) {
      const currentUser = user.value
      if (!currentUser || !to.meta.roles.includes(currentUser.role)) {
        next('/dashboard') // 重定向到仪表板
        return
      }
    }
  }
  
  // 如果已经登录但访问登录/注册页，重定向到仪表板
  if ((to.path === '/login' || to.path === '/register') && isAuthenticated.value) {
    next('/dashboard')
    return
  }
  
  // 如果访问根路径且已登录，重定向到仪表板
  if (to.path === '/' && isAuthenticated.value) {
    next('/dashboard')
    return
  }
  
  next()
})

export default router