<template>
  <div class="page-layout">
    <div :class="narrow ? 'container-narrow' : 'container'">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
// 页面布局组件
interface Props {
  narrow?: boolean
}

defineProps<Props>()
</script>
