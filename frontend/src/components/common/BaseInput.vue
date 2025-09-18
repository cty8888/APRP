<template>
  <div class="form-group">
    <label v-if="label" :for="id" class="form-label">{{ label }}</label>
    <input
      :id="id"
      :type="type"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      :value="modelValue"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      class="form-input"
    />
  </div>
</template>

<script setup lang="ts">
interface Props {
  id?: string
  label?: string
  type?: string
  placeholder?: string
  required?: boolean
  disabled?: boolean
  modelValue?: string
}

withDefaults(defineProps<Props>(), {
  type: 'text',
  required: false,
  disabled: false
})

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>
