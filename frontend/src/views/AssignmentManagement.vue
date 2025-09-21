<template>
  <div class="assignment-management">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-main">
          <h1 class="page-title">
            <i class="icon">📋</i>
            {{ classId ? '班级任务管理' : '我的任务' }}
          </h1>
          <p class="page-subtitle">
            {{ classId ? '管理班级中的所有任务' : '查看和管理您的任务' }}
          </p>
        </div>
      </div>
    </div>

    <!-- 标签页导航 -->
    <div class="tabs-container">
      <div class="tabs">
        <button 
          :class="['tab', { active: activeTab === 'list' }]"
          @click="activeTab = 'list'"
        >
          <i class="icon">📝</i>
          {{ classId ? '班级任务' : '我的任务' }}
        </button>
        <button 
          :class="['tab', { active: activeTab === 'create' }]"
          @click="activeTab = 'create'"
          v-if="user?.role === 'teacher'"
        >
          <i class="icon">➕</i>
          创建任务
        </button>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="content-container">
      <!-- 任务列表 -->
      <div v-if="activeTab === 'list'" class="tab-pane">
        <AssignmentList 
          ref="assignmentListRef"
          :title="classId ? '班级任务' : '我的任务'"
          :classId="classId"
          @selectAssignment="handleSelectAssignment"
          @editAssignment="handleEditAssignment"
          @assignmentDeleted="handleAssignmentDeleted"
          @submitAssignment="handleSubmitAssignment"
          @viewSubmissions="handleViewSubmissions"
        />
      </div>

      <!-- 创建任务 -->
      <div v-if="activeTab === 'create'" class="tab-pane">
        <div class="form-container">
          <CreateAssignmentForm 
            :classId="classId"
            @success="handleCreateSuccess" 
          />
        </div>
      </div>

    </div>

    <!-- 编辑任务弹窗 -->
    <div v-if="editingAssignment" class="modal-overlay" @click="closeEditModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>编辑任务</h3>
          <button @click="closeEditModal" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <EditAssignmentForm 
            :assignment="editingAssignment"
            @success="handleEditSuccess"
            @cancel="closeEditModal"
          />
        </div>
        <div class="modal-footer">
          <button 
            @click="deleteAssignment(editingAssignment.id)"
            class="btn btn-danger"
          >
            <i class="icon">🗑️</i>
            删除任务
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../store/auth'
import { AssignmentList, CreateAssignmentForm, EditAssignmentForm } from '../components'
import { assignmentApi } from '../api'
import type { AssignmentResponse } from '../types'

const route = useRoute()
const router = useRouter()
const { user } = useAuth()

const activeTab = ref('list')
const editingAssignment = ref<AssignmentResponse | null>(null)
const assignmentListRef = ref()
const classId = ref<number | undefined>()


const handleSelectAssignment = (assignment: AssignmentResponse) => {
  // 现在不需要弹窗，直接跳转到相应页面
  if (user?.role === 'student') {
    handleSubmitAssignment(assignment)
  } else if (user?.role === 'teacher') {
    handleViewSubmissions(assignment)
  }
}

const handleCreateSuccess = (assignmentData: any) => {
  console.log('任务创建成功:', assignmentData)
  activeTab.value = 'list'
  // 刷新任务列表
  if (assignmentListRef.value) {
    assignmentListRef.value.refreshAssignments()
  }
}

const handleEditAssignment = (assignment: AssignmentResponse) => {
  editingAssignment.value = assignment
}

const handleEditSuccess = (assignmentData: AssignmentResponse) => {
  console.log('任务编辑成功:', assignmentData)
  editingAssignment.value = null
  // 刷新任务列表
  if (assignmentListRef.value) {
    assignmentListRef.value.refreshAssignments()
  }
}

const closeEditModal = () => {
  editingAssignment.value = null
}

const deleteAssignment = async (assignmentId: number) => {
  if (!confirm('确定要删除这个任务吗？此操作不可撤销。')) {
    return
  }
  
  try {
    await assignmentApi.delete(assignmentId)
    // 关闭编辑弹窗
    editingAssignment.value = null
    // 刷新任务列表
    if (assignmentListRef.value) {
      assignmentListRef.value.refreshAssignments()
    }
    console.log('任务删除成功:', assignmentId)
  } catch (error) {
    console.error('Failed to delete assignment:', error)
    alert('删除任务失败，请重试')
  }
}

