<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div class="mb-12">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
          <div>
            <h1 class="text-5xl md:text-6xl font-black bg-gradient-to-r from-gray-900 to-gray-700 dark:from-white dark:to-gray-400 bg-clip-text text-transparent mb-3 tracking-tight transition-colors duration-300">
              Bienvenido, {{ authStore.user?.username || 'Estudiante' }}
            </h1>
            <p class="text-xl text-gray-500 dark:text-gray-400 font-medium transition-colors duration-300">
              Tu centro de operaciones intelectuales
            </p>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
        <div
          v-for="stat in statCards"
          :key="stat.label"
          class="bg-white dark:bg-gray-800 shadow-sm rounded-[2.5rem] p-10 border border-gray-100 dark:border-gray-700 text-center hover:shadow-2xl hover:-translate-y-2 transition-all group duration-500"
        >
          <div class="text-5xl mb-6 group-hover:scale-110 transition-transform duration-500">
            {{ stat.icon }}
          </div>
          <h3 class="text-xs font-black text-gray-400 dark:text-gray-500 mb-2 uppercase tracking-[0.2em]">
            {{ stat.label }}
          </h3>
          <div :class="`text-5xl font-black ${stat.color}`">
            {{ stat.value }}
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
        <div class="lg:col-span-2 bg-white dark:bg-gray-800 shadow-sm rounded-[3rem] p-10 border border-gray-100 dark:border-gray-700 transition-colors duration-300">
          <div class="flex items-center justify-between mb-10">
            <h3 class="text-2xl font-black text-gray-900 dark:text-white tracking-tight">
              Actividad Reciente
            </h3>
            <span class="text-[10px] font-black text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/40 px-4 py-2 rounded-full uppercase tracking-widest">
              En Vivo
            </span>
          </div>

          <div v-if="loadingActivity" class="space-y-6">
            <div
              v-for="i in 3"
              :key="i"
              class="h-24 bg-gray-50 dark:bg-gray-900/50 rounded-[2rem] animate-pulse"
            ></div>
          </div>

          <div v-else-if="recentActivity.length > 0" class="space-y-6">
            <div
              v-for="item in recentActivity"
              :key="item.uniqueId"
              class="group flex items-center p-6 bg-gray-50 dark:bg-gray-900/30 hover:bg-white dark:hover:bg-gray-700 rounded-[2rem] border border-transparent hover:border-gray-100 dark:hover:border-gray-600 hover:shadow-lg transition-all duration-300 cursor-pointer"
              @click="navigateTo(item)"
            >
              <div
                :class="`w-14 h-14 ${item.bgClass} dark:bg-opacity-20 rounded-2xl flex items-center justify-center text-2xl mr-6 shadow-sm group-hover:scale-110 transition-transform font-bold`"
              >
                {{ item.icon }}
              </div>

              <div class="flex-1">
                <div class="flex items-center justify-between mb-1">
                  <h4 class="font-black text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                    {{ item.title }}
                  </h4>
                  <span class="text-xs font-bold text-gray-400 dark:text-gray-500">
                    {{ timeAgo(item.date) }}
                  </span>
                </div>

                <p class="text-sm text-gray-500 dark:text-gray-400 font-medium line-clamp-1">
                  {{ item.description }}
                </p>
              </div>
            </div>
          </div>

          <div v-else class="flex flex-col items-center justify-center py-20 text-gray-400">
            <div class="w-24 h-24 bg-gray-50 dark:bg-gray-900 rounded-[2.5rem] flex items-center justify-center mb-6 shadow-inner">
              <span class="text-4xl opacity-20">🍃</span>
            </div>
            <p class="font-black text-gray-400">Sin actividad reciente</p>
          </div>
        </div>

        <div class="space-y-8">
          <div class="bg-white dark:bg-gray-800 shadow-sm rounded-[3rem] p-10 border border-gray-100 dark:border-gray-700 transition-colors duration-300">
            <div class="flex items-center justify-between mb-10">
              <h3 class="text-xl font-black text-gray-900 dark:text-white tracking-tight">
                Tu Plan
              </h3>

              <span
                :class="subscriptionStore.usage?.subscription_plan === 'premium'
                  ? 'bg-green-100 text-green-600 dark:bg-green-900/20 dark:text-green-400'
                  : 'bg-blue-100 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400'"
                class="px-4 py-2 rounded-full text-[10px] font-black uppercase tracking-widest"
              >
                {{ subscriptionStore.usage?.subscription_plan === 'premium' ? 'Pro' : 'Knower' }}
              </span>
            </div>

            <div class="flex flex-col items-center justify-center">
              <p class="text-sm text-gray-500 dark:text-gray-400 font-medium text-center mb-8 leading-relaxed">
                Desbloquea funciones ilimitadas y acceso premium completo.
              </p>

              <router-link
                to="/pricing"
                class="block w-full"
              >
                <button
                  class="w-full bg-blue-600 hover:bg-blue-700 text-white py-5 rounded-2xl font-black text-sm uppercase tracking-widest transition-all active:scale-95 shadow-lg shadow-blue-500/20"
                >
                  Mejorar Plan
                </button>
              </router-link>
            </div>
          </div>

          <div class="bg-white dark:bg-gray-800 shadow-sm rounded-[3rem] p-10 border border-gray-100 dark:border-gray-700 transition-colors duration-300">
            <h3 class="text-xl font-black text-gray-900 dark:text-white mb-8 tracking-tight">
              Acceso Rápido
            </h3>

            <div class="grid grid-cols-1 gap-4">
              <router-link to="/timerflow" class="group flex items-center p-5 bg-orange-50 dark:bg-orange-900/20 text-orange-700 dark:text-orange-300 rounded-[1.5rem] font-black hover:bg-orange-100 transition-all active:scale-95 border border-orange-100/50 dark:border-orange-800/50">
                <div class="w-12 h-12 bg-white dark:bg-gray-800 rounded-xl flex items-center justify-center text-2xl mr-4 shadow-sm">
                  ⏱️
                </div>
                TimerFlow
              </router-link>

              <router-link to="/libraries" class="group flex items-center p-5 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 rounded-[1.5rem] font-black hover:bg-blue-100 transition-all active:scale-95 border border-blue-100/50 dark:border-blue-800/50">
                <div class="w-12 h-12 bg-white dark:bg-gray-800 rounded-xl flex items-center justify-center text-2xl mr-4 shadow-sm">
                  📁
                </div>
                Librerías
              </router-link>

              <router-link to="/flowcards" class="group flex items-center p-5 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300 rounded-[1.5rem] font-black hover:bg-emerald-100 transition-all active:scale-95 border border-emerald-100/50 dark:border-emerald-800/50">
                <div class="w-12 h-12 bg-white dark:bg-gray-800 rounded-xl flex items-center justify-center text-2xl mr-4 shadow-sm">
                  🎴
                </div>
                Flowcards
              </router-link>
            </div>
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
import { useSubscriptionStore } from '../stores/subscription'
import api from '../services/api'

