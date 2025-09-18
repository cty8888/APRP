import { createRouter, createWebHistory } from 'vue-router'
import routes from './routes'

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, _from, next) => {
  const token = localStorage.getItem('token')
  const user = localStorage.getItem('user')
  
  // 验证token和用户数据的有效性
  const isValidAuth = () => {
    if (!token || !user) return false
    try {
      const userData = JSON.parse(user)
      return userData && userData.id && userData.name && userData.role
    } catch {
      return false
    }
  }
  
  const isAuthenticated = isValidAuth()
  
  // 清理无效的认证数据
  if (!isAuthenticated && (token || user)) {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }
  
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    if (!isAuthenticated) {
      next(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
      return
    }
    
    // 检查角色权限
    if (to.meta.roles && Array.isArray(to.meta.roles)) {
      const userData = JSON.parse(user!)
      if (!to.meta.roles.includes(userData.role)) {
        next('/dashboard') // 重定向到仪表板
        return
      }
    }
  }
  
  // 如果已经登录但访问登录/注册页，重定向到仪表板
  if ((to.path === '/login' || to.path === '/register') && isAuthenticated) {
    next('/dashboard')
    return
  }
  
  // 如果访问根路径且已登录，重定向到仪表板
  if (to.path === '/' && isAuthenticated) {
    next('/dashboard')
    return
  }
  
  next()
})

export default router