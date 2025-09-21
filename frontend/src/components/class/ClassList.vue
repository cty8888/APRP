<template>
  <div class="class-list">
    <div class="class-list-header">
      <h2 class="section-title">
        <i class="icon">🏫</i>
        我的班级
      </h2>
      <button @click="refreshClasses" class="btn-refresh" :disabled="isLoading">
        <i class="icon">🔄</i>
        刷新
      </button>
    </div>

    <div v-if="isLoading" class="loading">
      加载中...
    </div>

    <div v-else-if="classes.length === 0" class="empty-state">
      暂无班级
    </div>

    <div v-else class="class-list">
      <div 
        v-for="classItem in classes" 
        :key="classItem.id" 
        class="class-item"
      >
         <div class="class-content">
           <!-- 顶部：班级名 + 描述 -->
           <div class="class-header">
             <div class="class-title-section">
               <h3 class="class-title">{{ classItem.name }}</h3>
               <p v-if="classItem.description" class="class-description">{{ classItem.description }}</p>
             </div>
             <div class="class-role-badge">
               <span class="role-text">{{ getRoleText(classItem.my_role) }}</span>
             </div>
           </div>
           
           <!-- 中间：班级信息 -->
           <div class="class-info-panel">
             <div class="info-row">
               <div class="info-item">
                 <span class="info-label">学生人数：</span>
                 <span class="info-value info-bold">{{ classItem.student_count }}人</span>
               </div>
               <div class="info-item">
                 <span class="info-label">班级代码：</span>
                 <span class="info-value info-bold">{{ classItem.class_code }}</span>
               </div>
             </div>
             <div class="info-row">
               <div class="info-item">
                 <span class="info-label">主教师：</span>
                 <span class="info-value">{{ classItem.teacher_name }}</span>
               </div>
               <div class="info-item">
                 <span class="info-label">助理教师：</span>
                 <span class="info-value">0人</span>
               </div>
             </div>
           </div>
           
           <!-- 底部：操作按钮 -->
           <div class="class-actions">
             <button 
               @click="$emit('selectClass', classItem)"
               class="btn btn-primary"
             >
               <i class="icon">👁️</i>
               查看班级详情
             </button>
             
             <!-- 只有主教师可以编辑班级 -->
             <template v-if="classItem.my_role === 'main_teacher'">
               <button 
                 @click.stop="editClass(classItem)"
                 class="btn btn-outline"
               >
                 <i class="icon">✏️</i>
                 编辑班级
               </button>
             </template>
           </div>
         </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { classApi } from '../../api'
import type { ClassResponse } from '../../types'

const emit = defineEmits<{
  selectClass: [classItem: ClassResponse]
  editClass: [classItem: ClassResponse]
  viewStudents: [classItem: ClassResponse]
  classDeleted: [classId: number]
}>()

const classes = ref<ClassResponse[]>([])
const isLoading = ref(false)

const getRoleText = (role: string) => {
  switch (role) {
    case 'main_teacher': return '主教师'
    case 'assistant_teacher': return '助教'
    case 'student': return '学生'
    default: return role
  }
}


const refreshClasses = async () => {
  isLoading.value = true
  try {
    classes.value = await classApi.getMyClasses()
  } catch (error) {
    console.error('Failed to load classes:', error)
  } finally {
    isLoading.value = false
  }
}

const editClass = (classItem: ClassResponse) => {
  // 发出编辑事件，让父组件处理
  emit('editClass', classItem)
}

const viewStudents = (classItem: ClassResponse) => {
  // 发出查看学生事件，让父组件处理
  emit('viewStudents', classItem)
}

const deleteClass = async (classId: number) => {
  if (!confirm('确定要删除这个班级吗？此操作不可撤销。')) {
    return
  }
  
  try {
    await classApi.delete(classId)
    // 刷新班级列表
    await refreshClasses()
    emit('classDeleted', classId)
  } catch (error) {
    console.error('Failed to delete class:', error)
    alert('删除班级失败，请重试')
  }
}

onMounted(() => {
  refreshClasses()
})

// 暴露刷新方法给父组件
defineExpose({
  refreshClasses
})
</script>

<style scoped>
.class-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-8);
  padding-bottom: var(--spacing-4);
  border-bottom: 2px solid var(--color-border-light);
}

.section-title {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin: 0;
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
}

.section-title .icon {
  font-size: var(--font-size-xl);
}

.btn-refresh {
  background: var(--color-background-muted);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-3) var(--spacing-4);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-2);
  height: 40px;
}

.btn-refresh:hover:not(:disabled) {
  background: var(--color-primary-light);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.btn-refresh:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.icon {
  font-style: normal;
}

.loading, .empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 1.2rem;
}

.class-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-6);
}

.class-item {
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-6);
  transition: all var(--transition-fast);
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
  min-height: 140px;
}

.class-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light));
  opacity: 0;
  transition: opacity var(--transition-fast);
}

.class-item:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.class-item:hover::before {
  opacity: 1;
}

.class-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
  height: 100%;
}

.class-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--spacing-4);
}

.class-title-section {
  flex: 1;
}

.class-title {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-2) 0;
  line-height: 1.2;
}

.class-description {
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  margin: 0;
  line-height: 1.4;
  max-width: 500px;
}

.class-role-badge {
  flex-shrink: 0;
}

.role-text {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-hover));
  color: white;
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  box-shadow: var(--shadow-sm);
  display: inline-block;
}

.class-info-panel {
  background: var(--color-background-light);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-4);
  flex: 1;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-3);
}

.info-row:last-child {
  margin-bottom: 0;
}

.info-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  flex: 1;
}

.info-item:first-child {
  margin-right: var(--spacing-6);
}

.info-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-medium);
  white-space: nowrap;
}

.info-value {
  font-size: var(--font-size-sm);
  color: var(--color-text-primary);
  font-weight: var(--font-weight-medium);
  word-break: break-word;
}

.info-bold {
  font-weight: var(--font-weight-bold);
  color: var(--color-text-primary);
}

.class-actions {
  display: flex;
  gap: var(--spacing-3);
  flex-shrink: 0;
  align-items: center;
  justify-content: flex-end;
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

.btn-outline {
  background-color: transparent;
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

.btn-outline:hover:not(:disabled) {
  background-color: var(--color-background-muted);
  border-color: var(--color-text-primary);
}

.btn {
  padding: var(--spacing-3) var(--spacing-4);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  border: 1px solid transparent;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
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
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
