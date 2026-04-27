<template>
  <DefaultLayout>
    <div class="min-h-screen flex items-center justify-center py-12 px-4 bg-gradient-to-br from-emerald-50 to-teal-50">
      <div class="w-full max-w-2xl mx-auto">
        <!-- Header -->
        <div class="flex items-center justify-between mb-8">
          <router-link to="/flowcards" class="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            <span>Volver a Flashcards</span>
          </router-link>
          <div class="text-right">
            <span class="text-sm text-gray-500">Card {{ currentIndex + 1 }} / {{ cards.length }}</span>
          </div>
        </div>

        <!-- Card Container -->
        <div class="relative">
          <div class="w-full h-96 rounded-3xl shadow-2xl overflow-hidden cursor-pointer relative group" @click="showDefinition = !showDefinition">
            <!-- Pulse glow effect -->
            <div class="absolute inset-0 rounded-3xl bg-gradient-to-r from-emerald-400 via-teal-400 to-emerald-500 opacity-0 group-hover:opacity-100 transition-all duration-200 blur-xl scale-110 -z-10"></div>
            
            <!-- Concept side -->
            <div v-if="!showDefinition" class="h-full bg-gradient-to-b from-emerald-500 to-teal-500 flex flex-col items-center justify-center text-white p-8 text-center transition-all duration-500 group-hover:scale-105 hover:shadow-3xl">
              <div class="w-20 h-20 bg-white/20 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-200">
                <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 5 7.5c1.323 0 2.5 1.177 2.5 2.5s1.177 2.5 2.5 2.5 2.5-1.177 2.5-2.5S9.168 7.323 10.5 7.5c0.832 0 1.246.477 1.5 1.5 3 3z" />
                </svg>
              </div>
              <h2 class="text-4xl font-black mb-4 drop-shadow-lg leading-tight group-hover:scale-105 transition-transform duration-200">{{ currentCard?.term }}</h2>
              <p class="text-xl opacity-90 drop-shadow-md leading-relaxed max-w-md transition-all duration-200">Toca para ver definición</p>
            </div>
            
            <!-- Definition side -->
            <div v-else class="h-full bg-gradient-to-b from-white to-gray-50 flex flex-col items-center justify-center p-8 text-center transition-all duration-500 group-hover:scale-105 hover:shadow-3xl">
              <div class="w-20 h-20 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-2xl flex items-center justify-center mb-6 shadow-xl group-hover:scale-110 transition-transform duration-200">
                <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="mb-8 p-6 bg-emerald-50 rounded-2xl border border-emerald-200 hover:shadow-2xl transition-shadow duration-200 max-w-lg">
                <h2 class="text-2xl font-black text-gray-900 mb-4">Definición</h2>
                <p class="text-lg text-gray-800 leading-relaxed">{{ currentCard?.definition }}</p>
              </div>
            </div>
          </div>

          <!-- Navigation -->
          <div class="flex justify-center gap-4 mt-12">
            <button @click="prevCard" :disabled="currentIndex === 0" class="px-8 py-3 bg-gray-200 text-gray-800 rounded-2xl font-semibold hover:bg-gray-300 transition-all shadow-lg hover:shadow-xl flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
              </svg>
              <span>Anterior</span>
            </button>
            <button @click="nextCard" :disabled="currentIndex === cards.length - 1" class="px-8 py-3 bg-gradient-to-r from-emerald-500 to-teal-500 text-white rounded-2xl font-semibold hover:shadow-2xl transition-all shadow-xl hover:shadow-2xl flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed">
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

