<template>
  <DefaultLayout>
    <div class="max-w-4xl mx-auto">
      <!-- Library Header -->
      <div class="card mb-12 p-8 text-center">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">{{ library.name }}</h1>
        <p class="text-xl text-gray-600 mb-8">{{ library.description }}</p>
        <div class="flex items-center justify-center space-x-6 text-sm text-gray-500">
          <span>{{ library.contents }} elementos</span>
          <span>Creada {{ formatDate(library.created_at) }}</span>
        </div>
      </div>

      <!-- Content Tabs -->
      <div class="card p-6 mb-8">
        <nav class="flex space-x-1 border-b border-gray-200">
          <button 
            v-for="tab in tabs" 
            :key="tab.key"
            @click="activeTab = tab.key"
            class="px-6 py-3 font-medium text-sm transition-colors"
            :class="activeTab === tab.key ? 'border-primary-500 text-primary-600 border-b-2' : 'text-gray-500 hover:text-gray-700 border-b'"
          >
            {{ tab.label }}
          </button>
        </nav>
        <div class="mt-6">
          <!-- Flashcards tab -->
          <div v-if="activeTab === 'flowcards'">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="card in libraryContents.flowcards" :key="card.slug" class="group cursor-pointer p-6 border rounded-xl hover:shadow-lg hover:border-primary-300 transition-all">
                <h4 class="font-semibold text-gray-900 mb-2 line-clamp-1">{{ card.term }}</h4>
                <p class="text-gray-600 text-sm line-clamp-2">{{ card.definition }}</p>
              </div>
            </div>
          </div>
          
          <!-- Notes tab -->
          <div v-if="activeTab === 'notes'">
            <div class="space-y-4">
              <div v-for="note in libraryContents.notes" :key="note.slug" class="p-6 border rounded-xl hover:shadow-lg transition-all">
                <h4 class="font-semibold text-gray-900 mb-2">{{ note.title }}</h4>
                <p class="text-gray-600 line-clamp-3">{{ note.content }}</p>
              </div>
            </div>
          </div>
          
          <!-- Knowtionaries tab -->
          <div v-if="activeTab === 'knowtionaries'">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div v-for="quiz in libraryContents.knowtionaries" :key="quiz.id" class="p-6 border rounded-xl hover:shadow-lg transition-all">
                <h4 class="font-semibold text-gray-900 mb-2">{{ quiz.title }}</h4>
                <p class="text-gray-600 text-sm">{{ quiz.questions.length }} preguntas</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

const route = useRoute()
const library = ref({ name: '', description: '', contents: 0, created_at: '' })
const libraryContents = ref({ flowcards: [], notes: [], knowtionaries: [] })
const activeTab = ref('flowcards')

const tabs = [
  { key: 'flowcards', label: 'Flashcards' },
  { key: 'notes', label: 'Notas' },
  { key: 'knowtionaries', label: 'Cuestionarios' }
]

const loadLibrary = async () => {
  const id = route.params.id
  // Load library details and contents
  library.value = { name: 'Mi Primera Librería', description: 'Contenido de estudio', contents: 12, created_at: new Date().toISOString() }
  // libraryContents.value populated from API
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('es-ES')
}

onMounted(loadLibrary)
</script>
