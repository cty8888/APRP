<template>
  <div class="class-management">
    <div class="container">
      <div class="page-header">
        <h1 class="page-title">班级管理</h1>
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
          :class="['tab', { active: activeTab === 'search' }]"
          @click="activeTab = 'search'"
        >
          搜索班级
        </button>
      </div>

      <div class="tab-content">
        <!-- 班级列表 -->
        <div v-if="activeTab === 'list'" class="tab-pane">
          <div class="content-section">
            <ClassList 
              ref="classListRef"
              @selectClass="handleSelectClass"
              @editClass="handleEditClass"
              @viewStudents="handleViewStudents"
              @classDeleted="handleClassDeleted"
            />
          </div>
        </div>

        <!-- 班级详情 -->
        <div v-if="activeTab === 'detail'" class="tab-pane">
          <ClassDetail 
            :classData="selectedClass!"
            @editClass="handleEditClass"
            @createAssignment="handleCreateAssignment"
            @selectAssignment="handleSelectAssignment"
            @submitAssignment="handleSubmitAssignment"
            @viewSubmissions="handleViewSubmissions"
            @editAssignment="handleEditAssignment"
            @deleteAssignment="handleDeleteAssignment"
          />
        </div>

        <!-- 创建班级 -->
        <div v-if="activeTab === 'create'" class="tab-pane">
          <div class="form-container">
            <CreateClassForm @success="handleCreateSuccess" />
          </div>
        </div>

        <!-- 搜索并加入班级 -->
        <div v-if="activeTab === 'search'" class="tab-pane">
          <div class="form-container">
            <SearchClassForm @success="handleSearchSuccess" />
          </div>
        </div>


        <!-- 班级学生列表 -->
        <div v-if="activeTab === 'students'" class="tab-pane">
          <ClassStudentsList 
            :classId="viewingStudentsClass.id"
            :classInfo="viewingStudentsClass"
            @close="handleCloseStudents"
            @viewStudentSubmissions="handleViewStudentSubmissions"
          />
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

    <!-- 编辑班级弹窗 -->
    <div v-if="editingClass" class="modal-overlay" @click="closeEditModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>编辑班级</h3>
          <button @click="closeEditModal" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <EditClassForm 
            :classData="editingClass"
            @success="handleEditSuccess"
            @cancel="closeEditModal"
          />
        </div>
        <div class="modal-footer">
          <button 
            @click="deleteClass(editingClass.id)"
            class="btn btn-danger"
          >
            删除班级
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../store/auth'
import { ClassList, ClassDetail, CreateClassForm, EditClassForm, SearchClassForm, ClassStudentsList } from '../components'
import { classApi } from '../api'
import type { ClassResponse } from '../types'

const router = useRouter()
const { user } = useAuth()

const activeTab = ref('list')
const selectedClass = ref<ClassResponse | null>(null)
const editingClass = ref<ClassResponse | null>(null)
const viewingStudentsClass = ref<{ id: number; name: string }>({ id: 0, name: '' })
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
  // 根据用户角色跳转到不同的任务管理页面
  if (user?.role === 'teacher') {
    router.push(`/classes/${classItem.id}/assignments`)
  } else {
    router.push(`/my-classes/${classItem.id}`)
  }
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

const handleSearchSuccess = (data: any) => {
  console.log('加入班级成功:', data)
  activeTab.value = 'list'
  // 刷新班级列表
  if (classListRef.value) {
    classListRef.value.refreshClasses()
  }
}

const handleEditClass = (classItem: ClassResponse) => {
  editingClass.value = classItem
}

const handleViewStudents = (classItem: ClassResponse) => {
  viewingStudentsClass.value = {
    id: classItem.id,
    name: classItem.name
  }
  activeTab.value = 'students'
}

const handleCloseStudents = () => {
  activeTab.value = 'list'
  viewingStudentsClass.value = { id: 0, name: '' }
}

const handleViewStudentSubmissions = (student: any) => {
  // 跳转到提交管理页面，显示该学生的提交
  window.location.href = `/submissions?studentId=${student.id}`
}

const handleClassDeleted = (classId: number) => {
  console.log('班级删除成功:', classId)
  // 班级列表会自动刷新
}

const handleEditSuccess = (updatedClass: ClassResponse) => {
  console.log('班级编辑成功:', updatedClass)
  editingClass.value = null
  // 刷新班级列表
  if (classListRef.value) {
    classListRef.value.refreshClasses()
  }
}

const closeEditModal = () => {
  editingClass.value = null
}

const deleteClass = async (classId: number) => {
  if (!confirm('确定要删除这个班级吗？此操作不可撤销。')) {
    return
  }
  
  try {
    await classApi.delete(classId)
    // 关闭编辑弹窗
    editingClass.value = null
    // 刷新班级列表
    if (classListRef.value) {
      classListRef.value.refreshClasses()
    }
    console.log('班级删除成功:', classId)
  } catch (error) {
    console.error('Failed to delete class:', error)
    alert('删除班级失败，请重试')
  }
}

const handleCreateAssignment = () => {
  // 跳转到任务管理页面创建任务
  if (selectedClass.value) {
    router.push(`/classes/${selectedClass.value.id}/assignments`)
  }
}

const handleSelectAssignment = (assignment: any) => {
  // 跳转到任务详情页面
  if (selectedClass.value) {
    if (user?.role === 'student') {
      router.push(`/my-classes/${selectedClass.value.id}/assignments/${assignment.id}`)
    } else {
      router.push(`/classes/${selectedClass.value.id}/assignments/${assignment.id}/submissions`)
    }
  }
}

const handleSubmitAssignment = (assignment: any) => {
  // 学生提交作业
  if (selectedClass.value) {
    router.push(`/my-classes/${selectedClass.value.id}/assignments/${assignment.id}`)
  }
}

const handleViewSubmissions = (assignment: any) => {
  // 老师查看提交
  if (selectedClass.value) {
    router.push(`/classes/${selectedClass.value.id}/assignments/${assignment.id}/submissions`)
  }
}

const handleEditAssignment = () => {
  // 编辑任务
  if (selectedClass.value) {
    router.push(`/classes/${selectedClass.value.id}/assignments`)
  }
}

const handleDeleteAssignment = (assignmentId: number) => {
  // 任务删除成功，刷新班级详情
  console.log('任务删除成功:', assignmentId)
}
</script>

<style scoped>
.class-management {
  padding: var(--spacing-8) 0;
}

/* 页面样式使用全局样式类 */

.tab-content {
  width: 100%;
}

.content-section {
  background: var(--color-background);
  border-radius: var(--radius-xl);
  padding: var(--spacing-8);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--color-border);
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

.modal-footer {
  padding: var(--spacing-6);
  border-top: 1px solid var(--color-border);
  background: var(--color-background-secondary);
  display: flex;
  justify-content: flex-start;
  align-items: center;
}
</style>
