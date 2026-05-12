<template>
  <DefaultLayout>
    <div class="min-h-screen flex items-center justify-center py-12 px-4 bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-slate-950 dark:to-slate-900 transition-colors duration-500">
      <div class="w-full max-w-2xl mx-auto">
        <!-- Header -->
        <div class="flex items-center justify-between mb-8">
          <router-link to="/flowcards" class="flex items-center space-x-2 text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-200 transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            <span class="font-bold">Volver a Flashcards</span>
          </router-link>
          <div class="text-right">
            <span class="text-sm text-gray-500 dark:text-gray-400 font-medium">Card {{ currentIndex + 1 }} / {{ cards.length }}</span>
          </div>
        </div>

        <!-- Card Container -->
        <div class="relative">
          <div class="w-full h-96 rounded-[3rem] shadow-2xl overflow-hidden cursor-pointer relative group" @click="showDefinition = !showDefinition">
            <!-- Pulse glow effect -->
            <div class="absolute inset-0 rounded-[3rem] bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-500 opacity-0 group-hover:opacity-40 transition-all duration-300 blur-2xl scale-110 -z-10"></div>
            
            <!-- Concept side -->
            <div v-if="!showDefinition" class="h-full bg-gradient-to-br from-emerald-500 to-teal-600 dark:from-emerald-600 dark:to-teal-800 flex flex-col items-center justify-center text-white p-8 text-center transition-all duration-500 group-hover:scale-[1.02]">
              <div class="w-24 h-24 bg-white/20 backdrop-blur-md rounded-3xl flex items-center justify-center mb-8 group-hover:scale-110 transition-transform duration-300 shadow-xl">
                <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 5 7.5c1.323 0 2.5 1.177 2.5 2.5s1.177 2.5 2.5 2.5 2.5-1.177 2.5-2.5S9.168 7.323 10.5 7.5c0.832 0 1.246.477 1.5 1.5 3 3z" />
                </svg>
              </div>
              <h2 class="text-5xl font-black mb-4 drop-shadow-xl tracking-tight">{{ currentCard?.term }}</h2>
              <p class="text-xl font-medium opacity-80 uppercase tracking-widest text-sm">Toca para ver definición</p>
            </div>
            
            <!-- Definition side -->
            <div v-else class="h-full bg-white dark:bg-slate-900 flex flex-col items-center justify-center p-8 text-center transition-all duration-500 group-hover:scale-[1.02] border border-gray-100 dark:border-slate-800">
              <div class="w-20 h-20 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-2xl flex items-center justify-center mb-8 shadow-xl group-hover:scale-110 transition-transform duration-300">
                <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="max-w-lg">
                <h3 class="text-sm font-black text-emerald-500 dark:text-emerald-400 uppercase tracking-widest mb-4">Definición</h3>
                <p class="text-2xl font-bold text-gray-900 dark:text-white leading-relaxed">{{ currentCard?.definition }}</p>
              </div>
            </div>
          </div>

          <!-- Navigation -->
          <div class="flex justify-center gap-6 mt-16">
            <button @click="prevCard" :disabled="currentIndex === 0" class="px-10 py-4 bg-white dark:bg-slate-800 text-gray-700 dark:text-gray-200 rounded-2xl font-black hover:bg-gray-50 dark:hover:bg-slate-700 transition-all shadow-xl hover:shadow-2xl flex items-center space-x-3 disabled:opacity-30 disabled:cursor-not-allowed border border-gray-100 dark:border-slate-700 uppercase tracking-widest text-xs">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
              <span>Anterior</span>
            </button>
            <button @click="nextCard" :disabled="currentIndex === cards.length - 1" class="px-10 py-4 bg-gradient-to-r from-emerald-500 to-teal-600 text-white rounded-2xl font-black shadow-xl hover:shadow-emerald-500/40 transition-all hover:scale-105 flex items-center space-x-3 disabled:opacity-30 disabled:cursor-not-allowed uppercase tracking-widest text-xs">
              <span>Siguiente</span>
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import api from '@/services/api'

const route = useRoute()
const cards = ref([])
const currentIndex = ref(0)
const showDefinition = ref(false)

const currentCard = computed(() => cards.value[currentIndex.value])

onMounted(async () => {
  await loadCards()
})

const loadCards = async () => {
  try {
    const response = await api.get('flowcards/')
    cards.value = response.data || []
    if (cards.value.length === 0) {
      cards.value = [{ term: 'Sin flashcards', definition: 'Crea flashcards desde /flowcards' }]
    }
  } catch (error) {
    console.error('Error loading cards:', error)
    cards.value = [{ term: 'Error', definition: 'No se pudieron cargar las flashcards' }]
  }
}

const prevCard = () => {
  showDefinition.value = false
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

const nextCard = () => {
  showDefinition.value = false
  if (currentIndex.value < cards.value.length - 1) {
    currentIndex.value++
  }
}
</script>

<style scoped></style>

