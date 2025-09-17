<template>
  <div class="analysis-result">
    <div class="result-header">
      <h2>📊 文档分析结果</h2>
      <button class="btn-download" @click="downloadReport">下载报告</button>
    </div>
    
    <!-- 基础统计 -->
    <div class="stats-section">
      <h3>基础统计</h3>
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-number">{{ result.total_words_count }}</div>
          <div class="stat-label">总字数</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ result.paragraph_count }}</div>
          <div class="stat-label">段落数</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ result.outline?.length || 0 }}</div>
          <div class="stat-label">标题数</div>
        </div>
      </div>
    </div>
    
    <!-- 文档结构 -->
    <div class="outline-section">
      <h3>文档结构</h3>
      <div class="outline-tree">
        <OutlineNode 
          v-for="node in result.outline_tree" 
          :key="node.id" 
          :node="node"
          @nodeClick="scrollToParagraph"
        />
      </div>
    </div>
    
    <!-- 段落详情 -->
    <div class="paragraphs-section">
      <h3>段落详情</h3>
      <div class="paragraphs-list">
        <div 
          v-for="para in result.paragraphs" 
          :key="para.id"
          :id="`paragraph-${para.id}`"
          class="paragraph-item"
          :class="{ 'is-heading': isHeading(para.id) }"
        >
          <div class="paragraph-header">
            <span class="paragraph-id">#{{ para.id }}</span>
            <span class="word-count">{{ para.word_count }} 字</span>
            <span v-if="isHeading(para.id)" class="heading-badge">
              {{ getHeadingLevel(para.id) }}
            </span>
          </div>
          <div class="paragraph-text">{{ para.text }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import OutlineNode from './OutlineNode.vue'

interface AnalysisResult {
  total_words_count: number
  paragraph_count: number
  paragraphs: Array<{
    id: number
    text: string
    word_count: number
  }>
  outline: Array<{
    id: number
    text: string
    level: number
    style: string
  }>
  outline_tree: Array<{
    id: number
    text: string
    level: number
    style: string
    children: any[]
  }>
}

const props = defineProps<{
  result: AnalysisResult
}>()

const headingIds = computed(() => {
  return new Set(props.result.outline?.map(item => item.id) || [])
})

const headingLevels = computed(() => {
  const levels: Record<number, string> = {}
  props.result.outline?.forEach(item => {
    levels[item.id] = item.style
  })
  return levels
})

const isHeading = (paragraphId: number) => {
  return headingIds.value.has(paragraphId)
}

const getHeadingLevel = (paragraphId: number) => {
  return headingLevels.value[paragraphId] || ''
}

const scrollToParagraph = (paragraphId: number) => {
  const element = document.getElementById(`paragraph-${paragraphId}`)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'center' })
    element.classList.add('highlight')
    setTimeout(() => {
      element.classList.remove('highlight')
    }, 2000)
  }
}

const downloadReport = () => {
  // TODO: 实现报告下载功能
  console.log('下载报告')
}
</script>

<style scoped>
.analysis-result {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.result-header h2 {
  margin: 0;
  color: #2c3e50;
}

.btn-download {
  background: #28a745;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-download:hover {
  background: #218838;
}

.stats-section, .outline-section, .paragraphs-section {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stats-section h3, .outline-section h3, .paragraphs-section h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  border-bottom: 2px solid #3498db;
  padding-bottom: 0.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #3498db;
}

.stat-label {
  color: #666;
  margin-top: 0.5rem;
}

.outline-tree {
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 1rem;
}

.paragraphs-list {
  max-height: 600px;
  overflow-y: auto;
}

.paragraph-item {
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 1rem;
  padding: 1rem;
  transition: all 0.3s ease;
}

.paragraph-item.is-heading {
  border-left: 4px solid #3498db;
  background: #f8f9fa;
}

.paragraph-item.highlight {
  border-color: #ffc107;
  background: #fff3cd;
  box-shadow: 0 0 10px rgba(255, 193, 7, 0.5);
}

.paragraph-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.paragraph-id {
  background: #6c757d;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
}

.word-count {
  color: #666;
}

.heading-badge {
  background: #3498db;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
}

.paragraph-text {
  line-height: 1.6;
  color: #333;
}

@media (max-width: 768px) {
  .analysis-result {
    padding: 1rem;
  }
  
  .result-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
