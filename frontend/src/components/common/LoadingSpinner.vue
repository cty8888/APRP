<template>
  <div class="loading-spinner" v-if="show">
    <div class="spinner"></div>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  show?: boolean
  message?: string
}

withDefaults(defineProps<Props>(), {
  show: true
})
</script>
