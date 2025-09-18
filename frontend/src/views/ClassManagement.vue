<template>
  <div class="class-management">
    <div class="container">
      <div class="page-header">
        <h1>班级管理</h1>
        <p class="page-subtitle">管理您的班级，创建和加入学习班级</p>
      </div>

      <div class="tabs">
        <button 
          :class="['tab', { active: activeTab === 'list' }]"
          @click="activeTab = 'list'"
        >
          我的班级
        </button>
        <button 
          :class="['tab', { active: activeTab === 'create' }]"
          @click="activeTab = 'create'"
          v-if="user?.role === 'teacher'"
        >
          创建班级
        </button>
        <button 
          :class="['tab', { active: activeTab === 'join' }]"
          @click="activeTab = 'join'"
        >
          加入班级
        </button>
      </div>

      <div class="tab-content">
        <!-- 班级列表 -->
        <div v-if="activeTab === 'list'" class="tab-pane">
          <ClassList 
            ref="classListRef"
            @selectClass="handleSelectClass" 
          />
        </div>

        <!-- 创建班级 -->
        <div v-if="activeTab === 'create'" class="tab-pane">
          <div class="form-container">
            <CreateClassForm @success="handleCreateSuccess" />
          </div>
        </div>

        <!-- 加入班级 -->
        <div v-if="activeTab === 'join'" class="tab-pane">
          <div class="form-container">
            <JoinClassForm @success="handleJoinSuccess" />
          </div>
        </div>
      </div>
    </div>

    <!-- 班级详情弹窗 -->
    <div v-if="selectedClass" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>{{ selectedClass.name }}</h3>
          <button @click="closeModal" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="class-details">
            <p><strong>班级代码：</strong>{{ selectedClass.class_code }}</p>
            <p><strong>描述：</strong>{{ selectedClass.description || '无' }}</p>
            <p><strong>主教师：</strong>{{ selectedClass.teacher_name }}</p>
            <p><strong>学生数量：</strong>{{ selectedClass.student_count }}</p>
            <p><strong>我的角色：</strong>{{ getRoleText(selectedClass.my_role) }}</p>
            <p><strong>创建时间：</strong>{{ formatDate(selectedClass.created_at) }}</p>
          </div>
          
          <div class="modal-actions">
            <router-link 
              :to="`/assignments?classId=${selectedClass.id}`"
              class="btn btn-primary"
            >
              查看任务
            </router-link>
            <router-link 
              :to="`/submissions?classId=${selectedClass.id}`"
              class="btn btn-outline"
            >
              查看提交
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '../store/auth'
import { ClassList, CreateClassForm, JoinClassForm } from '../components'
import type { ClassResponse } from '../types'

const { user } = useAuth()

const activeTab = ref('list')
const selectedClass = ref<ClassResponse | null>(null)
const classListRef = ref()

const getRoleText = (role: string) => {
  switch (role) {
    case 'main_teacher': return '主教师'
    case 'assistant_teacher': return '助教'
    case 'student': return '学生'
    default: return role
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const handleSelectClass = (classItem: ClassResponse) => {
  selectedClass.value = classItem
}

const closeModal = () => {
  selectedClass.value = null
}

const handleCreateSuccess = (classData: any) => {
  console.log('班级创建成功:', classData)
  activeTab.value = 'list'
  // 刷新班级列表
  if (classListRef.value) {
    classListRef.value.refreshClasses()
  }
}

const handleJoinSuccess = (data: any) => {
  console.log('加入班级成功:', data)
  activeTab.value = 'list'
  // 刷新班级列表
  if (classListRef.value) {
    classListRef.value.refreshClasses()
  }
}
</script>

<style scoped>
.class-management {
  padding: var(--spacing-8) 0;
}

.page-header {
  text-align: center;
  margin-bottom: var(--spacing-10);
}

.page-header h1 {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-3);
}

.page-subtitle {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin: 0;
}

.tabs {
  display: flex;
  justify-content: center;
  border-bottom: 2px solid var(--color-border);
  margin-bottom: var(--spacing-8);
  gap: var(--spacing-2);
}

.tab {
  background: none;
  border: none;
  padding: var(--spacing-4) var(--spacing-6);
  cursor: pointer;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
  transition: all var(--transition-fast);
  border-radius: var(--radius-md) var(--radius-md) 0 0;
  position: relative;
}

.tab:hover {
  color: var(--color-text-primary);
  background-color: var(--color-background-muted);
}

.tab.active {
  color: var(--color-primary);
  background-color: var(--color-background);
  border-bottom: 2px solid var(--color-primary);
  margin-bottom: -2px;
  font-weight: var(--font-weight-semibold);
}

.tab-content {
  max-width: 600px;
  margin: 0 auto;
}

.form-container {
  max-width: 500px;
  margin: 0 auto;
  padding: var(--spacing-6);
  background: var(--color-background);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

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

.class-details p {
  margin: var(--spacing-4) 0;
  font-size: var(--font-size-base);
  color: var(--color-text-primary);
}

.class-details strong {
  color: var(--color-text-primary);
  font-weight: var(--font-weight-semibold);
}

.modal-actions {
  display: flex;
  gap: var(--spacing-4);
  margin-top: var(--spacing-8);
}

.modal-actions .btn {
  flex: 1;
  text-align: center;
  text-decoration: none;
}
</style>
