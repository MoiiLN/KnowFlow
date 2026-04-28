<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-12">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
          <div>
            <h1 class="text-4xl md:text-5xl font-black bg-gradient-to-r from-gray-900 to-gray-700 dark:from-white dark:to-gray-300 bg-clip-text text-transparent mb-3 tracking-tight transition-colors duration-300">
              Bienvenido, {{ authStore.user?.username || 'Estudiante' }}
            </h1>
            <p class="text-xl text-gray-500 dark:text-gray-400 font-medium transition-colors duration-300">Tu panel de control de estudios inteligente</p>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
        <div v-for="stat in statCards" :key="stat.label" class="bg-white dark:bg-gray-800 shadow-sm rounded-[2rem] p-10 border border-gray-100 dark:border-gray-700 text-center hover:shadow-2xl hover:-translate-y-2 transition-all group duration-500">
          <div class="text-5xl mb-6 group-hover:scale-110 transition-transform duration-500">{{ stat.icon }}</div>
          <h3 class="text-sm font-black text-gray-400 dark:text-gray-500 mb-2 uppercase tracking-[0.2em]">{{ stat.label }}</h3>
          <div :class="`text-5xl font-black ${stat.color}`">{{ stat.value }}</div>
        </div>
      </div>

      <!-- Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
        <!-- Recent Activity -->
        <div class="lg:col-span-2 bg-white dark:bg-gray-800 shadow-sm rounded-[2.5rem] p-10 border border-gray-100 dark:border-gray-700 transition-colors duration-300">
          <div class="flex items-center justify-between mb-10">
            <h3 class="text-2xl font-black text-gray-900 dark:text-white tracking-tight">Actividad Reciente</h3>
            <span class="text-xs font-black text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/40 px-4 py-2 rounded-full uppercase tracking-widest">EN VIVO</span>
          </div>

          <div v-if="loadingActivity" class="space-y-6">
            <div v-for="i in 3" :key="i" class="h-24 bg-gray-50 dark:bg-gray-900/50 rounded-3xl animate-pulse"></div>
          </div>

          <div v-else-if="recentActivity.length > 0" class="space-y-6">
            <div 
              v-for="item in recentActivity" 
              :key="item.uniqueId"
              class="group flex items-center p-6 bg-gray-50 dark:bg-gray-900/30 hover:bg-white dark:hover:bg-gray-700 rounded-3xl border border-transparent hover:border-gray-100 dark:hover:border-gray-600 hover:shadow-xl transition-all duration-300 cursor-pointer"
              @click="navigateTo(item)"
            >
              <div :class="`w-14 h-14 ${item.bgClass} dark:bg-opacity-20 rounded-2xl flex items-center justify-center text-2xl mr-6 shadow-sm group-hover:scale-110 transition-transform font-bold`">
                {{ item.icon }}
              </div>
              <div class="flex-1">
                <div class="flex items-center justify-between mb-1">
                  <h4 class="font-black text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">{{ item.title }}</h4>
                  <span class="text-xs font-bold text-gray-400 dark:text-gray-500">{{ timeAgo(item.date) }}</span>
                </div>
                <p class="text-sm text-gray-500 dark:text-gray-400 font-medium line-clamp-1">{{ item.description }}</p>
              </div>
              <div class="ml-4 opacity-0 group-hover:opacity-100 transition-opacity">
                <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </div>

          <div v-else class="flex flex-col items-center justify-center py-20 text-gray-400">
            <div class="w-24 h-24 bg-gray-50 dark:bg-gray-900 rounded-[2rem] flex items-center justify-center mb-6 shadow-inner">
               <svg class="w-12 h-12 opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p class="font-bold">Aún no hay actividad reciente.</p>
            <p class="text-sm mt-1">¡Empieza creando contenido para verlo aquí!</p>
          </div>
        </div>

        <!-- Quick Actions & Recommendations -->
        <div class="space-y-8">
          <div class="bg-white dark:bg-gray-800 shadow-sm rounded-[2.5rem] p-10 border border-gray-100 dark:border-gray-700 transition-colors duration-300">
            <h3 class="text-2xl font-black text-gray-900 dark:text-white mb-10 tracking-tight">Acciones Rápidas</h3>
            <div class="grid grid-cols-1 gap-5">
              <router-link to="/libraries" class="group flex items-center p-6 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 rounded-2xl font-black hover:bg-blue-100 dark:hover:bg-blue-900/40 transition-all active:scale-95">
                <div class="w-12 h-12 bg-white dark:bg-gray-800 rounded-xl flex items-center justify-center text-2xl mr-4 shadow-sm group-hover:rotate-12 transition-transform">📁</div>
                Gestionar Librerías
              </router-link>
              <router-link to="/tasks" class="group flex items-center p-6 bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 rounded-2xl font-black hover:bg-purple-100 dark:hover:bg-purple-900/40 transition-all active:scale-95">
                <div class="w-12 h-12 bg-white dark:bg-gray-800 rounded-xl flex items-center justify-center text-2xl mr-4 shadow-sm group-hover:rotate-12 transition-transform">✅</div>
                Ver Mis Tareas
              </router-link>
              <router-link to="/flowcards" class="group flex items-center p-6 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300 rounded-2xl font-black hover:bg-emerald-100 dark:hover:bg-emerald-900/40 transition-all active:scale-95">
                <div class="w-12 h-12 bg-white dark:bg-gray-800 rounded-xl flex items-center justify-center text-2xl mr-4 shadow-sm group-hover:rotate-12 transition-transform">🎴</div>
                Crear Flashcard
              </router-link>
            </div>
          </div>

          <!-- Goal Summary (New) -->
          <div class="bg-gradient-to-br from-indigo-600 to-blue-700 rounded-[2.5rem] p-10 text-white shadow-xl shadow-blue-500/20 overflow-hidden relative">
            <div class="absolute top-0 right-0 -mt-8 -mr-8 w-32 h-32 bg-white/10 rounded-full blur-2xl"></div>
            <h4 class="text-xl font-black mb-4 relative z-10">Meta Diaria</h4>
            <div class="flex items-end gap-3 mb-6 relative z-10">
              <span class="text-5xl font-black leading-none">85%</span>
              <span class="text-blue-100 font-bold text-sm mb-1">COMPLETADO</span>
            </div>
            <div class="w-full bg-white/20 h-3 rounded-full overflow-hidden mb-6 relative z-10">
              <div class="bg-white h-full w-[85%]"></div>
            </div>
            <p class="text-blue-50 text-sm font-medium leading-relaxed relative z-10">¡Casi lo logras! Revisa 15 flashcards más para alcanzar tu objetivo de hoy.</p>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import DefaultLayout from '../layouts/DefaultLayout.vue'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const authStore = useAuthStore()
