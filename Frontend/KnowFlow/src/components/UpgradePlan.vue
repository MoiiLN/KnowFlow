<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
  >
    <div class="bg-white dark:bg-slate-900 rounded-2xl shadow-2xl p-8 max-w-md w-full mx-4">
      <h2 class="text-2xl font-bold mb-4 text-slate-900 dark:text-white">
        Límite alcanzado
      </h2>

      <p class="text-slate-600 dark:text-slate-300 mb-6">
        {{ message }}
      </p>

      <div class="space-y-2 mb-6 text-sm text-slate-700 dark:text-slate-300">
        <p>✔ Más flashcards</p>
        <p>✔ Más notes</p>
        <p>✔ Más tasks</p>
        <p>✔ Knowtionaries ilimitados</p>
      </div>

      <div class="flex gap-3">
        <button
          @click="closeModal"
          class="flex-1 border border-slate-300 dark:border-slate-700 rounded-xl py-2"
        >
          Más tarde
        </button>

        <router-link
          to="/pricing"
          class="flex-1 bg-blue-600 hover:bg-blue-700 text-white rounded-xl py-2 text-center"
          @click="closeModal"
        >
          Mejorar plan
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const show = ref(false)
const message = ref('Has alcanzado el límite de tu plan gratuito.')

const openModal = (event: Event) => {
  const customEvent = event as CustomEvent
  message.value = customEvent.detail || message.value
  show.value = true
}

const closeModal = () => {
  show.value = false
}

onMounted(() => {
  window.addEventListener('subscription-limit', openModal)
})

onUnmounted(() => {
  window.removeEventListener('subscription-limit', openModal)
})
</script>