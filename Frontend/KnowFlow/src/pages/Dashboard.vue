<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-12">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
          <div>
            <h1 class="text-5xl md:text-6xl font-black bg-gradient-to-r from-gray-900 to-gray-700 dark:from-white dark:to-gray-400 bg-clip-text text-transparent mb-3 tracking-tight transition-colors duration-300">
              Bienvenido, {{ authStore.user?.username || 'Estudiante' }}
            </h1>
            <p class="text-xl text-gray-500 dark:text-gray-400 font-medium transition-colors duration-300">Tu centro de operaciones intelectuales</p>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
        <div v-for="stat in statCards" :key="stat.label" class="bg-white dark:bg-gray-800 shadow-sm rounded-[2.5rem] p-10 border border-gray-100 dark:border-gray-700 text-center hover:shadow-2xl hover:-translate-y-2 transition-all group duration-500">
          <div class="text-5xl mb-6 group-hover:scale-110 transition-transform duration-500">{{ stat.icon }}</div>
          <h3 class="text-xs font-black text-gray-400 dark:text-gray-500 mb-2 uppercase tracking-[0.2em]">{{ stat.label }}</h3>
          <div :class="`text-5xl font-black ${stat.color}`">{{ stat.value }}</div>
        </div>
      </div>

      <!-- Content -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-10">
        <!-- Recent Activity -->
        <div class="lg:col-span-2 bg-white dark:bg-gray-800 shadow-sm rounded-[3rem] p-10 border border-gray-100 dark:border-gray-700 transition-colors duration-300">
          <div class="flex items-center justify-between mb-10">
            <h3 class="text-2xl font-black text-gray-900 dark:text-white tracking-tight">Actividad Reciente</h3>
            <span class="text-[10px] font-black text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/40 px-4 py-2 rounded-full uppercase tracking-widest">En Vivo</span>
          </div>

          <div v-if="loadingActivity" class="space-y-6">
            <div v-for="i in 3" :key="i" class="h-24 bg-gray-50 dark:bg-gray-900/50 rounded-[2rem] animate-pulse"></div>
          </div>

          <div v-else-if="recentActivity.length > 0" class="space-y-6">
            <div 
              v-for="item in recentActivity" 
              :key="item.uniqueId"
              class="group flex items-center p-6 bg-gray-50 dark:bg-gray-900/30 hover:bg-white dark:hover:bg-gray-700 rounded-[2rem] border border-transparent hover:border-gray-100 dark:hover:border-gray-600 hover:shadow-lg transition-all duration-300 cursor-pointer"
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
            </div>
          </div>

          <div v-else class="flex flex-col items-center justify-center py-20 text-gray-400">
            <div class="w-24 h-24 bg-gray-50 dark:bg-gray-900 rounded-[2.5rem] flex items-center justify-center mb-6 shadow-inner">
                <span class="text-4xl opacity-20">🍃</span>
            </div>
            <p class="font-black text-gray-400">Sin actividad reciente</p>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-8">
          <!-- Quick Actions (NOW FIRST) -->
          <div class="bg-white dark:bg-gray-800 shadow-sm rounded-[3rem] p-10 border border-gray-100 dark:border-gray-700 transition-colors duration-300">
            <h3 class="text-xl font-black text-gray-900 dark:text-white mb-8 tracking-tight">Acceso Rápido</h3>
            <div class="grid grid-cols-1 gap-4">
              <router-link to="/timerflow" class="group flex items-center p-5 bg-orange-50 dark:bg-orange-900/20 text-orange-700 dark:text-orange-300 rounded-[1.5rem] font-black hover:bg-orange-100 transition-all active:scale-95 border border-orange-100/50 dark:border-orange-800/50">
                <div class="w-12 h-12 bg-white dark:bg-gray-800 rounded-xl flex items-center justify-center text-2xl mr-4 shadow-sm group-hover:rotate-12 transition-transform">⏱️</div>
                TimerFlow
              </router-link>
              <router-link to="/libraries" class="group flex items-center p-5 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 rounded-[1.5rem] font-black hover:bg-blue-100 transition-all active:scale-95 border border-blue-100/50 dark:border-blue-800/50">
                <div class="w-12 h-12 bg-white dark:bg-gray-800 rounded-xl flex items-center justify-center text-2xl mr-4 shadow-sm group-hover:rotate-12 transition-transform">📁</div>
                Librerías
              </router-link>
              <router-link to="/flowcards" class="group flex items-center p-5 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300 rounded-[1.5rem] font-black hover:bg-emerald-100 transition-all active:scale-95 border border-emerald-100/50 dark:border-emerald-800/50">
                <div class="w-12 h-12 bg-white dark:bg-gray-800 rounded-xl flex items-center justify-center text-2xl mr-4 shadow-sm group-hover:rotate-12 transition-transform">🎴</div>
                Flowcards
              </router-link>
            </div>
          </div>

          <!-- Wisdom Section (NOW SECOND and SMALLER) -->
          <div class="bg-gradient-to-br from-indigo-600 via-blue-700 to-indigo-800 rounded-[2.5rem] p-8 text-white shadow-xl shadow-blue-500/20 relative overflow-hidden group">
            <div class="absolute top-0 right-0 -mt-8 -mr-8 w-24 h-24 bg-white/10 rounded-full blur-2xl transition-transform duration-700 group-hover:scale-150"></div>

            <div class="relative z-10">
                <div class="flex items-center gap-2 mb-6">
                    <span class="p-1.5 bg-white/20 rounded-lg text-sm backdrop-blur-sm">
                        {{ currentWisdom.type === 'quote' ? '💡' : currentWisdom.type === 'ad' ? '🚀' : '🎓' }}
                    </span>
                    <h4 class="text-[9px] font-black uppercase tracking-[0.3em] text-blue-100">
                        {{ currentWisdom.type === 'quote' ? 'Motivación' : currentWisdom.type === 'ad' ? 'Descubre' : 'Técnica' }}
                    </h4>
                </div>

                <div class="min-h-[120px] flex flex-col justify-center">
                    <p class="text-lg font-black leading-snug mb-4 italic transition-all duration-500" :key="currentWisdom.text">
                        "{{ currentWisdom.text }}"
                    </p>
                    <p v-if="currentWisdom.author" class="text-[10px] font-bold text-blue-200/80">— {{ currentWisdom.author }}</p>
                    <p v-if="currentWisdom.tip || currentWisdom.adText" class="text-[11px] font-medium text-blue-50/90 leading-relaxed">
                        {{ currentWisdom.tip || currentWisdom.adText }}
                    </p>
                </div>

                <div class="mt-6 pt-4 border-t border-white/10 flex justify-between items-center">
                    <button @click="nextWisdom" class="text-[9px] font-black uppercase tracking-widest text-white/50 hover:text-white transition-colors">
                        Siguiente <span class="ml-1">→</span>
                    </button>
                    <span class="text-[9px] font-black text-white/30 uppercase tracking-widest">KnowFlow Wisdom</span>
                </div>
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

