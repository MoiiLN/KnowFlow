<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto py-8 px-4">
      <div class="flex flex-col lg:flex-row gap-8 items-start lg:items-center justify-between mb-12">
        <div>
          <h1 class="text-4xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent mb-3">
            Knowtionaries
          </h1>
          <p class="text-xl text-gray-600 max-w-2xl">Crea cuestionarios interactivos con scoring automático 1-10</p>
        </div>
        <button @click="showCreateModal = true" class="bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-8 py-4 rounded-2xl font-bold shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all whitespace-nowrap">
          + Nuevo Cuestionario
        </button>
      </div>

      <!-- Search & Filter -->
      <div class="bg-white rounded-2xl shadow-lg p-6 mb-8">
        <div class="flex flex-col lg:flex-row gap-4 items-center lg:items-end">
          <div class="relative flex-1 max-w-md">
            <input v-model="searchTerm" placeholder="Buscar cuestionarios..." class="w-full pl-12 pr-4 py-4 border border-gray-200 rounded-2xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 text-lg">
            <svg class="w-6 h-6 text-gray-400 absolute left-4 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <div class="flex gap-2">
            <button @click="filterType = 'all'" :class="['px-6 py-3 rounded-xl font-semibold transition-all', filterType === 'all' ? 'bg-gradient-to-r from-purple-500 to-indigo-500 text-white shadow-lg' : 'bg-gray-100 hover:bg-gray-200']">
              Todos
            </button>
            <button @click="filterType = 'mine'" :class="['px-6 py-3 rounded-xl font-semibold transition-all', filterType === 'mine' ? 'bg-gradient-to-r from-purple-500 to-indigo-500 text-white shadow-lg' : 'bg-gray-100 hover:bg-gray-200']">
              Míos
            </button>
            <button @click="filterType = 'public'" :class="['px-6 py-3 rounded-xl font-semibold transition-all', filterType === 'public' ? 'bg-gradient-to-r from-green-500 to-emerald-500 text-white shadow-lg' : 'bg-gray-100 hover:bg-gray-200']">
              Públicos
            </button>
          </div>
        </div>
      </div>

      <!-- Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        <div v-for="quiz in filteredQuizzes" :key="quiz.id" class="group">
          <div class="bg-gradient-to-br from-white to-gray-50 rounded-3xl p-8 shadow-xl hover:shadow-2xl hover:-translate-y-3 transition-all cursor-pointer border border-gray-100 hover:border-purple-200 overflow-hidden h-full" @click="openQuiz(quiz)">
            <div class="relative">
              <div class="w-16 h-16 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-2xl flex items-center justify-center mb-6 shadow-lg group-hover:scale-110 transition-all">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-gray-900 mb-3 line-clamp-2 group-hover:text-purple-600">{{ quiz.name }}</h3>
              <p class="text-gray-600 mb-4 line-clamp-2 leading-relaxed">{{ quiz.description }}</p>
              <div class="flex items-center gap-4 mb-6 text-sm">
                <span class="px-3 py-1 bg-purple-100 text-purple-800 rounded-full font-medium">
                  {{ quiz.questions_count }} preguntas
                </span>
                <span class="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full font-medium">
                  {{ Math.round(quiz.avg_score) }}/10
                </span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-500">{{ formatDate(quiz.created_at) }}</span>
                <button class="px-4 py-2 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 transition-all group-hover:bg-purple-50">
                  {{ quiz.is_owner ? 'Mis' : 'Por ' + quiz.author }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="filteredQuizzes.length === 0" class="col-span-full bg-white rounded-3xl shadow-lg p-20 flex flex-col items-center justify-center border-2 border-dashed border-gray-300">
          <div class="w-24 h-24 bg-gradient-to-br from-purple-100 to-indigo-100 rounded-3xl flex items-center justify-center mb-8">
            <svg class="w-12 h-12 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-3xl font-bold text-gray-900 mb-4">{{ searchTerm ? 'Sin resultados' : 'Sin cuestionarios' }}</h3>
          <p class="text-xl text-gray-600 mb-8 text-center">Crea tu primer cuestionario interactivo</p>
          <button @click="showCreateModal = true" class="bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-10 py-4 rounded-2xl font-bold shadow-xl hover:shadow-2xl transition-all">
            Crear Cuestionario
          </button>
        </div>
      </div>

      <!-- Create Modal -->
      <div v-if="showCreateModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-6">
        <div class="bg-white rounded-3xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden">
          <div class="p-8">
            <div class="flex items-center justify-between mb-8">
              <h2 class="text-3xl font-bold bg-gradient-to-r from-purple-600 to-indigo-600 bg-clip-text text-transparent">
                Nuevo Cuestionario
              </h2>
              <button @click="closeCreateModal" class="text-gray-400 hover:text-gray-600 p-2 rounded-xl hover:bg-gray-100">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <form @submit.prevent="createQuiz">
              <div class="space-y-6">
                <div>
                  <label class="block text-lg font-semibold text-gray-900 mb-3">Nombre del cuestionario *</label>
                  <input v-model="createForm.name" required class="w-full px-6 py-4 border border-gray-300 rounded-2xl focus:ring-3 focus:ring-purple-500/20 focus:border-purple-500 text-lg">
                </div>
                <div>
                  <label class="block text-lg font-semibold text-gray-900 mb-3">Descripción</label>
                  <textarea v-model="createForm.description" rows="3" class="w-full px-6 py-4 border border-gray-300 rounded-2xl focus:ring-3 focus:ring-purple-500/20 focus:border-purple-500 text-lg resize-vertical"></textarea>
                </div>
                <div>
                  <label class="block text-lg font-semibold text-gray-900 mb-3">Puntuación máxima por pregunta</label>
  <input v-model.number="createForm.max_score_per_question" type="number" min="1" max="10" class="w-full px-6 py-4 border border-gray-300 rounded-2xl focus:ring-3 focus:ring-purple-500/20 focus:border-purple-500 text-lg">
                </div>
              </div>
              <div class="flex gap-4 justify-end mt-10">
                <button type="button" @click="closeCreateModal" class="px-10 py-4 border border-gray-300 text-gray-700 rounded-2xl font-semibold hover:bg-gray-50 transition-all">
                  Cancelar
                </button>
                <button type="submit" :disabled="creatingQuiz" class="px-10 py-4 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-2xl font-bold shadow-xl hover:shadow-2xl disabled:opacity-50">
                  {{ creatingQuiz ? 'Creando...' : 'Crear Cuestionario' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Quiz Modal -->
      <div v-if="currentQuiz" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-6">
        <div class="bg-white rounded-3xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
          <div class="sticky top-0 bg-white p-6 border-b">
            <div class="flex items-center gap-4">
              <button @click="closeQuiz" class="p-2 rounded-xl hover:bg-gray-100">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <div class="flex-1">
                <h2 class="text-3xl font-bold text-gray-900">{{ currentQuiz.name }}</h2>
                <p class="text-lg text-gray-600">{{ currentQuiz.questions_count }} preguntas</p>
              </div>
              <button @click="startQuiz" :disabled="!currentQuiz.questions.length" class="bg-gradient-to-r from-emerald-500 to-green-600 text-white px-8 py-3 rounded-xl font-bold shadow-lg hover:shadow-xl">
                {{ quizStarted ? 'Continuar Quiz' : 'Empezar Quiz' }}
              </button>
            </div>
          </div>
          <div class="p-8">
            <div v-if="!quizStarted" class="text-center py-20">
              <div class="w-32 h-32 mx-auto mb-8 bg-gradient-to-br from-emerald-100 to-green-100 rounded-3xl flex items-center justify-center">
                <svg class="w-16 h-16 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-gray-900 mb-4">Listo para empezar</h3>
              <p class="text-lg text-gray-600 mb-8">Responde todas las preguntas correctamente para obtener tu puntuación</p>
              <div class="grid grid-cols-2 gap-4 max-w-md mx-auto">
                <div class="text-center p-6 bg-gray-50 rounded-xl">
                  <div class="text-3xl font-bold text-indigo-600">{{ currentQuiz.questions_count }}</div>
                  <div class="text-sm text-gray-600">Preguntas</div>
                </div>
                <div class="text-center p-6 bg-gray-50 rounded-xl">
                  <div class="text-3xl font-bold text-emerald-600">{{ currentQuiz.max_score_per_question || 1 }}</div>
                  <div class="text-sm text-gray-600">Puntos máx</div>
                </div>
              </div>
            </div>

            <div v-else-if="currentQuestionIndex < currentQuiz.questions.length">
              <div class="mb-8">
                <div class="flex items-center gap-4 mb-6">
                  <div class="flex items-center gap-2 text-sm text-gray-500">
                    <span class="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center font-bold text-indigo-700 text-xs">{{ currentQuestionIndex + 1 }}</span>
                    <span>de {{ currentQuiz.questions_count }}</span>
                  </div>
                  <div class="ml-auto">
                    <div class="flex items-center gap-2">
                      <div class="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                        <span class="text-white font-bold text-lg">{{ currentQuiz.max_score_per_question || 1 }}pts</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="bg-gradient-to-r from-indigo-50 to-purple-50 p-8 rounded-3xl border border-indigo-200">
                  <h3 class="text-2xl font-bold text-gray-900 mb-6">{{ currentQuiz.questions[currentQuestionIndex].question }}</h3>
                  <div class="space-y-3">
                    <label v-for="(option, index) in currentQuiz.questions[currentQuestionIndex].options" :key="index" class="flex items-center p-4 border-2 border-gray-200 rounded-2xl hover:border-indigo-400 hover:bg-indigo-50 transition-all cursor-pointer group" :class="{ 'border-emerald-400 bg-emerald-50 shadow-md ring-2 ring-emerald-200': answers[currentQuestionIndex] === index }">
                      <input type="radio" :value="index" v-model="answers[currentQuestionIndex]" class="sr-only">
                      <span class="w-6 h-6 mr-4 rounded-full border-2 border-gray-400 flex items-center justify-center text-sm font-bold group-hover:border-indigo-500" :class="{ 'bg-emerald-500 border-emerald-500 text-white': answers[currentQuestionIndex] === index }">
                        {{ String.fromCharCode(65 + index) }}
                      </span>
                      <span class="font-semibold text-gray-900 group-hover:text-indigo-700">{{ option }}</span>
                    </label>
                  </div>
                </div>
                <div class="flex gap-4 mt-12">
                  <button v-if="currentQuestionIndex > 0" @click="previousQuestion" class="flex-1 px-8 py-4 border border-gray-300 rounded-2xl font-semibold hover:bg-gray-50">
                    Anterior
                  </button>
                  <button :disabled="currentQuestionIndex === currentQuiz.questions_count - 1" @click="nextQuestion" class="flex-1 px-8 py-4 bg-indigo-600 text-white rounded-2xl font-semibold hover:bg-indigo-700 shadow-lg disabled:opacity-50">
                    {{ currentQuestionIndex === currentQuiz.questions_count - 1 ? 'Finalizar' : 'Siguiente' }}
                  </button>
                </div>
              </div>
            </div>

            <!-- Results -->
            <div v-else class="text-center py-20">
              <div class="w-48 h-48 mx-auto mb-12 relative">
                <svg class="w-full h-full" viewBox="0 0 200 200">
                  <circle cx="100" cy="100" r="85" fill="none" stroke="#e5e7eb" stroke-width="15"></circle>
                  <circle cx="100" cy="100" r="85" fill="none" stroke="#10b981" stroke-width="15" stroke-linecap="round" :stroke-dasharray="circumference" :stroke-dashoffset="circumference - progress * circumference / 100" stroke-dasharray="530"></circle>
                </svg>
                <div class="absolute inset-0 flex items-center justify-center">
                  <div class="text-5xl font-black bg-gradient-to-r from-emerald-500 to-green-600 bg-clip-text text-transparent">
                    {{ score }}/10
                  </div>
                </div>
              </div>
              <h2 class="text-4xl font-bold text-gray-900 mb-4">¡Resultado obtenido!</h2>
              <p class="text-2xl text-gray-600 mb-12">{{ scoreText }}</p>
              <div class="max-w-2xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-4 mb-12">
                <div class="bg-emerald-50 p-6 rounded-2xl">
                  <div class="text-3xl font-bold text-emerald-600 mb-2">{{ correctAnswers }}</div>
                  <div class="text-sm text-emerald-700 font-semibold">Correctas</div>
                </div>
                <div class="bg-gray-50 p-6 rounded-2xl">
                  <div class="text-3xl font-bold text-gray-900 mb-2">{{ totalQuestions }}</div>
                  <div class="text-sm text-gray-700 font-semibold">Total</div>
                </div>
              </div>
              <div class="space-x-4">
                <button @click="restartQuiz" class="px-10 py-4 bg-indigo-600 text-white rounded-2xl font-bold hover:bg-indigo-700 shadow-lg">
                  Repetir
                </button>
                <button @click="closeQuiz" class="px-10 py-4 border border-gray-300 rounded-2xl font-semibold hover:bg-gray-50">
                  Cerrar
                </button>
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
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import api from '@/services/api'

interface Quiz {
  id: number
  name: string
  slug: string
  description: string
  questions_count: number
  avg_score: number
  max_score_per_question: number
  questions: Array<{
    question: string
    options: string[]
    correct_option: number
  }>
  is_owner: boolean
  author: string
  created_at: string
}

interface CreateForm {
  name: string
  description: string
  max_score_per_question: number
}

const quizzes = ref<Quiz[]>([])
const searchTerm = ref('')
const filterType = ref<'all' | 'mine' | 'public'>('all')
const showCreateModal = ref(false)
const createForm = ref<CreateForm>({ name: '', description: '', max_score_per_question: 1 })
const creatingQuiz = ref(false)

const currentQuiz = ref<Quiz | null>(null)
const quizStarted = ref(false)
const currentQuestionIndex = ref(0)
const answers = ref<number[]>([])
const score = ref(0)
const correctAnswers = ref(0)
const totalQuestions = ref(0)
const circumference = 2 * Math.PI * 85
const progress = ref(0)

const filteredQuizzes = computed(() => {
  return quizzes.value.filter(quiz => {
    const matchesSearch = quiz.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
                          quiz.description.toLowerCase().includes(searchTerm.value.toLowerCase())
    const matchesFilter = filterType.value === 'all' || 
                          (filterType.value === 'mine' && quiz.is_owner) ||
                          (filterType.value === 'public' && !quiz.is_owner)
    return matchesSearch && matchesFilter
  })
})

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('es-ES', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

const scoreText = computed(() => {
  if (score.value >= 9) return '¡Excelente!'
  if (score.value >= 7) return 'Muy bien'
  if (score.value >= 5) return 'Bien'
  if (score.value >= 3) return 'En progreso'
  return 'Sigue practicando'
})

const loadQuizzes = async () => {
  try {
    const response = await api.get('/knowtionaries/')
    quizzes.value = response.data
  } catch (error) {
    console.error('Error loading quizzes:', error)
  }
}

const createQuiz = async () => {
  creatingQuiz.value = true
  try {
    const data = new FormData()
    data.append('name', createForm.value.name)
    data.append('description', createForm.value.description)
    data.append('max_score_per_question', createForm.value.max_score_per_question.toString())
    
    await api.post('/knowtionaries/add/', data)
    await loadQuizzes()
    closeCreateModal()
  } catch (error) {
    console.error('Error creating quiz:', error)
  } finally {
    creatingQuiz.value = false
  }
}

const closeCreateModal = () => {
  createForm.value = { name: '', description: '', max_score_per_question: 1 }
  showCreateModal.value = false
}

const openQuiz = (quiz: Quiz) => {
  currentQuiz.value = quiz
  currentQuestionIndex.value = 0
  answers.value = []
  quizStarted.value = false
}

const closeQuiz = () => {
  currentQuiz.value = null
  quizStarted.value = false
  answers.value = []
  currentQuestionIndex.value = 0
}

const startQuiz = () => {
  quizStarted.value = true
  totalQuestions.value = currentQuiz.value.questions.length
  answers.value = new Array(totalQuestions.value).fill(-1)
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < currentQuiz.value.questions.length - 1) {
    currentQuestionIndex.value++
  }
}

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
  }
}

const restartQuiz = () => {
  currentQuestionIndex.value = 0
  answers.value = []
  quizStarted.value = true
}

const calculateScore = () => {
  let totalScore = 0
  let correct = 0
  
  currentQuiz.value.questions.forEach((q, index) => {
    if (answers.value[index] === q.correct_option) {
      totalScore += currentQuiz.value.max_score_per_question || 1
      correct++
    }
  })
  
  score.value = Math.round((totalScore / (currentQuiz.value.questions.length * (currentQuiz.value.max_score_per_question || 1))) * 10)
  correctAnswers.value = correct
  progress.value = (score.value / 10) * 100
}

onMounted(() => {
  loadQuizzes()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
</style>

