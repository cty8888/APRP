<template>
  <div class="dashboard">
    <div class="container">
      <div class="dashboard-header">
        <h1 class="page-title">仪表板</h1>
        <p class="dashboard-subtitle">欢迎回来，{{ user?.name }}！</p>
      </div>
      
      <div class="dashboard-content">
        <!-- 加载状态 -->
        <div v-if="isLoading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>加载数据中...</p>
        </div>
        
        <!-- 错误状态 -->
        <div v-else-if="hasError" class="error-container">
          <div class="error-icon">⚠️</div>
          <h3>加载失败</h3>
          <p>{{ errorMessage }}</p>
          <button @click="retryLoadStats" class="btn btn-primary">
            重试
          </button>
        </div>
        
        <!-- 教师仪表板 -->
        <template v-else-if="user?.role === 'teacher'">
          <div class="stats-grid">
            <div class="stat-card">
              <h3>我的班级</h3>
              <p class="stat-number">{{ stats.classCount }}</p>
            </div>
            <div class="stat-card">
              <h3>总任务数</h3>
              <p class="stat-number">{{ stats.assignmentCount }}</p>
            </div>
            <div class="stat-card">
              <h3>待评分</h3>
              <p class="stat-number">{{ stats.pendingGrading }}</p>
            </div>
          </div>
        </template>
        
        <!-- 学生仪表板 -->
        <template v-else>
          <div class="stats-grid">
            <div class="stat-card">
              <h3>加入的班级</h3>
              <p class="stat-number">{{ stats.joinedClasses }}</p>
            </div>
            <div class="stat-card">
              <h3>待完成任务</h3>
              <p class="stat-number">{{ stats.pendingAssignments }}</p>
            </div>
            <div class="stat-card">
              <h3>已提交任务</h3>
              <p class="stat-number">{{ stats.submittedAssignments }}</p>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuth } from '../store/auth'
import { classApi, assignmentApi, submissionApi } from '../api'

const { user } = useAuth()

// 统计数据
const stats = ref({
  classCount: 0,
  assignmentCount: 0,
  pendingGrading: 0,
  joinedClasses: 0,
  pendingAssignments: 0,
  submittedAssignments: 0
})

const isLoading = ref(true)
const hasError = ref(false)
const errorMessage = ref('')

const loadStats = async () => {
  if (!user) return
  
  try {
    isLoading.value = true
    hasError.value = false
    errorMessage.value = ''
    
    if (user.role === 'teacher') {
      // 教师统计
      const [classes, assignments] = await Promise.all([
        classApi.getMyCreatedClasses(),
        assignmentApi.getMyAssignments()
      ])
      
      stats.value.classCount = classes.length
      stats.value.assignmentCount = assignments.length
      
      // 计算待评分数量（老师专用API）
      try {
        // 获取所有任务，然后统计未批改的提交
        let totalUngraded = 0
        for (const assignment of assignments) {
          try {
            const ungradedSubmissions = await submissionApi.getUngradedSubmissions(assignment.id)
            totalUngraded += ungradedSubmissions.length
          } catch (error) {
            console.warn(`Failed to load ungraded submissions for assignment ${assignment.id}:`, error)
          }
        }
        stats.value.pendingGrading = totalUngraded
      } catch (error) {
        console.warn('Failed to load ungraded submissions count:', error)
        stats.value.pendingGrading = 0
      }
    } else {
      // 学生统计 - 使用getMyClasses，它会根据用户角色返回相应的班级
      try {
        const [myClasses, submissions] = await Promise.all([
          classApi.getMyClasses(),
          submissionApi.getMySubmissions()
        ])
        
        stats.value.joinedClasses = myClasses.length
        stats.value.submittedAssignments = submissions.length
        
        console.log('Student stats loaded:', {
          joinedClasses: myClasses.length,
          submittedAssignments: submissions.length,
          classes: myClasses
        })
      } catch (error) {
        console.warn('Failed to load student stats:', error)
        stats.value.joinedClasses = 0
        stats.value.submittedAssignments = 0
      }
      
      // 计算待完成任务数量（简化版本）
      try {
        const pendingAssignments = await submissionApi.getPendingAssignments()
        stats.value.pendingAssignments = pendingAssignments.length
      } catch (error) {
        console.warn('Failed to load pending assignments:', error)
        // 如果API失败，尝试通过其他方式计算
        try {
          const assignments = await assignmentApi.getMyAssignments()
          const submissions = await submissionApi.getMySubmissions()
          stats.value.pendingAssignments = assignments.filter(a => 
            !submissions.find(s => s.assignment_id === a.id)
          ).length
        } catch (fallbackError) {
          console.warn('Fallback calculation also failed:', fallbackError)
          stats.value.pendingAssignments = 0
        }
      }
    }
  } catch (error: any) {
    console.error('Failed to load dashboard stats:', error)
    hasError.value = true
    errorMessage.value = error.response?.data?.detail || '加载数据失败，请检查网络连接'
  } finally {
    isLoading.value = false
  }
}

const retryLoadStats = () => {
  loadStats()
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-container p {
  color: var(--color-text-secondary);
  font-size: 1.1rem;
  margin: 0;
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background: #fff5f5;
  border: 1px solid #fed7d7;
  border-radius: 8px;
  margin: 2rem 0;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-container h3 {
  color: #e53e3e;
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
}

.error-container p {
  color: #718096;
  margin: 0 0 1.5rem 0;
  font-size: 1.1rem;
}

.error-container .btn {
  min-width: 120px;
}
</style>