const authStore = useAuthStore()
const subscriptionStore = useSubscriptionStore()
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
  { label: 'Knowtionaries', icon: '❓', value: stats.value.knowtionaries, color: 'text-orange-600' }
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

    stats.value = {
      libraries: Array.isArray(libs.data) ? libs.data.length : 0,
      flashcards: Array.isArray(cards.data) ? cards.data.length : 0,
      notes: Array.isArray(notes.data) ? notes.data.length : 0,
      knowtionaries: Array.isArray(quizzes.data) ? quizzes.data.length : 0
    }

    // Process Recent Activity
    const allItems: any[] = []

    if (Array.isArray(libs.data)) {
      libs.data.forEach((item: any) => {
        allItems.push({
          id: item.id,
          uniqueId: `lib-${item.id}`,
          type: 'library',
          title: item.name,
          description: `Librería con ${item.content_count || 0} elementos`,
          date: item.updated_at || item.created_at,
          icon: '📁',
          bgClass: 'bg-blue-100 text-blue-600'
        })
      })
    }

    if (Array.isArray(cards.data)) {
      cards.data.forEach((item: any) => {
        allItems.push({
          id: item.id,
          uniqueId: `card-${item.id}`,
          type: 'flashcard',
          title: item.term || item.name,
          description: 'Nueva flashcard creada',
          date: item.created_at,
          icon: '🎴',
          bgClass: 'bg-emerald-100 text-emerald-600'
        })
      })
    }

    if (Array.isArray(notes.data)) {
      notes.data.forEach((item: any) => {
        allItems.push({
          id: item.id,
          uniqueId: `note-${item.id}`,
          type: 'note',
          title: item.title,
          description: item.text ? item.text.substring(0, 50) + '...' : 'Nota sin contenido',
          date: item.updated_at || item.created_at,
          icon: '📝',
          bgClass: 'bg-purple-100 text-purple-600'
        })
      })
    }

    if (Array.isArray(quizzes.data)) {
      quizzes.data.forEach((item: any) => {
        allItems.push({
          id: item.id,
          uniqueId: `quiz-${item.id}`,
          type: 'knowtionary',
          title: item.name,
          description: `Cuestionario con ${item.words_count || 0} términos`,
          date: item.updated_at || item.created_at,
          icon: '❓',
          bgClass: 'bg-orange-100 text-orange-600'
        })
      })
    }

    // Sort by date (descending) and take top 5
    recentActivity.value = allItems
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

  await loadData()
  await subscriptionStore.fetchUsage()
})
</script>