<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-8">
        <div>
          <h1 class="text-4xl font-bold text-gray-900 mb-2">Cuestionarios</h1>
          <p class="text-xl text-gray-600">Practica con preguntas interactivas</p>
        </div>
        <Button @click="showCreateModal = true" class="w-full lg:w-auto">
          + Nuevo Cuestionario
        </Button>
      </div>

      <!-- Cuestionaries Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="quiz in knowtionaries" 
          :key="quiz.id"
          class="card overflow-hidden hover:shadow-2xl group cursor-pointer transition-all p-8"
          @click="startQuiz(quiz.id)"
        >
          <div class="text-center">
            <div class="w-20 h-20 bg-gradient-to-br from-orange-400 to-red-400 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform">
              <span class="text-2xl font-bold text-white">❓</span>
            </div>
            <h3 class="font-bold text-2xl text-gray-900 mb-3 line-clamp-2 group-hover:text-orange-600">{{ quiz.title }}</h3>
            <div class="space-y-1 mb-6">
              <div class="flex items-center justify-between text-sm">
                <span class="text-gray-600">Preguntas</span>
                <span class="font-semibold text-gray-900">{{ quiz.questions.length }}</span>
              </div>
            </div>
            <div class="flex items-center justify-center pt-4 border-t border-gray-100">
              <Button variant="outline" size="sm" @click.stop="editQuiz(quiz)" class="mr-2">Editar</Button>
              <Button size="sm" @click.stop="startQuiz(quiz.id)">Practicar</Button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!knowtionaries.length" class="col-span-full flex flex-col items-center justify-center py-24 text-center border-2 border-dashed border-gray-200 rounded-3xl">
          <div class="w-28 h-28 bg-gradient-to-br from-orange-100 to-yellow-100 rounded-3xl flex items-center justify-center mb-8 p-6">
            <svg class="w-14 h-14 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">No tienes cuestionarios</h3>
          <p class="text-gray-600 mb-6 max-w-md">Crea cuestionarios para practicar y reforzar conocimientos.</p>
          <Button @click="showCreateModal = true" class="px-8 py-3 text-lg">Crear cuestionario</Button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-3xl shadow-2xl max-w-2xl w-full">
        <div class="p-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">{{ editingQuiz ? 'Editar Cuestionario' : 'Nuevo Cuestionario' }}</h2>
          <form @submit.prevent="saveQuiz" class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Título *</label>
              <input
                v-model="form.title"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500"
              />
            </div>
            <div>
              <h4 class="text-lg font-semibold text-gray-900 mb-4">Preguntas</h4>
              <div v-for="(question, index) in form.questions" :key="index" class="border border-gray-200 rounded-xl p-4 mb-4 hover:border-orange-300 transition-colors">
                <div class="flex gap-3 mb-3">
                  <input v-model="question.question" :placeholder="`Pregunta ${index + 1}`" class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500" />
                  <Button type="button" size="sm" variant="danger" @click="removeQuestion(index)">Eliminar</Button>
                </div>
                <input v-model="question.answer" placeholder="Respuesta correcta" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 mb-2" />
                <select v-model="question.type" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500">
                  <option value="text">Respuesta libre</option>
                  <option value="multiple">Múltiple choice</option>
                </select>
              </div>
              <Button type="button" variant="outline" @click="addQuestion" class="w-full">+ Añadir pregunta</Button>
            </div>
            <div class="flex space-x-3">
              <Button type="submit" :loading="saving" class="flex-1">Guardar</Button>
              <Button type="button" variant="secondary" @click="closeModal" class="flex-1">Cancelar</Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import Button from '@/components/Button.vue'
import { knowtionaryService } from '@/services/api'
import type { Knowtionary } from '@/types/index'

const router = useRouter()
const knowtionaries = ref<Knowtionary[]>([])
const showCreateModal = ref(false)
const editingQuiz = ref<Knowtionary | null>(null)
const form = ref({
  title: '',
  questions: [
    { question: '', answer: '', type: 'text' as const }
  ]
})
const saving = ref(false)

const loadKnowtionaries = async () => {
  try {
    const response = await knowtionaryService.getAll()
    knowtionaries.value = response.data
  } catch (error) {
    console.error('Error loading knowtionaries:', error)
  }
}

const startQuiz = (id: number) => {
  router.push(`/knowtionaries/quiz/${id}`)
}

const editQuiz = (quiz: Knowtionary) => {
  editingQuiz.value = quiz
  form.value = { ...quiz }
  showCreateModal.value = true
}

const closeModal = () => {
  showCreateModal.value = false
  editingQuiz.value = null
  form.value = {
    title: '',
    questions: [{ question: '', answer: '', type: 'text' }]
  }
}

const addQuestion = () => {
  form.value.questions.push({ question: '', answer: '', type: 'text' })
}

const removeQuestion = (index: number) => {
  form.value.questions.splice(index, 1)
}

const saveQuiz = async () => {
  saving.value = true
  try {
    if (editingQuiz.value) {
      await knowtionaryService.update(editingQuiz.value.id.toString(), form.value)
    } else {
      await knowtionaryService.create(form.value)
    }
    closeModal()
    loadKnowtionaries()
  } catch (error) {
    console.error('Error saving quiz:', error)
  } finally {
    saving.value = false
  }
}

onMounted(loadKnowtionaries)
</script>
