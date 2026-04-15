
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
        <div class="card p-8 text-center hover:shadow-xl transition-all group">
          <div class="text-4xl mb-4">📚</div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">Librerías</h3>
          <div class="text-3xl font-bold text-primary-600">{{ stats.libraries }}</div>
        </div>
        <div class="card p-8 text-center hover:shadow-xl transition-all group">
          <div class="text-4xl mb-4">🧠</div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">Flashcards</h3>
          <div class="text-3xl font-bold text-green-600">{{ stats.flashcards }}</div>
        </div>
        <div class="card p-8 text-center hover:shadow-xl transition-all group">
          <div class="text-4xl mb-4">📝</div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">Notas</h3>
          <div class="text-3xl font-bold text-purple-600">{{ stats.notes }}</div>
        </div>
        <div class="card p-8 text-center hover:shadow-xl transition-all group">
          <div class="text-4xl mb-4">❓</div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">Cuestionarios</h3>
          <div class="text-3xl font-bold text-orange-600">{{ stats.knowtionaries }}</div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Recent Items -->
        <div class="card">
          <h3 class="text-2xl font-bold text-gray-900 mb-6">Actividad reciente</h3>
          <div v-if="recentItems.length" class="space-y-4">
            <div 
              v-for="item in recentItems" 
              :key="item.id"
              class="p-6 border border-gray-100 rounded-2xl hover:shadow-md transition-all group cursor-pointer"
              @click="navigateToItem(item)"
            >
              <div class="flex items-start space-x-4">
                <div class="flex-shrink-0">
                  <div class="w-12 h-12 rounded-xl flex items-center justify-center text-xl font-bold" :class="item.iconBg">
                    {{ item.icon }}
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center space-x-2 mb-1">
                    <h4 class="font-semibold text-lg text-gray-900 truncate">{{ item.title }}</h4>
                    <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">
                      {{ item.type }}
                    </span>
                  </div>
                  <p v-if="item.subtitle" class="text-sm text-gray-600 mb-2 line-clamp-1">{{ item.subtitle }}</p>
                  <div class="flex items-center justify-between text-xs text-gray-500">
                    <span>{{ formatRelativeTime(item.created_at) }}</span>
                    <router-link :to="item.link" class="font-medium hover:text-primary-600">
                      Ver →
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-12">
            <div class="w-20 h-20 mx-auto mb-4 p-5 bg-gray-100 rounded-2xl flex items-center justify-center">
              <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13c1.668-1.523 3.254-1.477 4.5-1.477 1.246 0 2.5.177 2.5 2.5s-1.177 2.5-2.5 2.5-2.5-1.177-2.5-2.5S9.168 7.323 10.5 7.5c.832 0 1.246.477 1.5 1.5 3 3z"/>
              </svg>
            </div>
            <h4 class="text-lg font-semibold text-gray-900 mb-1">Sin actividad reciente</h4>
            <p class="text-gray-600 mb-4">Crea contenido para ver tu progreso aquí</p>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="card">
          <h3 class="text-2xl font-bold text-gray-900 mb-8">Acciones rápidas</h3>
          <div class="grid grid-cols-1 gap-4">
            <router-link to="/libraries" class="group flex items-center p-6 border-2 border-dashed border-gray-200 rounded-2xl hover:border-primary-200 hover:bg-primary-50 transition-all">
              <div class="p-3 bg-primary-100 rounded-xl mr-4 group-hover:bg-primary-200">
                <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-2" />
                </svg>
              </div>
              <div>
                <h4 class="text-xl font-semibold text-gray-900 group-hover:text-primary-600">Nueva Librería</h4>
                <p class="text-gray-600">Organiza tu estudio</p>
              </div>
            </router-link>
            <router-link to="/flowcards" class="group flex items-center p-6 border-2 border-dashed border-gray-200 rounded-2xl hover:border-green-200 hover:bg-green-50 transition-all">
              <div class="p-3 bg-green-100 rounded-xl mr-4 group-hover:bg-green-200">
                <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 5 7.5c1.323 0 2.5 1.177 2.5 2.5s1.177 2.5 2.5 2.5 2.5-1.177 2.5-2.5S9.168 7.323 10.5 7.5c.832 0 1.246.477 1.5 1.5 3 3z"/>
                </svg>
              </div>
              <div>
                <h4 class="text-xl font-semibold text-gray-900 group-hover:text-green-600">Nueva Flashcard</h4>
                <p class="text-gray-600">Aprende más eficientemente</p>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import DefaultLayout from '../layouts/DefaultLayout.vue'
