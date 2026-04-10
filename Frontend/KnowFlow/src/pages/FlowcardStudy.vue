<template>
  <DefaultLayout>
    <div class="max-w-2xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent mb-4">
          Modo Estudio
        </h1>
        <div class="flex items-center justify-center space-x-4 text-gray-600 mb-8">
          <span>Flashcard {{ currentIndex + 1 }} de {{ flowcards.length }}</span>
          <div class="flex items-center space-x-2">
            <svg class="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            <span>{{ correctCount }} / {{ flowcards.length }} correctas</span>
          </div>
        </div>
      </div>

      <!-- Progress Bar -->
      <div class="card mb-12 p-6">
        <div class="w-full bg-gray-200 rounded-full h-3">
          <div class="bg-gradient-to-r from-green-500 to-blue-500 h-3 rounded-full transition-all duration-1000" 
               :style="{ width: progress + '%' }"></div>
        </div>
        <div class="flex justify-between text-sm text-gray-600 mt-2">
          <span>{{ progress }}% completado</span>
          <span>{{ remainingCards }} restantes</span>
        </div>
      </div>

      <!-- Flashcard -->
      <div v-if="flowcards.length" class="card relative overflow-hidden group" :class="{ flipped: isFlipped }">
        <!-- Front -->
        <div class="absolute inset-0 p-12 text-center flex items-center justify-center bg-gradient-to-b from-blue-50 to-indigo-100 group-hover:from-blue-100 transition-all duration-500" v-show="!isFlipped">
          <div>
            <h2 class="text-2xl font-bold text-gray-900 mb-8 leading-tight">{{ currentCard.term }}</h2>
            <div class="flex items-center justify-center space-x-4">
              <button @click="previousCard" class="p-3 bg-white/50 hover:bg-white rounded-full shadow-lg transition-all hover:scale-110">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <button 
                @click="flipCard"
                class="px-8 py-4 bg-gradient-to-r from-primary-500 to-primary-600 text-white font-bold text-lg rounded-2xl shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 mx-4"
              >
                Mostrar Respuesta
              </button>
              <button @click="nextCard" class="p-3 bg-white/50 hover:bg-white rounded-full shadow-lg transition-all hover:scale-110">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Back -->
        <div class="absolute inset-0 p-12 text-center flex flex-col items-center justify-center bg-gradient-to-b from-purple-50 to-pink-100 transition-all duration-500" v-show="isFlipped">
          <div class="max-w-2xl">
            <div class="mb-8 p-6 bg-white/60 backdrop-blur-sm rounded-2xl shadow-lg">
              <h2 class="text-2xl font-bold text-gray-900 mb-4 leading-tight">{{ currentCard.definition }}</h2>
            </div>
            <div class="flex items-center space-x-4">
              <button 
                @click="markCorrect"
                class="px-8 py-4 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-bold text-lg rounded-2xl shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all"
              >
                ✅ Entendido
              </button>
              <button 
                @click="markIncorrect"
                class="px-8 py-4 bg-gradient-to-r from-orange-500 to-red-500 text-white font-bold text-lg rounded-2xl shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all"
              >
                ❌ Necesito repasar
              </button>
            </div>
          </div>
        </div>

        <!-- Controls overlay on back -->
        <div v-if="isFlipped" class="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-3">
          <button @click="previousCard" class="w-12 h-12 bg-white/80 hover:bg-white rounded-2xl shadow-lg transition-all hover:scale-105">
            <svg class="w-6 h-6 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <button @click="nextCard" class="w-12 h-12 bg-white/80 hover:bg-white rounded-2xl shadow-lg transition-all hover:scale-105">
            <svg class="w-6 h-6 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Results -->
      <div v-if="!flowcards.length" class="text-center py-24">
        <div class="w-32 h-32 bg-gradient-to-br from-green-400 to-blue-500 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-2xl">
          <svg class="w-16 h-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" stroke-miterlimit="10" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <h2 class="text-3xl font-bold text-gray-900 mb-4">¡Estudio completado!</h2>
        <p class="text-xl text-gray-600 mb-8">Has repasado todas las flashcards perfectamente.</p>
        <div class="stats grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 max-w-md mx-auto">
          <div class="text-center p-6 bg-white rounded-2xl shadow-lg">
            <div class="text-3xl font-bold text-green-600">{{ correctCount }}</div>
            <div class="text-gray-600">Correctas</div>
          </div>
          <div class="text-center p-6 bg-white rounded-2xl shadow-lg">
            <div class="text-3xl font-bold text-orange-600">{{ incorrectCount }}</div>
            <div class="text-gray-600">Para repasar</div>
          </div>
          <div class="text-center p-6 bg-white rounded-2xl shadow-lg">
            <div class="text-3xl font-bold text-gray-900">{{ accuracy }}%</div>
            <div class="text-gray-600">Precisión</div>
          </div>
        </div>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <Button @click="restart" class="px-8">Repetir</Button>
          <router-link to="/flowcards" class="px-8 btn-secondary">Volver al listado</router-link>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { flowcardService } from '@/services/api'
import type { Flowcard } from '@/types/index'

const route = useRoute()
const flowcards = ref<Flowcard[]>([])
const currentIndex = ref(0)
const isFlipped = ref(false)
const correctAnswers = ref(new Set<number>())
const incorrectAnswers = ref(new Set<number>())

const currentCard = computed(() => flowcards.value[currentIndex.value] || null)

const progress = computed(() => {
  return Math.round((currentIndex.value / flowcards.value.length) * 100)
})

const remainingCards = computed(() => flowcards.value.length - currentIndex.value)

const correctCount = computed(() => correctAnswers.value.size)
const incorrectCount = computed(() => incorrectAnswers.value.size)
const accuracy = computed(() => flowcards.value.length ? Math.round((correctCount.value / flowcards.value.length) * 100) : 0)

const loadFlowcards = async () => {
  try {
    const slug = route.params.slug as string
    const response = await flowcardService.getBySlug(slug)
    flowcards.value = response.data // Assume single card or collection
    // Shuffle for study mode
    flowcards.value = shuffleArray(flowcards.value)
  } catch (error) {
    console.error('Error loading flowcards:', error)
  }
}

const flipCard = () => {
  isFlipped.value = !isFlipped.value
}

const nextCard = () => {
  if (currentIndex.value < flowcards.value.length - 1) {
    currentIndex.value++
    isFlipped.value = false
  }
}

const previousCard = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
    isFlipped.value = false
  }
}

const markCorrect = () => {
  correctAnswers.value.add(currentIndex.value)
  nextCard()
}

const markIncorrect = () => {
  incorrectAnswers.value.add(currentIndex.value)
  nextCard()
}

const restart = () => {
  currentIndex.value = 0
  isFlipped.value = false
  correctAnswers.value.clear()
  incorrectAnswers.value.clear()
}

const shuffleArray = <T>(array: T[]): T[] => {
  const shuffled = [...array]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }
  return shuffled
}

onMounted(loadFlowcards)
</script>

<style scoped>
.flipped {
  transform: rotateY(180deg);
}

.card {
  perspective: 1000px;
}
</style>
