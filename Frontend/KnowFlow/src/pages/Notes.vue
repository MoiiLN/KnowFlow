<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center mb-12">
        <div>
          <h1 class="text-4xl font-black text-gray-900 dark:text-white mb-2 tracking-tight">Notes</h1>
          <p class="text-xl text-gray-500 dark:text-gray-400 font-medium mt-2">Tus apuntes organizados e inteligentes</p>
        </div>
        <button @click="showModal = true" class="bg-indigo-600 text-white px-8 py-3 rounded-xl hover:bg-indigo-700 font-semibold shadow-lg hover:shadow-xl transition-all">
          + Nueva Nota
        </button>
      </div>

      <!-- Search -->
      <div class="mb-8">
        <div class="relative max-w-md">
          <input 
            v-model="searchTerm" 
            type="text" 
            placeholder="Buscar notas..."
            class="w-full pl-12 pr-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 dark:text-white transition-all"
          >
          <svg class="w-5 h-5 text-gray-400 absolute left-4 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="note in filteredNotes" :key="note.id" class="group">
          <div class="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg hover:shadow-2xl hover:-translate-y-2 transition-all cursor-pointer h-full border border-gray-100 dark:border-gray-700 hover:border-indigo-200 dark:hover:border-indigo-500" @click="editNote(note)">
            <div class="flex items-start justify-between mb-6">
              <div class="flex items-center space-x-3">
                <div class="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5.25M2 19V5a2 2 0 012-2h5.25" />
                  </svg>
                </div>
                <div>
                  <h3 class="font-bold text-xl text-gray-900 group-hover:text-indigo-600 transition-colors line-clamp-1">{{ note.title }}</h3>
                  <p class="text-sm text-gray-500">{{ formatDate(note.created_at) }}</p>
                </div>
              </div>
            </div>
            <p class="text-gray-700 dark:text-gray-300 leading-relaxed line-clamp-3 h-20">{{ note.text }}</p>
            <div class="mt-6 flex items-center space-x-4 text-sm text-gray-500">
              <span v-if="note.file">📎 Archivo adjunto</span>
            </div>
          </div>
        </div>

        <div v-if="filteredNotes.length === 0" class="col-span-full flex flex-col items-center justify-center py-24 border-2 border-dashed border-gray-300 rounded-3xl">
          <div class="w-24 h-24 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-3xl flex items-center justify-center mb-6">
            <svg class="w-12 h-12 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">{{ searchTerm ? 'Sin resultados' : 'Sin notas' }}</h3>
          <p class="text-gray-600 mb-6">Empieza creando tu primera nota</p>
          <button @click="showModal = true" class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-8 py-4 rounded-2xl font-semibold shadow-xl hover:shadow-2xl">
            + Nueva nota
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Create/Edit -->
    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-6">
      <div class="bg-white rounded-3xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-8">
          <div class="flex items-center justify-between mb-8">
            <h2 class="text-2xl font-bold text-gray-900">{{ editing ? 'Editar' : 'Nueva' }} Nota</h2>
            <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <form @submit.prevent="saveNote">
            <div class="mb-6">
              <label class="block text-sm font-semibold text-gray-700 mb-3">Título</label>
              <input v-model="form.title" required type="text" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500">
            </div>
            <div class="mb-6">
              <label class="block text-sm font-semibold text-gray-700 mb-3">Contenido</label>
              <textarea v-model="form.content" rows="12" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-vertical min-h-[200px]"></textarea>
            </div>
            <div class="mb-8">
              <label class="block text-sm font-semibold text-gray-700 mb-3">Archivo (opcional)</label>
              <input type="file" @change="handleFile" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500">
            </div>
            <div class="flex gap-3 justify-end">
              <button type="button" @click="closeModal" class="px-8 py-3 bg-gray-200 text-gray-800 rounded-xl font-semibold hover:bg-gray-300">
                Cancelar
              </button>
              <button type="submit" :disabled="saving" class="px-8 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold hover:shadow-xl disabled:opacity-50">
                {{ saving ? 'Guardando...' : 'Guardar Nota' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import api from '@/services/api'

const router = useRouter()
const notes = ref([])
const searchTerm = ref('')
const showModal = ref(false)
const editing = ref(null)
const form = ref({ title: '', content: '' })
const saving = ref(false)
const file = ref(null)

const filteredNotes = computed(() => {
  if (!searchTerm.value) return notes.value
  return notes.value.filter(note => 
    note.title.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    note.content.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

const formatDate = (dateString) => new Date(dateString).toLocaleDateString('es-ES')

const loadNotes = async () => {
  try {
    const response = await api.get('notes/')
    notes.value = response.data
  } catch (error) {
    console.error('Error loading notes:', error)
  }
}

const closeModal = () => {
  editing.value = null
  form.value = { title: '', content: '' }
  file.value = null
  showModal.value = false
}

const editNote = (note) => {
  editing.value = note.slug
  form.value = { title: note.title, content: note.content }
  showModal.value = true
}

const handleFile = (event) => {
  file.value = event.target.files[0]
}

const saveNote = async () => {
  saving.value = true
  try {
    const data = new FormData()
    data.append('title', form.value.title)
    data.append('content', form.value.content)
    if (file.value) data.append('file', file.value)
    
    if (editing.value) {
      await api.post(`/notes/edit/${editing.value}/`, data)
    } else {
      data.append('library_content_id', '1') // Mock - cambia por ID real
      data.append('slug', form.value.title.toLowerCase().replace(/\s+/g, '-').substring(0, 50))
      await api.post('notes/add/', data)
    }
    
    await loadNotes()
    closeModal()
  } catch (error) {
    console.error('Error saving note:', error)
    alert('Error al guardar nota')
  } finally {
    saving.value = false
  }
}

onMounted(loadNotes)
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