const router = useRouter()

const loadingActivity = ref(true)
const stats = ref({
  libraries: 0,
  flashcards: 0,
  notes: 0,
  knowtionaries: 0
})

const recentActivity = ref<any[]>([])

const statCards = computed(() => [
  { label: 'Librerías', icon: '📚', value: stats.value.libraries, color: 'text-blue-600' },
  { label: 'Flashcards', icon: '🧠', value: stats.value.flashcards, color: 'text-emerald-600' },
  { label: 'Notas', icon: '📝', value: stats.value.notes, color: 'text-purple-600' },
  { label: 'Cuestionarios', icon: '❓', value: stats.value.knowtionaries, color: 'text-orange-600' }
])

const timeAgo = (dateStr: string) => {
  if (!dateStr) return 'Reciente'
  const date = new Date(dateStr)
  const now = new Date()
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000)
  if (seconds < 60) return 'Ahora'
  if (seconds < 3600) return `Hace ${Math.floor(seconds / 60)}m`
  if (seconds < 86400) return `Hace ${Math.floor(seconds / 3600)}h`
  return `Hace ${Math.floor(seconds / 86400)}d`
}

const navigateTo = (item: any) => {
  if (item.type === 'library') router.push(`/libraries/${item.id}`)
  else if (item.type === 'flashcard') router.push('/flowcards')
  else if (item.type === 'note') router.push('/notes')
}

const loadData = async () => {
  loadingActivity.value = true
  try {
    const [libs, cards, notes, quizzes] = await Promise.all([
      api.get('libraries/'),
      api.get('flowcards/'),
      api.get('notes/'),
      api.get('knowtionaries/')
    ])

    // Update stats
    stats.value = {
      libraries: Array.isArray(libs.data) ? libs.data.length : 0,
      flashcards: Array.isArray(cards.data) ? cards.data.length : 0,
      notes: Array.isArray(notes.data) ? notes.data.length : 0,
      knowtionaries: Array.isArray(quizzes.data) ? quizzes.data.length : 0
    }

    // Process Recent Activity
    const activity: any[] = []
    
    if (Array.isArray(libs.data)) {
      libs.data.forEach((l: any) => {
        activity.push({
          uniqueId: `lib-${l.id}`,
          id: l.id,
          type: 'library',
          title: l.name,
          description: 'Librería creada',
          date: l.created_at,
          icon: '📁',
          bgClass: 'bg-blue-100 text-blue-600'
        })
      })
    }

    if (Array.isArray(cards.data)) {
      cards.data.forEach((c: any) => {
        activity.push({
          uniqueId: `card-${c.id}`,
          id: c.id,
          type: 'flashcard',
          title: c.term,
          description: 'Flashcard añadida',
          date: c.created_at,
          icon: '🎴',
          bgClass: 'bg-emerald-100 text-emerald-600'
        })
      })
    }

    if (Array.isArray(notes.data)) {
      notes.data.forEach((n: any) => {
        activity.push({
          uniqueId: `note-${n.id}`,
          id: n.id,
          type: 'note',
          title: n.title || 'Nueva Nota',
          description: 'Nota guardada',
          date: n.created_at,
          icon: '📄',
          bgClass: 'bg-purple-100 text-purple-600'
        })
      })
    }

    // Sort by date (descending) and take top 5
    recentActivity.value = activity
      .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
      .slice(0, 5)

  } catch (error) {
    console.error('Error loading dashboard data:', error)
  } finally {
    loadingActivity.value = false
  }
}

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    await authStore.checkAuth()
  }
  loadData()
})
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-in {
  animation: fade-in 0.4s ease-out forwards;
}
</style>