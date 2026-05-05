<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto py-12 lg:py-16 px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-12 flex flex-col md:flex-row md:items-end md:justify-between gap-6">
        <div>
          <h1 class="text-5xl md:text-6xl font-black bg-gradient-to-br from-gray-900 to-gray-600 dark:from-white dark:to-gray-400 bg-clip-text text-transparent mb-2 tracking-tighter transition-colors duration-300">
            TimerFlow
          </h1>
          <p class="text-lg text-gray-500 dark:text-gray-400 font-medium transition-colors duration-300 italic">"El tiempo es la materia de la que estás hecho."</p>
        </div>
        
        <!-- Quick Stats Header -->
        <div class="flex gap-4">
           <div class="px-6 py-3 bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-3">
             <span class="text-xl">⏱️</span>
             <div>
               <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Hoy</p>
               <p class="text-sm font-black text-gray-900 dark:text-white">{{ todayStats.total_minutes }} min</p>
             </div>
           </div>
           <div class="px-6 py-3 bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-3">
             <span class="text-xl">🔄</span>
             <div>
               <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Ciclos</p>
               <p class="text-sm font-black text-gray-900 dark:text-white">{{ todayStats.cycles }}</p>
             </div>
           </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-10">
        <!-- Main Timer Column -->
        <div class="lg:col-span-8">
          <div class="relative bg-white dark:bg-gray-800 rounded-[4rem] shadow-2xl border border-gray-100 dark:border-gray-700 p-12 md:p-20 overflow-hidden min-h-[650px] flex flex-col items-center justify-center transition-all duration-300">
            <!-- Animated Background -->
            <div class="absolute inset-0 overflow-hidden pointer-events-none">
              <div :class="['absolute -top-24 -right-24 w-96 h-96 rounded-full blur-[100px] transition-colors duration-1000', isRunning ? 'bg-blue-500/10' : 'bg-gray-500/5']"></div>
              <div :class="['absolute -bottom-24 -left-24 w-96 h-96 rounded-full blur-[100px] transition-colors duration-1000', isRunning ? 'bg-purple-500/10' : 'bg-gray-500/5']"></div>
            </div>

            <div class="relative w-full flex flex-col items-center">
              <!-- Mode Selector -->
              <div class="flex bg-gray-100/80 dark:bg-gray-900/50 p-1.5 rounded-[2.5rem] mb-16 space-x-1 z-10 backdrop-blur-md border border-white/20">
                <button 
                  v-for="mode in modes" 
                  :key="mode.id"
                  @click="setMode(mode.id)"
                  :class="[
                    activeMode === mode.id 
                      ? 'bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-400 shadow-xl scale-105' 
                      : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'
                  ]"
                  class="px-8 md:px-10 py-4 rounded-[2rem] font-black text-xs md:text-sm uppercase tracking-widest transition-all duration-500 active:scale-95"
                >
                  {{ mode.label }}
                </button>
              </div>

              <!-- The Clock Visual -->
              <div class="relative group cursor-default select-none my-8 flex items-center justify-center">
                <!-- Outer Progress Ring (Shadow/Glow) -->
                <div class="absolute inset-0 -m-20 md:-m-28 flex items-center justify-center opacity-20">
                    <svg class="w-full h-full -rotate-90 scale-150" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="48" fill="none" stroke="currentColor" stroke-width="0.5" class="text-blue-500" />
                    </svg>
                </div>

                <!-- Main SVG Progress -->
                <div class="absolute inset-0 -m-16 md:-m-24 flex items-center justify-center">
                  <svg class="w-full h-full -rotate-90 scale-125 md:scale-110" viewBox="0 0 100 100">
                    <!-- Track -->
                    <circle 
                      cx="50" cy="50" r="45" 
                      fill="none" 
                      stroke="currentColor" 
                      stroke-width="2" 
                      class="text-gray-100 dark:text-gray-900/80"
                    />
                    <!-- Progress -->
                    <circle 
                      cx="50" cy="50" r="45" 
                      fill="none" 
                      stroke="url(#timerGradient)" 
                      stroke-width="4" 
                      stroke-linecap="round"
                      :stroke-dasharray="dashArray"
                      stroke-dashoffset="0"
                      class="transition-all duration-1000 ease-linear drop-shadow-[0_0_8px_rgba(59,130,246,0.5)]"
                    />
                    <defs>
                      <linearGradient id="timerGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#3b82f6" />
                        <stop offset="100%" stop-color="#8b5cf6" />
                      </linearGradient>
                    </defs>
                  </svg>
                </div>

                <!-- Time Numbers -->
                <div :class="isRunning ? 'scale-110' : 'scale-100'" class="text-[7rem] md:text-[10rem] font-black tracking-tighter leading-none tabular-nums bg-gradient-to-b from-gray-900 to-gray-600 dark:from-white dark:to-gray-400 bg-clip-text text-transparent drop-shadow-2xl z-10 relative transition-all duration-700">
                  {{ formatTime }}
                </div>
              </div>

              <!-- Controls -->
              <div class="flex items-center space-x-10 md:space-x-14 mt-16 z-10">
                <button 
                  @click="resetTimer"
                  class="w-16 h-16 md:w-20 md:h-20 rounded-[2rem] bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 text-gray-400 dark:text-gray-500 flex items-center justify-center hover:text-rose-500 hover:border-rose-100 transition-all active:scale-90 shadow-sm"
                >
                  <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </button>

                <button 
                  @click="toggleTimer"
                  :class="isRunning ? 'bg-rose-500 shadow-rose-500/40 ring-rose-500/20' : 'bg-blue-600 shadow-blue-600/40 ring-blue-600/20'"
                  class="w-32 h-32 md:w-40 md:h-40 rounded-[3.5rem] text-white flex items-center justify-center shadow-2xl ring-8 hover:scale-110 transition-all duration-500 active:scale-95 group overflow-hidden relative"
                >
                  <div class="absolute inset-0 bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                  <svg v-if="!isRunning" class="w-20 h-20 translate-x-1 relative z-10" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M8 5v14l11-7z" />
                  </svg>
                  <svg v-else class="w-20 h-20 relative z-10" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
                  </svg>
                </button>

                <button 
                  @click="skipSession"
                  class="w-16 h-16 md:w-20 md:h-20 rounded-[2rem] bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 text-gray-400 dark:text-gray-500 flex items-center justify-center hover:text-blue-500 hover:border-blue-100 transition-all active:scale-90 shadow-sm"
                >
                  <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side: Sessions History -->
        <div class="lg:col-span-4 space-y-8">
          <div class="bg-white dark:bg-gray-800 rounded-[3rem] p-10 border border-gray-100 dark:border-gray-700 shadow-xl h-full flex flex-col transition-all duration-300">
            <div class="flex items-center justify-between mb-10">
              <h3 class="text-2xl font-black text-gray-900 dark:text-white tracking-tight">Sesiones de Hoy</h3>
              <div class="flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                  <span class="text-xs font-black text-emerald-500 uppercase tracking-widest">Activo</span>
              </div>
            </div>
            
            <div class="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar max-h-[400px]">
              <div v-if="sessions.length > 0" class="space-y-4">
                <div v-for="session in sessions" :key="session.id" class="flex items-center justify-between p-5 bg-gray-50 dark:bg-gray-900/50 rounded-3xl group hover:bg-white dark:hover:bg-gray-700 transition-all border border-transparent hover:border-gray-100 dark:hover:border-gray-600">
                  <div class="flex items-center">
                    <div :class="session.session_type === 'work' ? 'bg-blue-100 text-blue-600 dark:bg-blue-900/40 dark:text-blue-300' : 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/40 dark:text-emerald-300'" class="w-12 h-12 rounded-2xl flex items-center justify-center text-xl mr-4 font-bold">
                      {{ session.session_type === 'work' ? '🧠' : '☕' }}
                    </div>
                    <div>
                      <h4 class="font-black text-gray-900 dark:text-white capitalize text-sm">{{ session.session_type.replace('_', ' ') }}</h4>
                      <p class="text-[10px] font-black text-gray-400 dark:text-gray-500 uppercase tracking-widest">{{ formatSessionTime(session.started_at) }}</p>
                    </div>
                  </div>
                  <div class="text-right">
                    <span class="text-lg font-black text-gray-900 dark:text-white">{{ session.planned_minutes }}m</span>
                  </div>
                </div>
              </div>
              
              <div v-else class="flex flex-col items-center justify-center py-20 text-gray-400 text-center">
                <div class="w-20 h-20 bg-gray-50 dark:bg-gray-900 rounded-[2.5rem] flex items-center justify-center mb-6 shadow-inner">
                    <span class="text-4xl opacity-20">⏳</span>
                </div>
                <p class="font-black text-gray-500 dark:text-gray-400 px-4 text-sm">Empieza tu primera sesión</p>
              </div>
            </div>

            <!-- Motivational Tip Box -->
            <div class="mt-8 p-6 bg-gradient-to-br from-indigo-50 to-blue-50 dark:from-indigo-900/20 dark:to-blue-900/20 rounded-[2rem] border border-blue-100 dark:border-blue-900/30">
               <h4 class="text-xs font-black text-blue-600 dark:text-blue-400 uppercase tracking-widest mb-2">Consejo de Enfoque</h4>
               <p class="text-xs text-blue-800/70 dark:text-blue-300/70 font-medium leading-relaxed">
                   "La técnica Pomodoro funciona mejor si te alejas totalmente de las pantallas durante los descansos."
               </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { timerflowService } from '@/services/api'

