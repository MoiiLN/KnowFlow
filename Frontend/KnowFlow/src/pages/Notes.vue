<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center mb-12">
        <div>
          <h1 class="text-4xl font-black text-gray-900 dark:text-white mb-2 tracking-tight">Notes</h1>
          <p class="text-xl text-gray-500 dark:text-gray-400 font-medium mt-2">Tus apuntes organizados e inteligentes</p>
        </div>
        <button @click="showModal = true" class="bg-indigo-600 text-white px-8 py-3 rounded-xl hover:bg-indigo-700 font-semibold shadow-lg hover:shadow-xl transition-all">
          + Nueva Nota
        </button>
      </div>

      <!-- Search + Filter -->
      <div class="mb-8 flex flex-wrap gap-4 items-center">
        <div class="relative flex-1 min-w-[200px] max-w-md">
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
        <button
          @click="showOnlyFavorites = !showOnlyFavorites"
          :class="[
            'flex items-center gap-2 px-5 py-3 rounded-xl font-bold text-sm transition-all',
            showOnlyFavorites
              ? 'bg-amber-400 text-white shadow-lg shadow-amber-300/40'
              : 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 hover:bg-amber-50 dark:hover:bg-amber-900/20 hover:text-amber-500'
          ]"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
          </svg>
          Favoritas
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="note in filteredNotes" :key="note.id" class="group">
          <div
            class="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg hover:shadow-2xl hover:-translate-y-2 transition-all h-full border dark:border-gray-700 hover:border-indigo-200 dark:hover:border-indigo-500 flex flex-col"
            :class="note.favorite ? 'border-amber-200 dark:border-amber-700/40' : 'border-gray-100'"
          >
            <!-- Card Header -->
            <div class="flex items-start justify-between mb-6">
              <div class="flex items-center space-x-3 cursor-pointer flex-1 min-w-0" @click="editNote(note)">
                <div class="w-12 h-12 flex-shrink-0 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center">
                  <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5.25M2 19V5a2 2 0 012-2h5.25" />
                  </svg>
                </div>
                <div class="min-w-0">
                  <h3 class="font-bold text-xl text-gray-900 dark:text-white group-hover:text-indigo-600 transition-colors line-clamp-1">{{ note.title }}</h3>
                  <p class="text-sm text-gray-500">{{ formatDate(note.created_at) }}</p>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="flex items-center gap-1 ml-2 flex-shrink-0">
                <!-- Favorite -->
                <button
                  @click.stop="toggleFavorite(note)"
                  :title="note.favorite ? 'Quitar de favoritos' : 'Añadir a favoritos'"
                  :class="[
                    'p-2 rounded-xl transition-all duration-200',
                    note.favorite
                      ? 'text-amber-400 hover:text-amber-500 hover:bg-amber-50 dark:hover:bg-amber-900/20'
                      : 'text-gray-300 hover:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-900/20'
                  ]"
                >
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                  </svg>
                </button>

                <!-- Delete (double-click confirm) -->
                <button
                  @click.stop="deleteNote(note)"
                  :title="confirmingDelete === note.id ? 'Confirmar eliminación' : 'Eliminar nota'"
                  :class="[
                    'p-2 rounded-xl transition-all duration-300',
                    confirmingDelete === note.id
                      ? 'bg-red-500 text-white shadow-lg scale-110 animate-pulse'
                      : 'text-gray-300 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20'
                  ]"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path v-if="confirmingDelete !== note.id" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- Content -->
            <p class="text-gray-700 dark:text-gray-300 leading-relaxed line-clamp-3 flex-1 cursor-pointer" @click="editNote(note)">{{ note.text }}</p>
            <div class="mt-4 flex items-center text-sm text-gray-400">
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
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">{{ showOnlyFavorites ? 'Sin notas favoritas' : (searchTerm ? 'Sin resultados' : 'Sin notas') }}</h3>
          <p class="text-gray-600 dark:text-gray-400 mb-6">{{ showOnlyFavorites ? 'Marca notas con ⭐ para verlas aquí' : 'Empieza creando tu primera nota' }}</p>
          <button v-if="!showOnlyFavorites" @click="showModal = true" class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-8 py-4 rounded-2xl font-semibold shadow-xl hover:shadow-2xl">
            + Nueva nota
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Create/Edit -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-6 overflow-y-auto">
      <div class="fixed inset-0 bg-gray-900/60 backdrop-blur-md transition-opacity" @click="closeModal"></div>
      
      <div class="relative bg-white dark:bg-gray-800 rounded-[3rem] shadow-2xl w-full max-w-2xl overflow-hidden animate-in fade-in zoom-in duration-300 border border-gray-100 dark:border-gray-700">
        <div class="p-10 md:p-12">
          <div class="flex items-center justify-between mb-10">
            <div>
              <h2 class="text-3xl font-black text-gray-900 dark:text-white tracking-tight">{{ editing ? 'Editar' : 'Nueva' }} Nota</h2>
              <p class="text-gray-500 dark:text-gray-400 font-medium">Captura tus ideas e información importante.</p>
            </div>
            <button @click="closeModal" class="p-3 bg-gray-100 dark:bg-gray-900 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 rounded-2xl transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit.prevent="saveNote" class="space-y-8">
            <div class="space-y-2">
              <label class="text-xs font-black text-gray-400 dark:text-gray-500 uppercase tracking-widest ml-1">Título de la nota</label>
              <input v-model="form.title" required type="text" placeholder="Ej: Resumen de Biología Molecular"
                class="w-full px-6 py-4 bg-gray-50 dark:bg-gray-900 border border-transparent dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white dark:focus:bg-gray-800 dark:text-white transition-all outline-none font-bold text-lg"
              >
            </div>

            <div class="space-y-2">
              <label class="text-xs font-black text-gray-400 dark:text-gray-500 uppercase tracking-widest ml-1">Contenido de la nota</label>
              <textarea v-model="form.content" rows="10" placeholder="Escribe aquí tus apuntes..."
                class="w-full px-6 py-4 bg-gray-50 dark:bg-gray-900 border border-transparent dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white dark:focus:bg-gray-800 dark:text-white transition-all outline-none font-medium resize-none min-h-[300px]"
              ></textarea>
            </div>

            <div class="space-y-3">
              <label class="text-xs font-black text-gray-400 dark:text-gray-500 uppercase tracking-widest ml-1">Archivo adjunto (opcional)</label>
              <div class="relative group">
                <input type="file" @change="handleFile" 
                  class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                >
                <div class="w-full px-6 py-8 border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-[2rem] flex flex-col items-center justify-center group-hover:border-indigo-400 dark:group-hover:border-indigo-500 transition-colors">
                  <div class="w-12 h-12 bg-gray-100 dark:bg-gray-900 rounded-xl flex items-center justify-center mb-3 text-gray-400 group-hover:text-indigo-500 transition-colors">
                    <svg v-if="!file && !editingNoteFile" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <svg v-else class="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <p class="text-sm font-bold text-gray-500 dark:text-gray-400">
                    {{ file ? file.name : (editingNoteFile ? 'Cambiar archivo actual' : 'Arrastra un archivo o haz click aquí') }}
                  </p>
                  <p v-if="editingNoteFile && !file" class="text-xs text-indigo-500 dark:text-indigo-400 mt-1 font-medium">📎 Archivo actual guardado</p>
                </div>
              </div>
            </div>

            <div class="flex gap-4 pt-6">
              <button type="button" @click="closeModal" 
                class="flex-1 px-8 py-5 bg-gray-100 dark:bg-gray-900 text-gray-600 dark:text-gray-300 rounded-2xl font-black transition-all hover:bg-gray-200 dark:hover:bg-gray-700 active:scale-95 uppercase tracking-widest text-sm"
              >
                Cancelar
              </button>
              <button type="submit" :disabled="saving" 
                class="flex-[2] px-8 py-5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-2xl font-black shadow-xl shadow-indigo-500/20 hover:shadow-2xl hover:scale-[1.02] transition-all active:scale-95 disabled:opacity-50 uppercase tracking-widest text-sm"
              >
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
const showOnlyFavorites = ref(false)
const showModal = ref(false)
const editing = ref(null)
const form = ref({ title: '', content: '' })
const saving = ref(false)
const file = ref(null)
const editingNoteFile = ref(null)
const confirmingDelete = ref(null)

