<template>
  <div class="submission-detail">
    <div class="container">
      <!-- 页面头部 -->
      <div class="page-header">
        <nav class="breadcrumb">
          <router-link to="/dashboard" class="breadcrumb-item">仪表板</router-link>
          <span class="breadcrumb-separator">/</span>
          <router-link 
            :to="user?.role === 'teacher' ? '/classes' : '/my-classes'" 
            class="breadcrumb-item"
          >
            {{ user?.role === 'teacher' ? '班级管理' : '我的班级' }}
          </router-link>
          <span class="breadcrumb-separator">/</span>
          <span class="breadcrumb-current">提交详情</span>
        </nav>
        <h1 class="page-title">
          <i class="icon">📋</i>
          提交详情
        </h1>
        <p class="page-subtitle">查看作业提交的详细信息</p>
      </div>

      <!-- 加载状态 -->
      <div v-if="isLoading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="hasError" class="error-container">
        <div class="error-icon">⚠️</div>
        <h3>加载失败</h3>
        <p>{{ errorMessage }}</p>
        <div class="debug-info">
          <p><strong>调试信息：</strong></p>
          <ul>
            <li>路由参数: {{ JSON.stringify(route.params) }}</li>
            <li>提交ID: {{ submissionId }}</li>
            <li>当前路径: {{ route.path }}</li>
          </ul>
        </div>
        <button @click="loadSubmissionDetail" class="btn btn-primary">
          重试
        </button>
      </div>

      <!-- 提交详情内容 -->
      <div v-else-if="submissionDetail" class="submission-content">
        <!-- 基本信息卡片 -->
        <div class="info-card">
          <div class="card-header">
            <h2>基本信息</h2>
            <div class="header-actions">
              <button 
                v-if="submissionDetail.is_graded && submissionDetail.report"
                @click="exportReport"
                class="btn btn-outline"
                :disabled="isExporting"
              >
                <i class="icon">📄</i>
                {{ isExporting ? '导出中...' : '导出报告' }}
              </button>
            </div>
          </div>
          <div class="card-body">
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">学生姓名</span>
                <div class="student-info">
                  <div class="avatar">{{ getInitials(submissionDetail.student_name) }}</div>
                  <span>{{ submissionDetail.student_name }}</span>
                </div>
              </div>
              
              <div class="info-item">
                <span class="info-label">任务名称</span>
                <span class="info-value">{{ submissionDetail.assignment_title }}</span>
              </div>
              
              <div class="info-item">
                <span class="info-label">班级名称</span>
                <span class="info-value">{{ submissionDetail.class_name }}</span>
              </div>
              
              <div class="info-item">
                <span class="info-label">提交时间</span>
                <span class="info-value">{{ formatDate(submissionDetail.submitted_at) }}</span>
              </div>
              
              <div class="info-item">
                <span class="info-label">批改状态</span>
                <span :class="['status-badge', submissionDetail.is_graded ? 'graded' : 'pending']">
                  {{ submissionDetail.is_graded ? '已批改' : '待批改' }}
                </span>
              </div>
              
              <div class="info-item">
                <span class="info-label">分数</span>
                <span v-if="submissionDetail.score !== null" class="score-badge">
                  {{ submissionDetail.score }}分
                </span>
                <span v-else class="no-score-badge">未批改</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 批改报告卡片 -->
        <div v-if="submissionDetail.is_graded && submissionDetail.report" class="report-card">
          <div class="card-header">
            <h2>批改报告</h2>
            <div class="report-meta">
              <span v-if="submissionDetail.graded_at">
                批改时间：{{ formatDate(submissionDetail.graded_at) }}
              </span>
            </div>
          </div>
          <div class="card-body">
            <div class="report-content">
              <div class="report-text">{{ submissionDetail.report }}</div>
            </div>
          </div>
        </div>

        <!-- 文档解析内容卡片 -->
        <div v-if="submissionDetail.file_json" class="file-content-card">
          <div class="card-header">
            <h2>文档解析内容</h2>
            <div class="header-actions">
              <button 
                @click="downloadOriginalFile"
                class="btn btn-outline"
                :disabled="isDownloading"
              >
                <i class="icon">📥</i>
                {{ isDownloading ? '下载中...' : '下载原始文件' }}
              </button>
            </div>
          </div>
          <div class="card-body">
            <div class="parsed-content">
              <!-- 文档统计信息 -->
              <div class="content-section">
                <h3>文档统计</h3>
                <div class="stats-grid">
                  <div class="stat-item">
                    <span class="stat-label">总字数</span>
                    <span class="stat-value">{{ submissionDetail.file_json.total_words_count || 0 }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">段落数</span>
                    <span class="stat-value">{{ submissionDetail.file_json.paragraph_count || 0 }}</span>
                  </div>
                </div>
              </div>

              <!-- 文档大纲 -->
              <div v-if="submissionDetail.file_json.outline && submissionDetail.file_json.outline.length > 0" class="content-section">
                <h3>文档大纲</h3>
                <div class="outline-container">
                  <div 
                    v-for="item in submissionDetail.file_json.outline" 
                    :key="item.id"
                    :class="['outline-item', `level-${item.level}`]"
                  >
                    <span class="outline-text">{{ item.text }}</span>
                    <span class="outline-style">{{ item.style }}</span>
                  </div>
                </div>
              </div>

              <!-- 段落内容 -->
              <div v-if="submissionDetail.file_json.paragraphs && submissionDetail.file_json.paragraphs.length > 0" class="content-section">
                <h3>段落内容</h3>
                <div class="paragraphs-container">
                  <div 
                    v-for="para in submissionDetail.file_json.paragraphs" 
                    :key="para.id"
                    class="paragraph-item"
                  >
                    <div class="paragraph-header">
                      <span class="paragraph-id">段落 {{ para.id + 1 }}</span>
                      <span class="paragraph-count">{{ para.word_count }} 字</span>
                    </div>
                    <div class="paragraph-text">{{ para.text }}</div>
                  </div>
                </div>
              </div>

              <!-- 原始JSON数据（可折叠） -->
              <div class="content-section">
                <h3 @click="toggleJsonView" class="collapsible-header">
                  <i class="icon">{{ showJsonView ? '▼' : '▶' }}</i>
                  原始JSON数据
                </h3>
                <div v-if="showJsonView" class="json-viewer">
                  <pre>{{ formatJson(submissionDetail.file_json) }}</pre>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <button @click="goBack" class="btn btn-secondary">
            <i class="icon">←</i>
            返回
          </button>
          
          <button 
            v-if="user?.role === 'teacher' && !isGrading"
            @click="startGrading"
            class="btn btn-primary"
          >
            <i class="icon">✏️</i>
            {{ submissionDetail.is_graded ? '修改批改' : '开始批改' }}
          </button>
        </div>
      </div>

      <!-- 批改表单弹窗 -->
      <div v-if="isGrading && submissionDetail" class="modal-overlay" @click="cancelGrading">
        <div class="modal" @click.stop>
          <div class="modal-header">
            <h3>批改作业</h3>
            <button @click="cancelGrading" class="close-btn">&times;</button>
          </div>
          <div class="modal-body">
            <GradeSubmissionForm 
              :submissionId="submissionDetail.id"
              @success="handleGradeSuccess"
              @cancel="cancelGrading"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '../store/auth'
import { submissionApi } from '../api'
import { GradeSubmissionForm } from '../components'
import type { SubmissionDetailResponse } from '../types'
import { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } from 'docx'
import { saveAs } from 'file-saver'

const route = useRoute()
const router = useRouter()
const { user } = useAuth()

const submissionDetail = ref<SubmissionDetailResponse | null>(null)
const isLoading = ref(true)
const hasError = ref(false)
const errorMessage = ref('')
const isGrading = ref(false)
const isDownloading = ref(false)
const isExporting = ref(false)
const showJsonView = ref(false)

const submissionId = ref<number>()

const getInitials = (name: string) => {
  if (!name) return '?'
  return name.charAt(0).toUpperCase()
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

const formatJson = (jsonData: any) => {
  if (!jsonData) return '无数据'
  try {
    return JSON.stringify(jsonData, null, 2)
  } catch (error) {
    return '数据格式错误'
  }
}

const toggleJsonView = () => {
  showJsonView.value = !showJsonView.value
}

const loadSubmissionDetail = async () => {
  if (!submissionId.value) return
  
  try {
    isLoading.value = true
    hasError.value = false
    errorMessage.value = ''
    
    submissionDetail.value = await submissionApi.getSubmissionDetail(submissionId.value)
  } catch (error: any) {
    console.error('Failed to load submission detail:', error)
    hasError.value = true
    errorMessage.value = error.response?.data?.detail || '加载提交详情失败'
  } finally {
    isLoading.value = false
  }
}

const goBack = () => {
  router.go(-1)
}

const startGrading = () => {
  isGrading.value = true
}

const cancelGrading = () => {
  isGrading.value = false
}

const handleGradeSuccess = () => {
  isGrading.value = false
  loadSubmissionDetail() // 重新加载数据
}

const downloadOriginalFile = async () => {
  if (!submissionDetail.value) return
  
  try {
    isDownloading.value = true
    const blob = await submissionApi.downloadOriginalFile(submissionDetail.value.id)
    
    // 创建下载链接
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `submission_${submissionDetail.value.id}.docx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Failed to download file:', error)
    alert('下载文件失败')
  } finally {
    isDownloading.value = false
  }
}

const exportReport = async () => {
  if (!submissionDetail.value || !submissionDetail.value.report) {
    console.error('No submission detail or report available')
    return
  }
  
  try {
    isExporting.value = true
    console.log('Starting report export...')
    
    // 创建DOCX文档
    const doc = new Document({
      sections: [{
        properties: {},
        children: [
          // 标题
          new Paragraph({
            children: [
              new TextRun({
                text: "作业批改报告",
                bold: true,
                size: 32,
                color: "2563eb"
              })
            ],
            heading: HeadingLevel.TITLE,
            alignment: AlignmentType.CENTER,
            spacing: { after: 400 }
          }),
          
          // 基本信息标题
          new Paragraph({
            children: [
              new TextRun({
                text: "基本信息",
                bold: true,
                size: 24,
                color: "1f2937"
              })
            ],
            heading: HeadingLevel.HEADING_1,
            spacing: { before: 300, after: 200 }
          }),
          
          // 学生姓名
          new Paragraph({
            children: [
              new TextRun({
                text: "学生姓名：",
                bold: true
              }),
              new TextRun({
                text: submissionDetail.value.student_name || '未知'
              })
            ],
            spacing: { after: 100 }
          }),
          
          // 任务名称
          new Paragraph({
            children: [
              new TextRun({
                text: "任务名称：",
                bold: true
              }),
              new TextRun({
                text: submissionDetail.value.assignment_title || '未知'
              })
            ],
            spacing: { after: 100 }
          }),
          
          // 班级名称
          new Paragraph({
            children: [
              new TextRun({
                text: "班级名称：",
                bold: true
              }),
              new TextRun({
                text: submissionDetail.value.class_name || '未知'
              })
            ],
            spacing: { after: 100 }
          }),
          
          // 提交时间
          new Paragraph({
            children: [
              new TextRun({
                text: "提交时间：",
                bold: true
              }),
              new TextRun({
                text: formatDate(submissionDetail.value.submitted_at)
              })
            ],
            spacing: { after: 100 }
          }),
          
          // 批改时间
          new Paragraph({
            children: [
              new TextRun({
                text: "批改时间：",
                bold: true
              }),
              new TextRun({
                text: submissionDetail.value.graded_at ? formatDate(submissionDetail.value.graded_at) : '未批改'
              })
            ],
            spacing: { after: 100 }
          }),
          
          // 分数
          new Paragraph({
            children: [
              new TextRun({
                text: "分数：",
                bold: true
              }),
              new TextRun({
                text: submissionDetail.value.score ? `${submissionDetail.value.score}分` : '未评分',
                color: submissionDetail.value.score ? (submissionDetail.value.score >= 80 ? "10b981" : submissionDetail.value.score >= 60 ? "f59e0b" : "ef4444") : "6b7280"
              })
            ],
            spacing: { after: 200 }
          }),
          
          // 批改报告标题
          new Paragraph({
            children: [
              new TextRun({
                text: "批改报告",
                bold: true,
                size: 24,
                color: "1f2937"
              })
            ],
            heading: HeadingLevel.HEADING_1,
            spacing: { before: 300, after: 200 }
          }),
          
          // 批改报告内容
          new Paragraph({
            children: [
              new TextRun({
                text: submissionDetail.value.report,
                size: 20
              })
            ],
            spacing: { after: 300 }
          }),
          
          // 分隔线
          new Paragraph({
            children: [
              new TextRun({
                text: "─".repeat(50),
                color: "d1d5db"
              })
            ],
            alignment: AlignmentType.CENTER,
            spacing: { before: 400, after: 200 }
          }),
          
          // 页脚
          new Paragraph({
            children: [
              new TextRun({
                text: "此报告由APRP系统自动生成",
                italics: true,
                color: "6b7280",
                size: 18
              })
            ],
            alignment: AlignmentType.CENTER,
            spacing: { before: 200 }
          })
        ]
      }]
    })
    
    console.log('Document created, generating blob...')
    
    // 生成并下载DOCX文件
    const blob = await Packer.toBlob(doc)
    console.log('Blob created, saving file...')
    
    const fileName = `批改报告_${submissionDetail.value.student_name || '未知'}_${submissionDetail.value.assignment_title || '未知'}.docx`
    saveAs(blob, fileName)
    
    console.log('File saved successfully')
    
  } catch (error) {
    console.error('Failed to export report:', error)
    console.error('Error details:', error.message)
    alert(`导出报告失败: ${error.message}`)
  } finally {
    isExporting.value = false
  }
}

onMounted(() => {
  const id = route.params.id as string
  console.log('Route params:', route.params)
  console.log('Submission ID from route:', id)
  
  if (id) {
    submissionId.value = parseInt(id)
    console.log('Parsed submission ID:', submissionId.value)
    loadSubmissionDetail()
  } else {
    console.error('No submission ID found in route params')
    hasError.value = true
    errorMessage.value = '无效的提交ID'
    isLoading.value = false
  }
})
</script>

<style scoped>
.submission-detail {
  padding: var(--spacing-8) 0;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  min-height: 100vh;
}

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
  transition: color var(--transition-fast);
}

.breadcrumb-item:hover {
  color: var(--color-primary-hover);
}

.breadcrumb-separator {
  color: var(--color-text-muted);
}

.breadcrumb-current {
  color: var(--color-text-secondary);
}

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

.debug-info {
  background: #f7fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0;
  text-align: left;
  font-family: monospace;
  font-size: 0.9rem;
}

.debug-info ul {
  margin: 0.5rem 0;
  padding-left: 1rem;
}

.debug-info li {
  margin: 0.25rem 0;
}

.submission-content {
  display: grid;
  gap: var(--spacing-8);
}

.info-card, .report-card, .file-content-card {
  background: var(--color-background);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--color-border);
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-6);
  border-bottom: 1px solid var(--color-border);
  background: var(--color-background-muted);
}

.card-header h2 {
  margin: 0;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
}

.header-actions {
  display: flex;
  gap: var(--spacing-3);
}

.card-body {
  padding: var(--spacing-6);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-6);
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2);
}

.info-label {
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: var(--font-size-base);
  color: var(--color-text-primary);
  font-weight: var(--font-weight-medium);
}

.student-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-3);
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-hover));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-weight-semibold);
  font-size: var(--font-size-lg);
  flex-shrink: 0;
}

.status-badge {
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  display: inline-block;
  width: fit-content;
}

.status-badge.graded {
  background: var(--color-success-light);
  color: var(--color-success);
}

.status-badge.pending {
  background: var(--color-warning-light);
  color: var(--color-warning);
}

.score-badge {
  background: var(--color-success-light);
  color: var(--color-success);
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  display: inline-block;
  width: fit-content;
}

.no-score-badge {
  background: var(--color-background-muted);
  color: var(--color-text-secondary);
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  display: inline-block;
  width: fit-content;
}

.report-meta {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.report-content {
  background: var(--color-background-muted);
  border-radius: var(--radius-lg);
  padding: var(--spacing-6);
  border: 1px solid var(--color-border);
}

.report-text {
  font-size: var(--font-size-base);
  line-height: 1.6;
  color: var(--color-text-primary);
  white-space: pre-wrap;
  word-break: break-word;
}

.parsed-content {
  padding: var(--spacing-4);
}

.content-section {
  margin-bottom: var(--spacing-6);
}

.content-section h3 {
  margin: 0 0 var(--spacing-4) 0;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--color-text-primary);
  border-bottom: 2px solid var(--color-border);
  padding-bottom: var(--spacing-2);
}

.json-viewer {
  background: var(--color-background-muted);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-4);
  overflow-x: auto;
  max-height: 500px;
  overflow-y: auto;
}

.json-viewer pre {
  margin: 0;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: var(--font-size-sm);
  line-height: 1.5;
  color: var(--color-text-primary);
  white-space: pre-wrap;
  word-break: break-word;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-4);
  margin-bottom: var(--spacing-4);
}

.stat-item {
  background: var(--color-background-muted);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-4);
  text-align: center;
  transition: all var(--transition-fast);
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.stat-label {
  display: block;
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-2);
  font-weight: var(--font-weight-medium);
}

.stat-value {
  display: block;
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
}

.outline-container {
  background: var(--color-background-muted);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-4);
  max-height: 400px;
  overflow-y: auto;
}

.outline-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-3) var(--spacing-4);
  margin-bottom: var(--spacing-2);
  border-radius: var(--radius-md);
  transition: all var(--transition-fast);
  border-left: 4px solid transparent;
}

.outline-item:hover {
  background: var(--color-background-light);
}

.outline-item.level-0 {
  border-left-color: var(--color-primary);
  background: var(--color-primary-light);
}

.outline-item.level-1 {
  border-left-color: var(--color-success);
  margin-left: var(--spacing-4);
}

.outline-item.level-2 {
  border-left-color: var(--color-warning);
  margin-left: calc(var(--spacing-4) * 2);
}

.outline-item.level-3 {
  border-left-color: var(--color-info);
  margin-left: calc(var(--spacing-4) * 3);
}

.outline-text {
  font-weight: var(--font-weight-medium);
  color: var(--color-text-primary);
  flex: 1;
}

.outline-style {
  font-size: var(--font-size-sm);
  color: var(--color-text-muted);
  background: var(--color-background);
  padding: var(--spacing-1) var(--spacing-2);
  border-radius: var(--radius-sm);
  font-family: monospace;
}

.paragraphs-container {
  max-height: 500px;
  overflow-y: auto;
  background: var(--color-background-muted);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-4);
}

.paragraph-item {
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-4);
  margin-bottom: var(--spacing-4);
  transition: all var(--transition-fast);
}

.paragraph-item:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.paragraph-item:last-child {
  margin-bottom: 0;
}

.paragraph-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-3);
  padding-bottom: var(--spacing-2);
  border-bottom: 1px solid var(--color-border-light);
}

.paragraph-id {
  font-weight: var(--font-weight-semibold);
  color: var(--color-primary);
  font-size: var(--font-size-sm);
}

.paragraph-count {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  background: var(--color-background-muted);
  padding: var(--spacing-1) var(--spacing-2);
  border-radius: var(--radius-sm);
}

.paragraph-text {
  line-height: 1.6;
  color: var(--color-text-primary);
  white-space: pre-wrap;
  word-break: break-word;
}

.collapsible-header {
  cursor: pointer;
  user-select: none;
  display: flex;
  align-items: center;
  gap: var(--spacing-2);
  transition: color var(--transition-fast);
}

.collapsible-header:hover {
  color: var(--color-primary);
}

.collapsible-header .icon {
  transition: transform var(--transition-fast);
}

.file-actions {
  text-align: center;
  padding: var(--spacing-6);
}

.file-info {
  margin-top: var(--spacing-4);
  color: var(--color-text-secondary);
  font-size: var(--font-size-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-2);
}

.no-content-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-4);
  opacity: 0.5;
}

.no-content p {
  margin: 0 0 var(--spacing-2) 0;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-medium);
}

.no-content small {
  color: var(--color-text-muted);
  font-size: var(--font-size-sm);
}

.action-buttons {
  display: flex;
  gap: var(--spacing-4);
  justify-content: center;
  padding: var(--spacing-6);
  background: var(--color-background);
  border-radius: var(--radius-xl);
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
  max-width: 600px;
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

.icon {
  font-style: normal;
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .card-header {
    flex-direction: column;
    gap: var(--spacing-4);
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>
