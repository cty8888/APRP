<template>
  <div class="student-class-detail">
    <div class="container">
      <div class="page-header">
        <nav class="breadcrumb">
          <router-link to="/my-classes" class="breadcrumb-item">我的班级</router-link>
          <span class="breadcrumb-separator">/</span>
          <span class="breadcrumb-current">班级详情</span>
        </nav>
        <h1>班级任务</h1>
        <p class="page-subtitle">查看和完成班级中的任务</p>
      </div>
      
      <div class="class-content">
        <div class="assignments-grid">
          <div class="assignment-card">
            <div class="card-header">
              <h3>暂无任务</h3>
            </div>
            <div class="card-body">
              <p>当前班级还没有发布任务，请稍后查看。</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 暂时不使用路由参数，后续会根据实际需求添加
</script>

<style scoped>
.breadcrumb {
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  font-size: var(--font-size-sm);
  margin-bottom: var(--spacing-4);
}

.breadcrumb-item {
  color: var(--color-primary);
  text-decoration: none;
}

.breadcrumb-separator {
  color: var(--color-text-muted);
}

.breadcrumb-current {
  color: var(--color-text-secondary);
}

.assignments-grid {
  display: grid;
  gap: var(--spacing-6);
}

.assignment-card {
  background: var(--color-background);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

.assignment-card .card-header {
  padding: var(--spacing-6);
  border-bottom: 1px solid var(--color-border);
}

.assignment-card .card-header h3 {
  margin: 0;
  font-size: var(--font-size-lg);
  color: var(--color-text-primary);
}

.assignment-card .card-body {
  padding: var(--spacing-6);
}

.assignment-card .card-body p {
  margin: 0;
  color: var(--color-text-secondary);
}
</style>