const filteredNotes = computed(() => {
  let result = [...notes.value]
  // Favorites first
  result.sort((a, b) => (b.favorite ? 1 : 0) - (a.favorite ? 1 : 0))
  if (showOnlyFavorites.value) result = result.filter(n => n.favorite)
  if (searchTerm.value) {
    const q = searchTerm.value.toLowerCase()
    result = result.filter(n =>
      n.title?.toLowerCase().includes(q) || n.text?.toLowerCase().includes(q)
    )
  }
  return result
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
  editingNoteFile.value = null
  showModal.value = false
}

const editNote = (note) => {
  editing.value = note.slug
  form.value = { title: note.title, content: note.text }
  editingNoteFile.value = note.file
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

const toggleFavorite = async (note) => {
  try {
    const response = await api.post(`/notes/favorite/${note.slug}/`)
    const idx = notes.value.findIndex(n => n.id === note.id)
    if (idx !== -1) notes.value[idx] = response.data
  } catch (error) {
    console.error('Error toggling favorite:', error)
  }
}

const deleteNote = async (note) => {
  if (confirmingDelete.value !== note.id) {
    confirmingDelete.value = note.id
    setTimeout(() => {
      if (confirmingDelete.value === note.id) confirmingDelete.value = null
    }, 3000)
    return
  }
  try {
    await api.post(`/notes/delete/${note.slug}/`)
    notes.value = notes.value.filter(n => n.id !== note.id)
    confirmingDelete.value = null
  } catch (error) {
    console.error('Error deleting note:', error)
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
