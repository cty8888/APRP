<template>
  <div class="outline-node" :style="{ marginLeft: `${node.level * 20}px` }">
    <div class="node-content" @click="$emit('nodeClick', node.id)">
      <span class="level-indicator">{{ getLevelIcon(node.level) }}</span>
      <span class="node-text">{{ node.text }}</span>
      <span class="node-style">{{ node.style }}</span>
    </div>
    
    <div v-if="node.children && node.children.length > 0" class="node-children">
      <OutlineNode 
        v-for="child in node.children" 
        :key="child.id" 
        :node="child"
        @nodeClick="$emit('nodeClick', $event)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
interface OutlineNode {
  id: number
  text: string
  level: number
  style: string
  children?: OutlineNode[]
}

defineProps<{
  node: OutlineNode
}>()

defineEmits<{
  nodeClick: [paragraphId: number]
}>()

const getLevelIcon = (level: number) => {
  const icons = ['📑', '📄', '📝', '📋', '📌', '📎']
  return icons[level] || '📄'
}
</script>

<style scoped>
.outline-node {
  margin-bottom: 0.5rem;
}

.node-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.node-content:hover {
  background: #f0f8ff;
}

.level-indicator {
  font-size: 1rem;
}

.node-text {
  flex: 1;
  color: #333;
  font-weight: 500;
}

.node-style {
  font-size: 0.8rem;
  color: #666;
  background: #e9ecef;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
}

.node-children {
  margin-left: 1rem;
  border-left: 2px solid #e9ecef;
  padding-left: 0.5rem;
}
</style>
