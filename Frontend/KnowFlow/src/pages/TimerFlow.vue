<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-12">
        <h1 class="text-4xl md:text-5xl font-black bg-gradient-to-br from-gray-900 to-gray-600 dark:from-white dark:to-gray-300 bg-clip-text text-transparent mb-2 tracking-tighter transition-colors duration-300">
          TimerFlow
        </h1>
        <p class="text-lg text-gray-500 dark:text-gray-400 font-medium transition-colors duration-300">Controla tu tiempo, potencia tu mente.</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-10">
        <!-- Main Timer Column (Left/Center) -->
        <div class="lg:col-span-8">
          <div class="relative bg-white dark:bg-gray-800 rounded-[4rem] shadow-2xl border border-gray-100 dark:border-gray-700 p-12 md:p-20 overflow-hidden min-h-[600px] flex flex-col items-center justify-center transition-all duration-300">
            <!-- Background Decorators -->
            <div class="absolute -top-24 -right-24 w-64 h-64 bg-blue-500/5 rounded-full blur-3xl"></div>
            <div class="absolute -bottom-24 -left-24 w-64 h-64 bg-indigo-500/5 rounded-full blur-3xl"></div>

            <div class="relative w-full flex flex-col items-center">
              <!-- Mode Selector -->
              <div class="flex bg-gray-100 dark:bg-gray-900/50 p-2 rounded-[2.5rem] mb-12 space-x-2 z-10">
                <button 
                  v-for="mode in modes" 
                  :key="mode.id"
                  @click="setMode(mode.id)"
                  :class="[
                    activeMode === mode.id 
                      ? 'bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-400 shadow-xl scale-105' 
                      : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'
                  ]"
                  class="px-6 md:px-10 py-4 rounded-3xl font-black text-xs md:text-sm uppercase tracking-widest transition-all duration-300 active:scale-95"
                >
                  {{ mode.label }}
                </button>
              </div>

              <!-- The Clock -->
              <div class="relative group cursor-default select-none my-8 md:my-12 flex items-center justify-center">
                <!-- Progress Ring Container -->
                <div class="absolute inset-0 -m-16 md:-m-24 flex items-center justify-center">
                  <svg class="w-full h-full -rotate-90 scale-125 md:scale-110" viewBox="0 0 100 100">
                    <!-- Background Circle -->
                    <circle 
                      cx="50" cy="50" r="45" 
                      fill="none" 
                      stroke="currentColor" 
                      stroke-width="3" 
                      class="text-gray-100 dark:text-gray-900/80"
                    />
                    <!-- Progress Circle -->
                    <circle 
                      cx="50" cy="50" r="45" 
                      fill="none" 
                      stroke="url(#timerGradient)" 
                      stroke-width="3" 
                      stroke-linecap="round"
                      :stroke-dasharray="dashArray"
                      class="transition-all duration-1000 ease-linear"
                    />
                    <defs>
                      <linearGradient id="timerGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#3b82f6" />
                        <stop offset="100%" stop-color="#8b5cf6" />
                      </linearGradient>
                    </defs>
                  </svg>
                </div>

                <!-- Clock Numbers (Reduced size to fit inside circle) -->
                <div class="text-[6rem] md:text-[9rem] font-black tracking-tighter leading-none tabular-nums bg-gradient-to-b from-gray-900 to-gray-600 dark:from-white dark:to-gray-200 bg-clip-text text-transparent drop-shadow-2xl z-10 relative transition-colors duration-300">
                  {{ formatTime }}
                </div>
              </div>

              <!-- Controls -->
              <div class="flex items-center space-x-8 md:space-x-12 mt-12 z-10">
                <button 
                  @click="resetTimer"
                  class="w-16 h-16 md:w-20 md:h-20 rounded-[2rem] bg-gray-50 dark:bg-gray-900/50 text-gray-500 dark:text-gray-300 flex items-center justify-center hover:bg-gray-100 dark:hover:bg-gray-700 transition-all active:scale-90 shadow-sm"
                  title="Reiniciar"
                >
                  <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </button>

                <button 
                  @click="toggleTimer"
                  :class="isRunning ? 'bg-rose-500 shadow-rose-500/30' : 'bg-blue-600 shadow-blue-600/30'"
                  class="w-28 h-28 md:w-36 md:h-36 rounded-[3rem] text-white flex items-center justify-center shadow-2xl hover:scale-105 transition-all active:scale-95 group"
                >
                  <svg v-if="!isRunning" class="w-16 h-16 translate-x-1" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M8 5v14l11-7z" />
                  </svg>
                  <svg v-else class="w-16 h-16" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
                  </svg>
                </button>

                <button 
                  @click="skipSession"
                  class="w-16 h-16 md:w-20 md:h-20 rounded-[2rem] bg-gray-50 dark:bg-gray-900/50 text-gray-500 dark:text-gray-300 flex items-center justify-center hover:bg-gray-100 dark:hover:bg-gray-700 transition-all active:scale-90 shadow-sm"
                  title="Siguiente"
                >
                  <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- History Column (Right) -->
        <div class="lg:col-span-4">
          <div class="bg-white dark:bg-gray-800 rounded-[3rem] p-10 border border-gray-100 dark:border-gray-700 shadow-xl h-full flex flex-col transition-colors duration-300">
            <div class="flex items-center justify-between mb-10">
              <h3 class="text-2xl font-black text-gray-900 dark:text-white tracking-tight">Sesiones de Hoy</h3>
              <span class="px-4 py-2 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 text-xs font-black rounded-full uppercase tracking-widest">{{ sessions.length }}</span>
            </div>
            
            <div class="flex-1 overflow-y-auto space-y-5 pr-2 custom-scrollbar">
              <div v-if="sessions.length > 0" class="space-y-4">
                <div v-for="session in sessions" :key="session.id" class="flex items-center justify-between p-6 bg-gray-50 dark:bg-gray-900/50 rounded-[2rem] group hover:bg-white dark:hover:bg-gray-700 transition-all border border-transparent hover:border-gray-100 dark:hover:border-gray-600 shadow-sm hover:shadow-md">
                  <div class="flex items-center">
                    <div :class="session.session_type === 'work' ? 'bg-blue-100 text-blue-600 dark:bg-blue-900/40 dark:text-blue-300' : 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/40 dark:text-emerald-300'" class="w-12 h-12 rounded-2xl flex items-center justify-center text-xl mr-4 font-bold shadow-inner">
                      {{ session.session_type === 'work' ? '🧠' : '☕' }}
                    </div>
                    <div>
                      <h4 class="font-black text-gray-900 dark:text-white capitalize text-sm">{{ session.session_type.replace('_', ' ') }}</h4>
                      <p class="text-[10px] font-black text-gray-500 dark:text-gray-400 uppercase tracking-widest">{{ formatSessionTime(session.started_at) }}</p>
                    </div>
                  </div>
                  <div class="text-right">
                    <span class="text-lg font-black text-gray-900 dark:text-white">{{ session.planned_minutes }}m</span>
                    <p class="text-[10px] font-black text-emerald-500 dark:text-emerald-400 uppercase tracking-widest">OK</p>
                  </div>
                </div>
              </div>
              
              <div v-else class="flex flex-col items-center justify-center py-20 text-gray-400 text-center">
                <div class="w-20 h-20 bg-gray-50 dark:bg-gray-900 rounded-[2rem] flex items-center justify-center mb-6 shadow-inner">
                   <svg class="w-10 h-10 opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <p class="font-black text-gray-500 dark:text-gray-400 px-4 text-sm">¡Aún no hay registros hoy!</p>
              </div>
            </div>

            <!-- Summary Stats -->
            <div class="mt-10 pt-8 border-t border-gray-50 dark:border-gray-700">
              <div class="grid grid-cols-2 gap-4">
                <div class="bg-blue-50 dark:bg-blue-900/20 p-5 rounded-3xl text-center">
                  <p class="text-[10px] font-black text-blue-600 dark:text-blue-400 uppercase tracking-widest mb-1">Tiempo Total</p>
                  <p class="text-2xl font-black text-gray-900 dark:text-white">{{ totalWorkTime }}m</p>
                </div>
                <div class="bg-emerald-50 dark:bg-emerald-900/20 p-5 rounded-3xl text-center">
                  <p class="text-[10px] font-black text-emerald-600 dark:text-emerald-400 uppercase tracking-widest mb-1">Ciclos</p>
                  <p class="text-2xl font-black text-gray-900 dark:text-white">{{ completedCyclesCount }}</p>
                </div>
              </div>
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
const completedCycles = ref(0)

