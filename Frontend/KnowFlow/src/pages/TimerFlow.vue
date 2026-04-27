<template>
  <DefaultLayout>
    <div class="max-w-4xl mx-auto py-12 px-4">
      <div class="text-center mb-16">
        <div class="w-24 h-24 bg-gradient-to-br from-orange-500 to-red-500 rounded-3xl mx-auto mb-8 shadow-2xl flex items-center justify-center">
          <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h1 class="text-5xl font-black bg-gradient-to-r from-gray-900 via-orange-600 to-red-500 bg-clip-text text-transparent mb-4">TimerFlow</h1>
        <p class="text-2xl text-gray-600 mb-8">Pomodoro inteligente para tu estudio</p>
      </div>

      <!-- Timer Controls -->
      <div class="bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl p-12 mb-12">
        <div class="text-center">
          <!-- Timer Display -->
          <div class="mb-12">
            <div class="text-8xl font-mono font-black text-gray-900 mb-4" id="timer">
              25:00
            </div>
            <div class="inline-flex gap-4">
              <button @click="setMode('work')" :class="['px-8 py-4 rounded-2xl font-bold text-xl transition-all shadow-lg', mode === 'work' ? 'bg-gradient-to-r from-orange-500 to-red-500 text-white shadow-orange-500/50' : 'bg-gray-100 hover:bg-gray-200 text-gray-800']">
                Trabajo (25min)
              </button>
              <button @click="setMode('short')" :class="['px-8 py-4 rounded-2xl font-bold text-xl transition-all shadow-lg', mode === 'short' ? 'bg-gradient-to-r from-green-500 to-emerald-500 text-white shadow-green-500/50' : 'bg-gray-100 hover:bg-gray-200 text-gray-800']">
                Pausa (5min)
              </button>
              <button @click="setMode('long')" :class="['px-8 py-4 rounded-2xl font-bold text-xl transition-all shadow-lg', mode === 'long' ? 'bg-gradient-to-r from-blue-500 to-indigo-500 text-white shadow-blue-500/50' : 'bg-gray-100 hover:bg-gray-200 text-gray-800']">
                Pausa Larga (15min)
              </button>
            </div>
          </div>

          <!-- Control Buttons -->
          <div class="flex justify-center gap-6 mb-12">
            <button @click="startTimer" :disabled="isRunning" class="px-12 py-6 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-3xl font-bold text-xl shadow-2xl hover:shadow-3xl transform hover:-translate-y-1 transition-all disabled:opacity-50 disabled:cursor-not-allowed">
              <svg v-if="!isRunning" class="w-8 h-8 inline mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v6a1 1 0 102 0v-6zM9 18a1 1 0 100 2 1 1 0 000-2z" clip-rule="evenodd" />
              </svg>
              {{ isRunning ? 'Pausado' : 'Iniciar' }}
            </button>
            <button @click="stopTimer" :disabled="!isRunning" class="px-12 py-6 bg-gradient-to-r from-red-500 to-rose-600 text-white rounded-3xl font-bold text-xl shadow-2xl hover:shadow-3xl transform hover:-translate-y-1 transition-all disabled:opacity-50 disabled:cursor-not-allowed">
              <svg class="w-8 h-8 inline mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
              Stop
            </button>
          </div>

          <!-- Progress Ring -->
          <div class="relative w-64 h-64 mx-auto mb-12">
            <svg class="w-full h-full transform -rotate-90">
              <circle cx="128" cy="128" r="120" stroke="currentColor" stroke-width="8" fill="transparent" stroke-opacity="0.1" class="text-gray-300"/>
              <circle cx="128" cy="128" r="120" stroke="currentColor" stroke-width="8" fill="transparent" stroke-linecap="round" stroke-dasharray="753.98" stroke-dashoffset="v-bind:dashOffset" class="text-orange-500 transition-all duration-100"/>
            </svg>
            <div class="absolute inset-0 flex flex-col items-center justify-center">
              <div class="text-3xl font-bold text-gray-700">{{ cyclesCount }}</div>
              <div class="text-sm text-gray-500">Ciclos</div>
            </div>
          </div>

          <!-- Settings -->
          <div class="max-w-md mx-auto">
            <div class="grid grid-cols-3 gap-4 text-sm">
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Trabajo</label>
                <input v-model.number="settings.work" type="number" min="1" max="99" class="w-full px-3 py-2 border border-gray-300 rounded-xl text-center font-mono">
                <span class="text-xs text-gray-500">min</span>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Pausa Corta</label>
                <input v-model.number="settings.short" type="number" min="1" max="20" class="w-full px-3 py-2 border border-gray-300 rounded-xl text-center font-mono">
                <span class="text-xs text-gray-500">min</span>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Pausa Larga</label>
                <input v-model.number="settings.long" type="number" min="5" max="60" class="w-full px-3 py-2 border border-gray-300 rounded-xl text-center font-mono">
                <span class="text-xs text-gray-500">min</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Sessions -->
      <div class="grid lg:grid-cols-2 gap-8">
        <div class="bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl p-8">
          <h3 class="text-2xl font-bold text-gray-900 mb-6">Sesiones Recientes</h3>
          <div v-if="sessions.length" class="space-y-4">
            <div v-for="session in sessions.slice(0,5)" :key="session.id" class="flex items-center space-x-4 p-4 bg-gradient-to-r from-gray-50 rounded-2xl">
              <div class="w-12 h-12 rounded-xl flex items-center justify-center font-mono text-sm" :class="session.session_type === 'work' ? 'bg-orange-100 text-orange-600' : session.session_type === 'short_break' ? 'bg-green-100 text-green-600' : 'bg-blue-100 text-blue-600'">
                {{ formatMinutes(session.planned_minutes) }}
              </div>
              <div class="flex-1">
                <div class="font-semibold text-gray-900">{{ session.session_type.replace('_', ' ').toUpperCase() }}</div>
                <div class="text-sm text-gray-500">{{ new Date(session.started_at).toLocaleString('es-ES') }}</div>
              </div>
              <div class="text-sm font-medium" :class="session.completed ? 'text-green-600' : 'text-gray-400'">✓</div>
            </div>
          </div>
          <div v-else class="text-center py-12 text-gray-500">
            Inicia tu primera sesión
          </div>
        </div>

        <div class="bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl p-8">
          <h3 class="text-2xl font-bold text-gray-900 mb-6">Estadísticas</h3>
          <div class="grid grid-cols-2 gap-6">
            <div class="text-center p-6 bg-gradient-to-br from-orange-50 rounded-2xl">
              <div class="text-3xl font-bold text-orange-600">{{ totalWork }}</div>
              <div class="text-sm text-gray-600 uppercase tracking-wide">Min Trabajo</div>
            </div>
            <div class="text-center p-6 bg-gradient-to-br from-green-50 rounded-2xl">
              <div class="text-3xl font-bold text-green-600">{{ totalSessions }}</div>
              <div class="text-sm text-gray-600 uppercase tracking-wide">Sesiones</div>
            </div>
            <div class="text-center p-6 bg-gradient-to-br from-blue-50 rounded-2xl">
              <div class="text-3xl font-bold text-blue-600">{{ avgSession }}</div>
              <div class="text-sm text-gray-600 uppercase tracking-wide">Promedio</div>
            </div>
            <div class="text-center p-6 bg-gradient-to-br from-purple-50 rounded-2xl">
              <div class="text-3xl font-bold text-purple-600">{{ completionRate }}%</div>
              <div class="text-sm text-gray-600 uppercase tracking-wide">Completado</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

