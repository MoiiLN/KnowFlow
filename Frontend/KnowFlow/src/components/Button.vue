<template>
  <button
    class="inline-flex items-center justify-center px-6 py-3 font-medium text-base rounded-xl shadow-sm transition-all duration-200 hover:shadow-md hover:-translate-y-0.5 active:translate-y-0 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none border font-medium"
    :class="computedClasses"
    :disabled="loading || disabled"
    @click="$emit('click', $event)"
  >
    <span v-if="loading" class="flex items-center space-x-2">
      <svg class="animate-spin -ml-1 h-4 w-4" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12c0-3.042 1.135-5.824 3 5.291z" />
      </svg>
      <span>{{ loadingText || 'Cargando...' }}</span>
    </span>
    <slot v-else />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String as () => 'primary' | 'secondary' | 'danger' | 'outline',
    default: 'primary'
  },
  size: {
    type: String as () => 'sm' | 'md' | 'lg',
    default: 'md'
  },
  loading: Boolean,
  disabled: Boolean,
  loadingText: String
})

const emit = defineEmits<{
  (e: 'click', event: MouseEvent): void
}>()

const computedClasses = computed(() => {
  const variants: Record<string, string> = {
    primary: 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white border-transparent shadow-lg hover:shadow-xl',
    secondary: 'bg-white hover:bg-gray-50 text-gray-900 border-gray-300 shadow-sm hover:shadow-md focus:ring-purple-500',
    danger: 'bg-red-600 hover:bg-red-700 text-white border-transparent shadow-lg hover:shadow-xl',
    outline: 'bg-transparent hover:bg-gray-50 text-gray-900 border-gray-300 focus:ring-purple-500 shadow-sm'
  }

  const sizes: Record<string, string> = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3',
    lg: 'px-8 py-3.5 text-lg'
  }

  return `${variants[props.variant]} ${sizes[props.size]}`
})
</script>