const handleAssignmentDeleted = (assignmentId: number) => {
  console.log('任务删除成功:', assignmentId)
  // 任务列表会自动刷新
}

const handleSubmitAssignment = (assignment: AssignmentResponse) => {
  // 学生提交作业 - 直接跳转到提交页面
  if (classId.value) {
    router.push(`/my-classes/${classId.value}/assignments/${assignment.id}`)
  }
}

const handleViewSubmissions = (assignment: AssignmentResponse) => {
  // 老师查看提交 - 直接跳转到提交管理页面
  if (classId.value) {
    router.push(`/classes/${classId.value}/assignments/${assignment.id}/submissions`)
  }
}


onMounted(() => {
  // 从路由参数获取classId
  if (route.params.classId) {
    classId.value = parseInt(route.params.classId as string)
  } else if (route.query.classId) {
    classId.value = parseInt(route.query.classId as string)
  }
})

// 监听classId变化，自动刷新数据
watch(classId, async (newClassId) => {
  if (newClassId && assignmentListRef.value) {
    await nextTick()
    assignmentListRef.value.refreshAssignments()
  }
}, { immediate: true })

// 监听assignmentListRef变化，确保组件挂载后刷新数据
watch(assignmentListRef, async (newRef) => {
  if (newRef && classId.value) {
    await nextTick()
    newRef.refreshAssignments()
  }
})
</script>

<style scoped>
.assignment-management {
  min-height: 100vh;
  background: var(--color-background-light);
}

.page-header {
  background: var(--color-background);
  border-bottom: 1px solid var(--color-border);
  padding: var(--spacing-8) 0;
  margin-bottom: var(--spacing-8);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-6);
  display: flex;
  justify-content: center;
  align-items: center;
}

.header-main {
  flex: 1;
}

.page-title {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-2) 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
}

.page-title .icon {
  font-size: var(--font-size-2xl);
}

.page-subtitle {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin: 0;
}

.header-actions {
  flex-shrink: 0;
}

.tabs-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-6);
  margin-bottom: var(--spacing-8);
}

.tabs {
  display: flex;
  background: var(--color-background);
  border-radius: var(--radius-lg);
  padding: var(--spacing-2);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

.tab {
  flex: 1;
  background: none;
  border: none;
  padding: var(--spacing-4) var(--spacing-6);
  cursor: pointer;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
  transition: all var(--transition-fast);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-2);
}

.tab:hover {
  color: var(--color-text-primary);
  background: var(--color-background-muted);
}

.tab.active {
  color: var(--color-primary);
  background: var(--color-primary-light);
  box-shadow: var(--shadow-sm);
}

.tab .icon {
  font-size: var(--font-size-lg);
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-6);
}

.tab-pane {
  background: var(--color-background);
  border-radius: var(--radius-lg);
  padding: var(--spacing-8);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
  min-height: 400px;
}

.form-container {
  max-width: 600px;
  margin: 0 auto;
}

.btn {
  padding: var(--spacing-3) var(--spacing-6);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  border: 1px solid transparent;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-2);
  white-space: nowrap;
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-lg {
  padding: var(--spacing-4) var(--spacing-8);
  font-size: var(--font-size-lg);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.icon {
  font-style: normal;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal {
  background: var(--color-background);
  border-radius: var(--radius-xl);
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--color-border);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-6);
  border-bottom: 1px solid var(--color-border);
}

.modal-header h3 {
  margin: 0;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.close-btn {
  background: none;
  border: none;
  font-size: var(--font-size-2xl);
  cursor: pointer;
  color: var(--color-text-secondary);
  padding: var(--spacing-2);
  border-radius: var(--radius-base);
  transition: all var(--transition-fast);
}

.close-btn:hover {
  color: var(--color-text-primary);
  background-color: var(--color-background-muted);
}

.modal-body {
  padding: var(--spacing-6);
}

.modal-footer {
  padding: var(--spacing-6);
  border-top: 1px solid var(--color-border);
  background: var(--color-background-secondary);
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.btn-danger {
  background-color: var(--color-danger);
  color: white;
  border: 1px solid var(--color-danger);
}

.btn-danger:hover:not(:disabled) {
  background-color: var(--color-danger-hover);
  border-color: var(--color-danger-hover);
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: var(--spacing-4);
    align-items: flex-start;
  }
  
  .tabs {
    flex-direction: column;
  }
  
  .tab {
    flex: none;
  }
}
</style>
