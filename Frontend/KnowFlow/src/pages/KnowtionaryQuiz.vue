<template>
  <DefaultLayout>
    <div class="max-w-2xl mx-auto">
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">{{ quiz.title }}</h1>
        <div class="text-2xl text-gray-600 mb-8">Pregunta {{ currentQuestionIndex + 1 }} de {{ quiz.questions.length }}</div>
      </div>
      
      <!-- Question -->
      <div class="card p-8 mb-12">
        <div class="mb-8 p-6 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-2xl">
          <p class="text-2xl font-semibold text-gray-900">{{ currentQuestion.question }}</p>
        </div>
        
        <div v-if="currentQuestion.type === 'text'" class="space-y-4">
          <textarea
            v-model="answer"
            rows="4"
            class="w-full px-4 py-4 border-2 border-gray-200 rounded-2xl focus:border-primary-400 focus:ring-4 focus:ring-primary-100 resize-vertical text-lg"
            placeholder="Escribe tu respuesta..."
          ></textarea>
        </div>
        
        <div v-else class="space-y-3">
          <label v-for="(option, index) in ['A', 'B', 'C', 'D']" :key="index" class="flex items-center p-4 border-2 border-gray-200 rounded-xl hover:border-primary-300 hover:bg-primary-50 cursor-pointer transition-all group">
            <input type="radio" class="sr-only" :value="option" v-model="answer" />
            <svg class="w-5 h-5 text-primary-600 mr-3 group-hover:scale-110 transition-transform" fill="currentColor" viewBox="0 0 20 20" v-if="answer === option">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            <svg class="w-5 h-5 text-gray-400 mr-3" fill="none" viewBox="0 0 24 24" v-else stroke="currentColor">
              <circle cx="12" cy="12" r="10" stroke-width="2"></circle>
            </svg>
            <span class="font-medium text-lg text-gray-900 group-hover:text-primary-600">{{ option }}. Opción</span>
          </label>
        </div>
        
        <div class="flex space-x-4 mt-8">
          <Button v-if="currentQuestionIndex > 0" @click="previousQuestion" variant="outline" class="flex-1">Anterior</Button>
          <Button 
            :loading="submitting" 
            @click="submitAnswer" 
            :disabled="!answer.trim()" 
            class="flex-1"
            class="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700"
          >
            {{ currentQuestionIndex === quiz.questions.length - 1 ? 'Finalizar' : 'Siguiente' }}
          </Button>
        </div>
      </div>
      
      <!-- Results -->
      <div v-if="showResults" class="space-y-6">
        <div class="card p-8 text-center">
          <div class="w-24 h-24 bg-gradient-to-br from-green-400 to-emerald-500 rounded-3xl flex items-center justify-center mx-auto mb-6">
            <svg class="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
          </div>
          <h2 class="text-3xl font-bold text-gray-900 mb-4">¡Cuestionario completado!</h2>
          <div class="text-5xl font-bold text-green-600 mb-4">{{ score }}%</div>
          <p class="text-xl text-gray-600 mb-8">Has acertado {{ correctAnswers.length }} de {{ quiz.questions.length }} preguntas</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-3">
            <h3 class="font-bold text-lg text-gray-900">✅ Respuestas correctas</h3>
            <div v-for="(q, i) in correctAnswers" :key="i" class="p-4 bg-green-50 border border-green-200 rounded-xl">
              <span class="font-semibold">Pregunta {{ i + 1 }}</span>
            </div>
          </div>
          <div class="space-y-3">
            <h3 class="font-bold text-lg text-gray-900">❌ Respuestas incorrectas</h3>
            <div v-for="(q, i) in incorrectAnswers" :key="i" class="p-4 bg-red-50 border border-red-200 rounded-xl">
              <span class="font-semibold">Pregunta {{ i + 1 }}</span>
              <div class="text-sm text-red-800 mt-1">Respuesta: {{ q }}</div>
            </div>
          </div>
        </div>
        
        <div class="flex flex-col sm:flex-row gap-4 pt-8 border-t border-gray-200 mt-12">
          <Button @click="restartQuiz" class="flex-1">Repetir</Button>
          <Button @click="backToList" variant="outline" class="flex-1">Volver</Button>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import Button from '@/components/Button.vue'

const route = useRoute()
const quiz = ref({
  title: 'Mi Cuestionario',
  questions: [
    { question: 'Pregunta 1?', answer: 'Respuesta 1', type: 'text' },
    { question: 'Pregunta 2?', answer: 'Respuesta 2', type: 'multiple' }
  ]
})
const currentQuestionIndex = ref(0)
const answer = ref('')
const answers = ref<string[]>([])
const showResults = ref(false)
const submitting = ref(false)
const correctAnswers = ref<number[]>([])
const incorrectAnswers = ref<{index: number, userAnswer: string}[]>([])

const currentQuestion = computed(() => quiz.value.questions[currentQuestionIndex.value])

const score = computed(() => Math.round((correctAnswers.value.length / quiz.value.questions.length) * 100))

const submitAnswer = async () => {
  submitting.value = true
  answers.value[currentQuestionIndex.value] = answer.value
  await new Promise(resolve => setTimeout(resolve, 500))
  
  if (answer.value.toLowerCase().trim() === currentQuestion.value.answer.toLowerCase().trim()) {
    correctAnswers.value.push(currentQuestionIndex.value)
  } else {
    incorrectAnswers.value.push({ index: currentQuestionIndex.value, userAnswer: answer.value })
  }
  
  submitting.value = false
  
  if (currentQuestionIndex.value < quiz.value.questions.length - 1) {
    nextQuestion()
  } else {
    showResults.value = true
  }
}

const nextQuestion = () => {
  currentQuestionIndex.value++
  answer.value = ''
}

const previousQuestion = () => {
  currentQuestionIndex.value--
  answer.value = answers.value[currentQuestionIndex.value] || ''
}

const restartQuiz = () => {
  currentQuestionIndex.value = 0
  answer.value = ''
  answers.value = []
  showResults.value = false
  correctAnswers.value = []
  incorrectAnswers.value = []
}

const backToList = () => {
  // router.push('/knowtionaries')
  window.history.back()
}
</script>
