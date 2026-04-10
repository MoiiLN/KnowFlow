<template>
  <DefaultLayout>
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-8">
        <div>
          <h1 class="text-4xl font-bold text-gray-900 mb-2">Notas</h1>
          <p class="text-xl text-gray-600">Tus apuntes organizados y fáciles de encontrar</p>
        </div>
        <Button @click="showCreateModal = true" class="w-full lg:w-auto">
          + Nueva Nota
        </Button>
      </div>

      <!-- Search -->
      <div class="card mb-8 p-6">
        <input
          v-model="searchTerm"
          @input="filterNotes"
          placeholder="Buscar notas por título o contenido..."
          class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent text-lg"
        />
      </div>

      <!-- Notes List -->
      <div v-if="filteredNotes.length" class="space-y-4">
        <div 
          v-for="note in filteredNotes" 
          :key="note.slug"
          class="card hover:shadow-xl group cursor-pointer transition-all p-6"
          @click="goToNote(note.slug)"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1 pr-4">
              <h3 class="font-bold text-xl text-gray-900 mb-2 line-clamp-1 group-hover:text-primary-600">{{ note.title }}</h3>
              <p class="text-gray-600 line-clamp-3 mb-4 leading-relaxed">{{ note.content }}</p>
              <div class="flex items-center text-sm text-gray-500 space-x-4">
                <span>{{ formatDate(note.created_at) }}</span>
                <span v-if="note.library">📚 Librería</span>
              </div>
            </div>
            <div class="flex-shrink-0 ml-4">
              <div class="w-2 h-20 bg-gradient-to-b from-primary-400 to-primary-600 rounded-full opacity-75 group-hover:opacity-100 transition-opacity"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-24 border-2 border-dashed border-gray-200 rounded-3xl">
        <div class="w-24 h-24 bg-gradient-to-r from-yellow-100 to-orange-100 rounded-3xl flex items-center justify-center mx-auto mb-6 p-4">
          <svg class="w-12 h-12 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
        </div>
        <h3 class="text-2xl font-bold text-gray-900 mb-2">{{ searchTerm ? 'No se encontraron notas' : 'No tienes notas' }}</h3>
        <p class="text-gray-600 mb-6 max-w-md mx-auto">{{ searchTerm ? 'Prueba con otras palabras clave.' : 'Crea tu primera nota para empezar a tomar apuntes.' }}</p>
        <Button @click="showCreateModal = true" class="px-8 py-3 text-lg">Nueva nota</Button>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-2xl max-h-[90vh]">
        <div class="p-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">{{ editingNote ? 'Editar Nota' : 'Nueva Nota' }}</h2>
          <form @submit.prevent="saveNote" class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Título *</label>
              <input
                v-model="form.title"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 text-lg font-semibold"
                placeholder="Título de tu nota"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Contenido *</label>
              <textarea
                v-model="form.content"
                required
                rows="15"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 font-medium text-lg leading-relaxed resize-vertical min-h-[200px]"
                placeholder="Escribe aquí tu contenido..."
              ></textarea>
            </div>
            <div class="flex space-x-3">
              <Button type="submit" :loading="saving" class="flex-1">Guardar Nota</Button>
              <Button type="button" variant="secondary" @click="closeModal" class="flex-1">Cancelar</Button>
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
import Button from '@/components/Button.vue'
import { noteService } from '@/services/api'
import type { Note } from '@/types/index'

const router = useRouter()
const notes = ref<Note[]>([])
const filteredNotes = ref<Note[]>([])
const searchTerm = ref('')
const showCreateModal = ref(false)
const editingNote = ref<Note | null>(null)
const form = ref({ title: '', content: '' })
const saving = ref(false)

const loadNotes = async () => {
  try {
    const response = await noteService.getAll()
    notes.value = response.data
    filteredNotes.value = notes.value
  } catch (error) {
    console.error('Error loading notes:', error)
  }
}

const filterNotes = () => {
  if (!searchTerm.value) {
    filteredNotes.value = notes.value
    return
  }
  filteredNotes.value = notes.value.filter(note =>
    note.title.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    note.content.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
}

const goToNote = (slug: string) => {
  router.push(`/notes/${slug}`)
}

const editNote = (note: Note) => {
  editingNote.value = note
  form.value = { title: note.title, content: note.content }
  showCreateModal.value = true
}

const closeModal = () => {
  showCreateModal.value = false
  editingNote.value = null
  form.value = { title: '', content: '' }
}

const saveNote = async () => {
  saving.value = true
  try {
    if (editingNote.value) {
      await noteService.update(editingNote.value.slug, form.value)
    } else {
      await noteService.create(form.value)
    }
    closeModal()
    loadNotes()
  } catch (error) {
    console.error('Error saving note:', error)
  } finally {
    saving.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('es-ES', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
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
