<template>
  <div class="assignment-management">
    <div class="page-header">
      <h1>任务管理</h1>
    </div>

    <div class="tabs">
      <button 
        :class="['tab', { active: activeTab === 'list' }]"
        @click="activeTab = 'list'"
      >
        {{ classId ? '班级任务' : '我的任务' }}
      </button>
      <button 
        :class="['tab', { active: activeTab === 'create' }]"
        @click="activeTab = 'create'"
        v-if="user?.role === 'teacher'"
      >
        创建任务
      </button>
    </div>

    <div class="tab-content">
      <!-- 任务列表 -->
      <div v-if="activeTab === 'list'" class="tab-pane">
        <AssignmentList 
          ref="assignmentListRef"
          :title="classId ? '班级任务' : '我的任务'"
          :classId="classId"
          @selectAssignment="handleSelectAssignment" 
        />
      </div>

      <!-- 创建任务 -->
      <div v-if="activeTab === 'create'" class="tab-pane">
        <div class="form-container">
          <CreateAssignmentForm @success="handleCreateSuccess" />
        </div>
      </div>
    </div>

    <!-- 任务详情弹窗 -->
    <div v-if="selectedAssignment" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>{{ selectedAssignment.title }}</h3>
          <button @click="closeModal" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="assignment-details">
            <p><strong>描述：</strong>{{ selectedAssignment.description || '无' }}</p>
            <p><strong>班级：</strong>{{ selectedAssignment.class_name }}</p>
            <p><strong>教师：</strong>{{ selectedAssignment.teacher_name }}</p>
            <p><strong>创建时间：</strong>{{ formatDate(selectedAssignment.created_at) }}</p>
          </div>
          
          <div class="modal-actions">
            <router-link 
              :to="`/submissions?assignmentId=${selectedAssignment.id}`"
              class="btn btn-primary"
            >
              查看提交
            </router-link>
            
            <router-link 
              v-if="user?.role === 'student'"
              :to="`/submit?assignmentId=${selectedAssignment.id}`"
              class="btn btn-outline"
            >
              提交作业
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuth } from '../store/auth'
import { AssignmentList, CreateAssignmentForm } from '../components'
import type { AssignmentResponse } from '../types'

const route = useRoute()
const { user } = useAuth()

const activeTab = ref('list')
const selectedAssignment = ref<AssignmentResponse | null>(null)
const assignmentListRef = ref()
const classId = ref<number | undefined>()

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const handleSelectAssignment = (assignment: AssignmentResponse) => {
  selectedAssignment.value = assignment
}

const closeModal = () => {
  selectedAssignment.value = null
}

const handleCreateSuccess = (assignmentData: any) => {
  console.log('任务创建成功:', assignmentData)
  activeTab.value = 'list'
  // 刷新任务列表
  if (assignmentListRef.value) {
    assignmentListRef.value.refreshAssignments()
  }
}

onMounted(() => {
  // 从路由参数获取classId
  if (route.query.classId) {
    classId.value = parseInt(route.query.classId as string)
  }
})
</script>

<style scoped>
.assignment-management {
  padding: 2rem 0;
}

.page-header {
  margin-bottom: 2rem;
}

.tabs {
  display: flex;
  border-bottom: 2px solid #e9ecef;
  margin-bottom: 2rem;
}

.tab {
  background: none;
  border: none;
  padding: 1rem 2rem;
  cursor: pointer;
  font-size: 1.2rem;
  color: #666;
  transition: all 0.2s;
}

.tab:hover {
  color: #007bff;
}

.tab.active {
  color: #007bff;
  border-bottom: 2px solid #007bff;
  margin-bottom: -2px;
}

.form-container {
  max-width: 500px;
  margin: 0 auto;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.6rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 1.5rem;
}

.assignment-details p {
  margin: 1rem 0;
  font-size: 1.1rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.modal-actions .btn {
  flex: 1;
  text-align: center;
  text-decoration: none;
}
</style>