const wisdomList = [
  // Quotes
  { type: 'quote', text: 'El éxito es la suma de pequeños esfuerzos repetidos día tras día.', author: 'Robert Collier' },
  { type: 'quote', text: 'La disciplina es el puente entre las metas y los logros.', author: 'Jim Rohn' },
  { type: 'quote', text: 'No juzgues cada día por lo que cosechas, sino por las semillas que plantas.', author: 'Robert Louis Stevenson' },
  { type: 'quote', text: 'Lo que hoy parece un sacrificio, mañana será tu mayor orgullo.', author: 'Anónimo' },
  { type: 'quote', text: 'Si no vas a por todo, ¿a qué vas?', author: 'Anónimo' },
  
  // Study Methods
  { type: 'tip', text: 'Método SQ3R', tip: 'Examina, Pregunta, Lee, Recita y Repasa. Ideal para comprender textos complejos de forma profunda.' },
  { type: 'tip', text: 'Curva del Olvido', tip: 'Revisa tus notas 24h después, 1 semana después y 1 mes después para fijar el conocimiento para siempre.' },
  { type: 'tip', text: 'Técnica Pomodoro', tip: 'Estudia 25 min y descansa 5 min. Mantendrás tu cerebro fresco y evitarás el agotamiento mental.' },
  { type: 'tip', text: 'Mapas Mentales', tip: 'Usa colores y dibujos para conectar conceptos. El cerebro humano recuerda mejor las imágenes que el texto plano.' },
  
  // KnowFlow Ads (Internal promotions)
  { type: 'ad', text: '¿Sabías que puedes crear cuestionarios?', adText: 'Usa los Knowtionaries para ponerte a prueba y descubrir en qué temas necesitas reforzar.' },
  { type: 'ad', text: 'Organización total con Librerías', adText: 'Divide tus estudios por asignaturas o proyectos para tener todo tu conocimiento a un click.' },
  { type: 'ad', text: 'TimerFlow: Tu mejor aliado', adText: 'Controla tus ciclos de estudio y asegura descansos de calidad para maximizar tu rendimiento.' }
]

const currentWisdomIndex = ref(Math.floor(Math.random() * wisdomList.length))
const currentWisdom = computed(() => wisdomList[currentWisdomIndex.value])

const nextWisdom = () => {
    currentWisdomIndex.value = (currentWisdomIndex.value + 1) % wisdomList.length
}

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

    stats.value = {
      libraries: Array.isArray(libs.data) ? libs.data.length : 0,
      flashcards: Array.isArray(cards.data) ? cards.data.length : 0,
      notes: Array.isArray(notes.data) ? notes.data.length : 0,
      knowtionaries: Array.isArray(quizzes.data) ? quizzes.data.length : 0
    }

    const activity: any[] = []
    
    if (Array.isArray(libs.data)) {
      libs.data.forEach((l: any) => {
        activity.push({
          uniqueId: `lib-${l.id}`,
          id: l.id,
          type: 'library',
          title: l.name,
          description: 'Librería organizada',
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
          description: 'Nueva flashcard',
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
          title: n.title || 'Nota sin título',
          description: 'Contenido guardado',
          date: n.created_at,
          icon: '📄',
          bgClass: 'bg-purple-100 text-purple-600'
        })
      })
    }

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