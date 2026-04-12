<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="bg-white rounded-2xl shadow-lg p-8 mb-8">
        <div class="flex items-start space-x-6">
          <div class="w-24 h-24 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center flex-shrink-0">
            <span class="text-3xl font-bold text-white">M</span>
          </div>
          <div class="flex-1 min-w-0">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Matemáticas Avanzadas</h1>
            <p class="text-xl text-gray-600 mb-4">Álgebra lineal, cálculo, estadística y más</p>
            <div class="flex items-center space-x-6 text-sm">
              <span class="flex items-center text-gray-500">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                Creada hace 3 días
              </span>
              <span class="flex items-center text-gray-500">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                </svg>
                25 elementos
              </span>
            </div>
          </div>
          <div class="flex flex-col space-y-3">
            <button class="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-xl hover:shadow-xl transition-all font-semibold">
              Editar librería
            </button>
            <button class="bg-red-100 text-red-700 px-6 py-3 rounded-xl hover:bg-red-200 transition-all font-semibold">
              Eliminar
            </button>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden mb-8">
        <div class="border-b border-gray-200">
          <nav class="flex space-x-8 px-6">
            <button @click="activeTab = 'flashcards'" :class="activeTab === 'flashcards' ? 'border-purple-500 text-purple-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'" class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors">
              Flashcards (12)
            </button>
            <button @click="activeTab = 'notes'" :class="activeTab === 'notes' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'" class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors">
              Notas (5)
            </button>
            <button @click="activeTab = 'knowtionaries'" :class="activeTab === 'knowtionaries' ? 'border-green-500 text-green-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'" class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors">
              Cuestionarios (3)
            </button>
          </nav>
        </div>

        <!-- Flashcards Tab -->
        <div v-if="activeTab === 'flashcards'" class="p-6">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900">Flashcards</h2>
            <button class="bg-gradient-to-r from-emerald-600 to-teal-600 text-white px-6 py-2.5 rounded-xl hover:shadow-xl transition-all font-semibold">
              + Nueva flashcard
            </button>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="card in flashcards" :key="card.id" class="group cursor-pointer p-6 border border-gray-200 rounded-xl hover:border-purple-300 hover:shadow-lg transition-all hover:-translate-y-1">
              <h3 class="font-bold text-lg text-gray-900 mb-2 line-clamp-1 group-hover:text-purple-600">{{ card.term }}</h3>
              <p class="text-gray-600 mb-4 line-clamp-2">{{ card.definition }}</p>
              <button class="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-2 px-4 rounded-lg text-sm hover:shadow-md transition-all">
                Estudiar →
              </button>
            </div>
          </div>
        </div>

        <!-- Notas Tab -->
        <div v-if="activeTab === 'notes'" class="p-6">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900">Notas</h2>
            <button class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-2.5 rounded-xl hover:shadow-xl transition-all font-semibold">
              + Nueva nota
            </button>
          </div>
          <div class="space-y-4">
            <div v-for="note in notes" :key="note.id" class="p-6 border border-gray-200 rounded-xl hover:shadow-lg transition-all">
              <h3 class="font-bold text-xl text-gray-900 mb-2 line-clamp-1">{{ note.title }}</h3>
              <p class="text-gray-600 line-clamp-3">{{ note.content }}</p>
            </div>
          </div>
        </div>

        <!-- Cuestionarios Tab -->
        <div v-if="activeTab === 'knowtionaries'" class="p-6">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900">Cuestionarios</h2>
            <button class="bg-gradient-to-r from-green-600 to-emerald-600 text-white px-6 py-2.5 rounded-xl hover:shadow-xl transition-all font-semibold">
              + Nuevo cuestionario
            </button>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div v-for="quiz in knowtionaries" :key="quiz.id" class="p-6 border border-gray-200 rounded-xl hover:shadow-lg transition-all">
              <h3 class="font-bold text-lg text-gray-900 mb-3 line-clamp-2">{{ quiz.title }}</h3>
              <p class="text-sm text-gray-600 mb-4">{{ quiz.description }}</p>
              <div class="flex items-center space-x-4 text-xs">
                <span class="px-2.5 py-1 bg-green-100 text-green-800 rounded-full">{{ quiz.questions.length }} preguntas</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <footer class="mt-16 pt-12 pb-8 border-t border-gray-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p class="text-gray-500 text-sm">&copy; 2024 KnowFlow. Tu plataforma de estudio interactivo.</p>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeTab = ref('flashcards')

const flashcards = ref([
  { id: 1, term: 'Matrices', definition: 'Arreglo rectangular de números' },
  { id: 2, term: 'Determinante', definition: 'Función que asigna escalar a matriz cuadrada' },
  { id: 3, term: 'Vector propio', definition: 'Vector que se multiplica por escalar bajo transformación lineal' }
])

const notes = ref([
  { id: 1, title: 'Teorema fundamental del cálculo', content: 'La derivada e integral son inversas...' },
  { id: 2, title: 'Teorema de Pitágoras', content: 'En triángulo rectángulo a² + b² = c²...' }
])

const knowtionaries = ref([
  { id: 1, title: 'Quiz Álgebra Lineal', description: '10 preguntas básicas', questions: [1,2,3] },
  { id: 2, title: 'Prueba Cálculo', description: 'Conceptos fundamentales', questions: [1,2] }
])
</script>

<style scoped>
.line-clamp-1 { @apply overflow-hidden truncate; }
.line-clamp-2 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.line-clamp-3 { display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
</style>

