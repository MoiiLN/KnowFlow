<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent mb-2">
          Bienvenido de vuelta
        </h1>
        <p class="text-xl text-gray-600">Tu espacio de estudio interactivo</p>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <div class="card p-8 text-center hover:shadow-xl transition-all">
          <div class="text-4xl mb-3">📚</div>
          <h3 class="text-2xl font-bold text-gray-900 mb-1">Librerías</h3>
          <div class="text-3xl font-bold text-primary-600">{{ librariesCount }}</div>
        </div>
        <div class="card p-8 text-center hover:shadow-xl transition-all">
          <div class="text-4xl mb-3">🧠</div>
          <h3 class="text-2xl font-bold text-gray-900 mb-1">Flashcards</h3>
          <div class="text-3xl font-bold text-green-600">{{ flowcardsCount }}</div>
        </div>
        <div class="card p-8 text-center hover:shadow-xl transition-all">
          <div class="text-4xl mb-3">📝</div>
          <h3 class="text-2xl font-bold text-gray-900 mb-1">Notas</h3>
          <div class="text-3xl font-bold text-purple-600">{{ notesCount }}</div>
        </div>
        <div class="card p-8 text-center hover:shadow-xl transition-all">
          <div class="text-4xl mb-3">❓</div>
          <h3 class="text-2xl font-bold text-gray-900 mb-1">Cuestionarios</h3>
          <div class="text-3xl font-bold text-orange-600">{{ knowtionariesCount }}</div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="card p-8">
          <h3 class="text-2xl font-bold text-gray-900 mb-6">Acciones rápidas</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <router-link 
              to="/libraries" 
              class="group flex items-center p-6 border-2 border-dashed border-gray-200 rounded-2xl hover:border-primary-300 hover:bg-primary-50 transition-all hover:shadow-lg"
            >
              <div class="p-3 bg-primary-100 rounded-xl group-hover:bg-primary-200 transition-colors mr-4">
                <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </div>
              <div>
                <h4 class="font-semibold text-xl text-gray-900 group-hover:text-primary-600">Nueva Librería</h4>
                <p class="text-gray-600">Organiza tu contenido</p>
              </div>
            </router-link>

            <router-link 
              to="/flowcards" 
              class="group flex items-center p-6 border-2 border-dashed border-gray-200 rounded-2xl hover:border-green-300 hover:bg-green-50 transition-all hover:shadow-lg"
            >
              <div class="p-3 bg-green-100 rounded-xl group-hover:bg-green-200 transition-colors mr-4">
                <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477. .5 7.5c1.323 0 2.5 1.177 2.5 2.5s1.177 2.5 2.5 2.5 2.5-1.177 2.5-2.5S9.168 7.323 10.5 7.5c. .832 0 1. .246 1.477 1.5 1.5 3 3z" />
                </svg>
              </div>
              <div>
                <h4 class="font-semibold text-xl text-gray-900 group-hover:text-green-600">Nueva Flashcard</h4>
                <p class="text-gray-600">Aprende con repetición espaciada</p>
              </div>
            </router-link>
          </div>
        </div>

        <div class="card p-8">
          <h3 class="text-2xl font-bold text-gray-900 mb-6">Tareas pendientes</h3>
          <div v-if="pendingTasks.length" class="space-y-3">
            <div 
              v-for="task in pendingTasks.slice(0,3)" 
              :key="task.id"
              class="flex items-center p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors"
            >
              <div class="flex-shrink-0 w-5 h-5 bg-gray-300 rounded-full mr-3"></div>
              <div class="flex-1 min-w-0">
                <p class="font-medium text-gray-900 truncate">{{ task.title }}</p>
                <p class="text-sm text-gray-500 truncate">{{ task.description }}</p>
              </div>
              <router-link :to="'/tasks'" class="text-sm font-medium text-primary-600 hover:text-primary-700">
                Ver todas →
              </router-link>
            </div>
          </div>
          <div v-else class="text-center py-12">
            <div class="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <h4 class="text-lg font-semibold text-gray-900 mb-1">¡Sin tareas pendientes!</h4>
            <p class="text-gray-600 mb-4">Estás al día con tus estudios</p>
            <router-link to="/tasks" class="btn-primary px-6 py-2.5">Añadir tarea</router-link>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { ref, onMounted } from 'vue'
import { libraryService, flowcardService, noteService, knowtionaryService, taskService } from '@/services/api'

interface DashboardStats {
  librariesCount: number
  flowcardsCount: number
  notesCount: number
  knowtionariesCount: number
  pendingTasks: Array<{ id: number; title: string; description?: string }>
}

const stats = ref<DashboardStats>({
  librariesCount: 0,
  flowcardsCount: 0,
  notesCount: 0,
  knowtionariesCount: 0,
  pendingTasks: []
})

const loadDashboardData = async () => {
  try {
    const [libs, cards, notes, quizzes, tasks] = await Promise.all([
      libraryService.getAll(),
      flowcardService.getAll(),
      noteService.getAll(),
      knowtionaryService.getAll(),
      taskService.getAll()
    ])
    
    stats.value = {
      librariesCount: libs.data.length,
      flowcardsCount: cards.data.length,
      notesCount: notes.data.length,
      knowtionariesCount: quizzes.data.length,
      pendingTasks: tasks.data.filter((t: any) => !t.completed).slice(0, 3)
    }
  } catch (error) {
    console.error('Error loading dashboard:', error)
  }
}

onMounted(loadDashboardData)
</script>

<style scoped>
.card {
  @apply bg-white/80 backdrop-blur-sm shadow-lg rounded-2xl border border-white/20 hover:shadow-2xl transition-all duration-300;
}

.btn-primary {
  @apply inline-flex items-center px-6 py-2.5 text-sm font-medium text-white bg-gradient-to-r from-primary-600 to-primary-700 rounded-xl hover:from-primary-700 hover:to-primary-800 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all duration-200;
}
</style>