import Button from '../components/Button.vue'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'
const libraryService = {
  getAll: () => api.get('/library/'),
  create: (data) => api.post('/library/create/', data)
}
const flowcardService = {
  getAll: () => api.get('/flashcards/'),
  create: (data) => api.post('/flashcards/add/', data)
}
const noteService = {
  getAll: () => api.get('/notes/')
}
const knowtionaryService = {
  getAll: () => api.get('/knowtionaries/')
}
const taskService = {
  getAll: () => api.get('/tasks/')
}
import type { Library, Flowcard, Note, Knowtionary, Task } from '../types'

const authStore = useAuthStore()
const router = useRouter()

interface RecentItem {
  id: number | string
  title: string
  subtitle?: string
  type: string
  icon: string
  iconBg: string
  link: string
  created_at: string
}

const stats = ref({
  libraries: 0,
  flashcards: 0,
  notes: 0,
  knowtionaries: 0
})

const recentItems = ref<RecentItem[]>([])

const loadStats = async () => {
  try {
    const [libs, cards, notes, quizzes, tasks] = await Promise.all([
      libraryService.getAll(),
      flowcardService.getAll(),
      noteService.getAll(),
      knowtionaryService.getAll(),
      taskService.getAll()
    ])
    
    stats.value = {
      libraries: libs.data?.length || 0,
      flashcards: cards.data?.length || 0,
      notes: notes.data?.length || 0,
      knowtionaries: quizzes.data?.length || 0
    }

    // Recent items from all lists, sorted by date
    const allItems = [
      ...libs.data.map((item: Library) => ({
        id: item.id,
        title: item.name,
        subtitle: item.description,
        type: 'Librería',
        icon: '📚',
        iconBg: 'bg-gradient-to-br from-purple-500 to-pink-500',
        link: `/libraries/${item.id}`,
        created_at: item.created_at || new Date().toISOString()
      })),
      ...cards.data.map((item: Flowcard) => ({
        id: item.slug,
        title: item.term,
        subtitle: item.definition.substring(0, 50) + '...',
        type: 'Flashcard',
        icon: '🧠',
        iconBg: 'bg-gradient-to-br from-blue-500 to-indigo-500',
        link: `/flowcards/${item.slug}`,
        created_at: item.created_at || new Date().toISOString()
      })),
      ...notes.data.map((item: Note) => ({
        id: item.slug,
        title: item.title,
        subtitle: item.content.substring(0, 50) + '...',
        type: 'Nota',
        icon: '📝',
        iconBg: 'bg-gradient-to-br from-indigo-500 to-purple-500',
        link: `/notes/${item.slug}`,
        created_at: item.created_at || new Date().toISOString()
      })),
      ...quizzes.data.map((item: Knowtionary) => ({
        id: item.id,
        title: item.title,
        type: 'Cuestionario',
        icon: '❓',
        iconBg: 'bg-gradient-to-br from-orange-500 to-red-500',
        link: `/knowtionaries/${item.id}`,
        created_at: item.created_at || new Date().toISOString()
      })),
      ...tasks.data.map((item: Task) => ({
        id: item.id,
        title: item.title,
        subtitle: item.description,
        type: item.completed ? 'Tarea ✓' : 'Tarea',
        icon: item.completed ? '✅' : '⭕',
        iconBg: item.completed ? 'bg-green-500' : 'bg-gradient-to-br from-yellow-500 to-orange-500',
        link: '/tasks',
        created_at: item.created_at || new Date().toISOString()
      }))
    ]

    // Sort by date desc, take last 8
    recentItems.value = allItems
      .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
      .slice(0, 8)

  } catch (error) {
    console.error('Error loading dashboard data:', error)
  }
}

const navigateToItem = (item: RecentItem) => {
  router.push(item.link)
}

const formatRelativeTime = (dateString: string) => {
  const now = new Date()
  const date = new Date(dateString)
  const diffMs = now.getTime() - date.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'Ahora'
  if (diffMins < 60) return `${diffMins}m atrás`
  if (diffHours < 24) return `${diffHours}h atrás`
  if (diffDays < 7) return `${diffDays}d atrás`
  return date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric' })
}

onMounted(() => {
  authStore.checkAuth()
  loadStats()
})
</script>

<style scoped>
.card {
  @apply bg-white/80 backdrop-blur-sm shadow-lg rounded-2xl p-8 border border-white/20 hover:shadow-2xl hover:-translate-y-1 transition-all duration-300;
}

.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

