<template>
  <div v-if="message" :class="['alert', `alert-${type}`]">
    {{ message }}
  </div>
</template>

<script setup lang="ts">
interface Props {
  message?: string
  type?: 'success' | 'error' | 'warning' | 'info'
}

withDefaults(defineProps<Props>(), {
  type: 'info'
})
</script>