const isRunning = ref(false)
const activeMode = ref('work')
const timeLeft = ref(25 * 60)
const totalTime = ref(25 * 60)
let timerId = null

const settings = ref({
  default_minutes: 25,
  short_break: 5,
  long_break: 15,
  cycle_before_long_break: 4
})

const sessions = ref([])
const todayStats = ref({
  total_minutes: 0,
  cycles: 0
})

const modes = [
  { id: 'work', label: 'Enfoque', minutes: 25 },
  { id: 'short_break', label: 'Descanso', minutes: 5 },
  { id: 'long_break', label: 'Largo', minutes: 15 }
]

const formatTime = computed(() => {
  const m = Math.floor(timeLeft.value / 60)
  const s = timeLeft.value % 60
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
})

const dashArray = computed(() => {
  const radius = 45 
  const circumference = 2 * Math.PI * radius
  const progress = (timeLeft.value / totalTime.value) * circumference
  return `${progress} ${circumference}`
})

const setMode = (modeId) => {
  if (isRunning.value) {
    if (!confirm('¿Quieres cambiar de modo? El progreso actual se perderá.')) return
  }
  
  activeMode.value = modeId
  isRunning.value = false
  clearInterval(timerId)
  
  const minutes = modeId === 'work' ? settings.value.default_minutes 
                : modeId === 'short_break' ? settings.value.short_break 
                : settings.value.long_break
                
  timeLeft.value = minutes * 60
  totalTime.value = minutes * 60
}