const modes = [
  { id: 'work', label: 'Enfoque', minutes: 25 },
  { id: 'short_break', label: 'Corto', minutes: 5 },
  { id: 'long_break', label: 'Largo', minutes: 15 }
]

const formatTime = computed(() => {
  const m = Math.floor(timeLeft.value / 60)
  const s = timeLeft.value % 60
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
})

const dashArray = computed(() => {
  const radius = 45 // Fixed radius for SVG
  const circumference = 2 * Math.PI * radius
  const progress = (timeLeft.value / totalTime.value) * circumference
  return `${progress} ${circumference}`
})

const totalWorkTime = computed(() => {
  return sessions.value
    .filter(s => s.session_type === 'work')
    .reduce((total, s) => total + s.planned_minutes, 0)
})

const completedCyclesCount = computed(() => {
  return sessions.value.filter(s => s.session_type === 'work').length
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
  
  // Save session to backend
  try {
    await timerflowService.createSession({
      planned_minutes: Math.floor(totalTime.value / 60),
      session_type: activeMode.value,
      completed: true
    })
    loadSessions()
  } catch (error) {
    console.error('Error saving session:', error)
  }

  // Auto-switch mode
  if (activeMode.value === 'work') {
    completedCycles.value++
    if (completedCycles.value >= settings.value.cycle_before_long_break) {
      setMode('long_break')
      completedCycles.value = 0
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

const loadSessions = async () => {
  try {
    const response = await timerflowService.getSessions()
    sessions.value = response.data
  } catch (error) {
    console.error('Error loading sessions:', error)
  }
}

const loadSettings = async () => {
  try {
    const response = await timerflowService.getSettings()
    settings.value = response.data
    // Update current timer if not running
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
  loadSessions()
})

onUnmounted(() => {
  clearInterval(timerId)
})

watch(formatTime, (newVal) => {
  if (isRunning.value) {
    document.title = `${newVal} - TimerFlow`
  } else {
    document.title = 'KnowFlow'
  }
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
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
</style>