interface StudySession {
  id: number
  planned_minutes: number
  session_type: string
  completed: boolean
  started_at: string
  ended_at: string | null
}

const sessions = ref<StudySession[]>([])
const isRunning = ref(false)
const currentTime = ref(25 * 60)
const mode = ref<'work' | 'short' | 'long'>('work')
const settings = ref({
  work: 25,
  short: 5,
  long: 15
})
const timerId = ref<number | null>(null)
const cyclesCount = ref(0)
const cycleCount = ref(0)

import { computed } from 'vue'
const dashOffset = computed(() => {
  const percent = (currentTime.value / getCurrentDuration()) * 753.98
  return Math.max(0, 753.98 - percent)
})

const getCurrentDuration = () => {
  return mode.value === 'work' ? settings.value.work * 60 : mode.value === 'short' ? settings.value.short * 60 : settings.value.long * 60
}

const formatTime = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const formatMinutes = (minutes: number) => minutes.toString().padStart(2, '0')

const setMode = (newMode: 'work' | 'short' | 'long') => {
  mode.value = newMode
  const duration = getCurrentDuration()
  currentTime.value = duration
  document.getElementById('timer')!.textContent = formatTime(duration)
}

const startTimer = () => {
  isRunning.value = true
  timerId.value = setInterval(() => {
    currentTime.value--
    document.getElementById('timer')!.textContent = formatTime(currentTime.value)
    
    if (currentTime.value <= 0) {
      stopTimer()
      cyclesCount.value++
      cycleCount.value++
      // Auto next
      setTimeout(() => {
        if (cycleCount.value % 4 === 0) {
          setMode('long')
        } else {
          setMode('short')
        }
        startTimer()
      }, 1000)
      // Save session
      saveSession()
    }
  }, 1000)
}

const stopTimer = () => {
  isRunning.value = false
  if (timerId.value) {
    clearInterval(timerId.value)
    timerId.value = null
  }
}

const saveSession = async () => {
  const type = mode.value === 'work' ? 'work' : mode.value === 'short' ? 'short_break' : 'long_break'
  const data = {
    planned_minutes: getCurrentDuration() / 60,
    session_type: type,
    completed: true
  }
  // TODO: api.post('timerflow/create_studysession/', data)
  console.log('Session saved:', data)
}

onMounted(() => {
  loadSessions()
})

onUnmounted(() => {
  if (timerId.value) clearInterval(timerId.value)
})

const loadSessions = async () => {
  // TODO: api.get('timerflow/studysession_list/')
  sessions.value = []
}

const totalWork = ref(0)
const totalSessions = ref(0)
const avgSession = ref(0)
const completionRate = ref(100)
</script>

<style scoped>
#timer {
  font-variant-numeric: tabular-nums;
}
</style>