const toggleTimer = () => {
  if (isRunning.value) {
    clearInterval(timerId)
    isRunning.value = false
  } else {
    isRunning.value = true
    timerId = setInterval(() => {
      if (timeLeft.value > 0) {
        timeLeft.value--
      } else {
        handleTimerComplete()
      }
    }, 1000)
  }
}

const resetTimer = () => {
  if (isRunning.value) {
    if (!confirm('¿Reiniciar el temporizador?')) return
  }
  clearInterval(timerId)
  isRunning.value = false
  timeLeft.value = totalTime.value
}

const handleTimerComplete = async () => {
  clearInterval(timerId)
  isRunning.value = false
  
  // Play sound if possible
  try {
      const audio = new Audio('https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3')
      audio.play()
  } catch(e) {}

  // Save session to backend
  try {
    await timerflowService.createSession({
      planned_minutes: Math.floor(totalTime.value / 60),
      session_type: activeMode.value,
      completed: true
    })
    await loadData() // Reload both sessions and stats
  } catch (error) {
    console.error('Error saving session:', error)
  }

  // Auto-switch logic
  if (activeMode.value === 'work') {
    if (todayStats.value.cycles % settings.value.cycle_before_long_break === 0) {
      setMode('long_break')
    } else {
      setMode('short_break')
    }
  } else {
    setMode('work')
  }
}

const skipSession = () => {
  if (confirm('¿Saltar esta sesión? No se contará como completada.')) {
    if (activeMode.value === 'work') {
      setMode('short_break')
    } else {
      setMode('work')
    }
  }
}

const loadData = async () => {
  try {
    const [sessionsRes, statsRes] = await Promise.all([
      timerflowService.getSessions(),
      timerflowService.getTodayStats()
    ])
    sessions.value = sessionsRes.data
    todayStats.value = statsRes.data
  } catch (error) {
    console.error('Error loading timer data:', error)
  }
}

const loadSettings = async () => {
  try {
    const response = await timerflowService.getSettings()
    settings.value = response.data
    if (!isRunning.value) {
      const minutes = activeMode.value === 'work' ? settings.value.default_minutes 
                    : activeMode.value === 'short_break' ? settings.value.short_break 
                    : settings.value.long_break
      timeLeft.value = minutes * 60
      totalTime.value = minutes * 60
    }
  } catch (error) {
    console.error('Error loading settings:', error)
  }
}

const formatSessionTime = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

onMounted(() => {
  loadSettings()
  loadData()
})

onUnmounted(() => {
  clearInterval(timerId)
})

watch(formatTime, (newVal) => {
  if (isRunning.value) {
    document.title = `${newVal} - Enfoque`
  } else {
    document.title = 'KnowFlow'
  }
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 10px;
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #374151;
}

@keyframes pulse-soft {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.02); opacity: 0.9; }
}

.animate-pulse-soft {
  animation: pulse-soft 3s infinite ease-in-out;
}
</style>
