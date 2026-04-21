<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-12">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
          <div>
            <h1 class="text-4xl md:text-5xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent mb-3">
              Bienvenido {{ authStore.user?.username || 'al estudiante' }}
            </h1>
            <p class="text-xl text-gray-600">Tu panel de control de estudios</p>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <div class="bg-white/80 backdrop-blur-sm shadow-lg rounded-2xl p-8 border border-gray-200 text-center hover:shadow-xl transition-all group">
          <div class="text-4xl mb-4">📚</div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">Librerías</h3>
          <div class="text-3xl font-bold text-primary-600">{{ stats.libraries }}</div>
        </div>

        <div class="bg-white/80 backdrop-blur-sm shadow-lg rounded-2xl p-8 border border-gray-200 text-center hover:shadow-xl transition-all group">
          <div class="text-4xl mb-4">🧠</div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">Flashcards</h3>
          <div class="text-3xl font-bold text-green-600">{{ stats.flashcards }}</div>
        </div>

        <div class="bg-white/80 backdrop-blur-sm shadow-lg rounded-2xl p-8 border border-gray-200 text-center hover:shadow-xl transition-all group">
          <div class="text-4xl mb-4">📝</div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">Notas</h3>
          <div class="text-3xl font-bold text-purple-600">{{ stats.notes }}</div>
        </div>

        <div class="bg-white/80 backdrop-blur-sm shadow-lg rounded-2xl p-8 border border-gray-200 text-center hover:shadow-xl transition-all group">
          <div class="text-4xl mb-4">❓</div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">Cuestionarios</h3>
          <div class="text-3xl font-bold text-orange-600">{{ stats.knowtionaries }}</div>
        </div>
      </div>

      <!-- Content -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">

        <!-- Activity -->
        <div class="bg-white/80 backdrop-blur-sm shadow-lg rounded-2xl p-8 border border-gray-200">
          <h3 class="text-2xl font-bold text-gray-900 mb-6">Actividad reciente</h3>

          <div v-if="recentItems.length" class="space-y-4">
            <div 
              v-for="item in recentItems" 
              :key="item.id"
              class="p-6 border border-gray-100 rounded-2xl hover:shadow-md transition-all cursor-pointer"
              @click="navigateToItem(item)"
            >
              {{ item.title }}
            </div>
          </div>

          <div v-else class="text-center py-12">
            <p class="text-gray-600">Sin actividad reciente</p>
          </div>
        </div>

        <!-- Actions -->
        <div class="bg-white/80 backdrop-blur-sm shadow-lg rounded-2xl p-8 border border-gray-200">
          <h3 class="text-2xl font-bold text-gray-900 mb-8">Acciones rápidas</h3>

          <router-link to="/libraries" class="block p-6 border-2 border-dashed border-gray-200 rounded-2xl hover:border-primary-200 hover:bg-primary-50 transition-all">
            Nueva Librería
          </router-link>
        </div>

      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import DefaultLayout from '../layouts/DefaultLayout.vue'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const authStore = useAuthStore()

const stats = ref({
  libraries: 0,
  flashcards: 0,
  notes: 0,
  knowtionaries: 0
})

const recentItems = ref([])

const loadStats = async () => {
  try {
    const [libs, cards, notes, quizzes] = await Promise.all([
      api.get('/library/'),
      api.get('/flashcards/'),
      api.get('/notes/'),
      api.get('/knowtionaries/')
    ])

    stats.value = {
      libraries: libs.data?.length || 0,
      flashcards: cards.data?.length || 0,
      notes: notes.data?.length || 0,
      knowtionaries: quizzes.data?.length || 0
    }

  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  authStore.checkAuth()
  loadStats()
})
</script>

<style scoped>
</style>