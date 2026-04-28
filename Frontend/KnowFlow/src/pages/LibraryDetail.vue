<template>
  <DefaultLayout>
    <div v-if="loading" class="min-h-[60vh] flex flex-col items-center justify-center space-y-4">
      <div class="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
      <p class="text-gray-500 font-bold animate-pulse">Cargando tu contenido...</p>
    </div>

    <div v-else-if="library" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <!-- Header / Hero Section -->
      <div class="relative overflow-hidden bg-gradient-to-br from-indigo-600 via-blue-700 to-indigo-800 rounded-[3rem] p-10 md:p-14 mb-12 shadow-2xl shadow-blue-500/20">
        <!-- Decorators -->
        <div class="absolute top-0 right-0 -mt-20 -mr-20 w-80 h-80 bg-white/10 rounded-full blur-3xl"></div>
        <div class="absolute bottom-0 left-0 -mb-20 -ml-20 w-80 h-80 bg-blue-400/20 rounded-full blur-3xl"></div>
        
        <div class="relative flex flex-col md:flex-row md:items-center justify-between gap-10">
          <div class="flex items-start md:items-center space-x-8">
            <div class="w-24 h-24 bg-white/10 backdrop-blur-xl border border-white/20 rounded-[2rem] flex items-center justify-center shrink-0 shadow-inner">
              <span class="text-4xl font-black text-white">{{ library.name?.charAt(0).toUpperCase() }}</span>
            </div>
            
            <div class="flex-1">
              <h1 class="text-4xl md:text-5xl font-black text-white mb-3 tracking-tight drop-shadow-sm">
                {{ library.name }}
              </h1>
              <p class="text-blue-100 text-lg md:text-xl font-medium opacity-90 max-w-2xl leading-relaxed mb-6">
                {{ library.description || 'Sin descripción disponible para esta librería.' }}
              </p>
              
              <div class="flex flex-wrap gap-6 text-sm">
                <div class="flex items-center text-blue-50 bg-white/10 px-4 py-2 rounded-full backdrop-blur-md border border-white/10">
                  <svg class="w-4 h-4 mr-2 opacity-70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  Creada {{ timeAgo(library.created_at) }}
                </div>
              </div>
            </div>
          </div>
          
          <div class="flex flex-col gap-3 shrink-0">
            <button @click="openEditModal" class="bg-white text-blue-700 px-8 py-4 rounded-2xl font-black text-lg shadow-xl hover:bg-blue-50 hover:scale-105 transition-all active:scale-95 flex items-center justify-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              Editar Librería
            </button>
            <button @click="deleteLibrary" class="bg-rose-500/20 backdrop-blur-md border border-rose-500/30 text-rose-100 px-8 py-4 rounded-2xl font-bold hover:bg-rose-500/30 transition-all active:scale-95 flex items-center justify-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              Eliminar
            </button>
          </div>
        </div>
      </div>

      <!-- Content Navigation (Tabs) -->
      <div class="bg-white dark:bg-gray-800 rounded-[2.5rem] shadow-xl border border-gray-100 dark:border-gray-700 overflow-hidden min-h-[500px]">
        <div class="border-b border-gray-100 dark:border-gray-700 px-10">
          <nav class="flex space-x-12">
            <button 
              v-for="tab in tabs" 
              :key="tab.id"
              @click="activeTab = tab.id" 
              :class="[
                activeTab === tab.id 
                  ? 'border-blue-600 text-blue-600 dark:text-blue-400' 
                  : 'border-transparent text-gray-400 hover:text-gray-600 dark:hover:text-gray-300'
              ]"
              class="relative py-8 px-2 border-b-4 font-black text-sm uppercase tracking-widest transition-all outline-none"
            >
              {{ tab.label }}
              <span v-if="activeTab === tab.id" class="absolute inset-x-0 bottom-0 h-1 bg-blue-600 rounded-t-full"></span>
            </button>
          </nav>
        </div>

        <div class="p-10 md:p-14">
          <!-- Flashcards Tab -->
          <div v-if="activeTab === 'flashcards'" class="animate-in fade-in duration-500">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-10">
              <div>
                <h2 class="text-3xl font-black text-gray-900 dark:text-white mb-2">Flashcards</h2>
                <p class="text-gray-500 dark:text-gray-400 font-medium">Practica con tus tarjetas de memoria.</p>
              </div>
              <router-link to="/flowcards" class="px-8 py-4 bg-emerald-600 hover:bg-emerald-700 text-white rounded-2xl font-black shadow-lg shadow-emerald-500/20 transition-all flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                NUEVA FLASHCARD
              </router-link>
            </div>
            <div class="py-20 flex flex-col items-center justify-center text-gray-400">
              <p class="font-bold">Contenido enlazado pronto disponible aquí.</p>
            </div>
          </div>

          <!-- Notes Tab -->
          <div v-if="activeTab === 'notes'" class="animate-in fade-in duration-500">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-10">
              <div>
                <h2 class="text-3xl font-black text-gray-900 dark:text-white mb-2">Notas</h2>
                <p class="text-gray-500 dark:text-gray-400 font-medium">Tus apuntes y conocimientos escritos.</p>
              </div>
              <router-link to="/notes" class="px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl font-black shadow-lg shadow-blue-500/20 transition-all flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                NUEVA NOTA
              </router-link>
            </div>
            <div class="py-20 flex flex-col items-center justify-center text-gray-400">
               <p class="font-bold text-lg mb-2">Aún no tienes notas en esta librería.</p>
            </div>
          </div>

          <!-- Quizzes Tab -->
          <div v-if="activeTab === 'knowtionaries'" class="animate-in fade-in duration-500">
             <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-10">
              <div>
                <h2 class="text-3xl font-black text-gray-900 dark:text-white mb-2">Cuestionarios</h2>
                <p class="text-gray-500 dark:text-gray-400 font-medium">Ponte a prueba con tests inteligentes.</p>
              </div>
              <router-link to="/knowtionaries" class="px-8 py-4 bg-purple-600 hover:bg-purple-700 text-white rounded-2xl font-black shadow-lg shadow-purple-500/20 transition-all flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                NUEVO CUESTIONARIO
              </router-link>
            </div>
             <div class="py-20 flex flex-col items-center justify-center text-gray-400">
               <p class="font-bold text-lg">Próximamente disponible.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Library Modal -->
    <div v-if="showEditModal" class="fixed inset-0 z-[60] flex items-center justify-center p-6 overflow-y-auto">
      <div class="fixed inset-0 bg-gray-900/60 backdrop-blur-md transition-opacity" @click="showEditModal = false"></div>
      
      <div class="relative bg-white dark:bg-gray-800 rounded-[2.5rem] shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-300">
        <div class="p-10">
          <div class="flex justify-between items-center mb-8">
            <h2 class="text-3xl font-black text-gray-900 dark:text-white tracking-tight">Editar Librería</h2>
            <button @click="showEditModal = false" class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full text-gray-400 transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit.prevent="updateLibrary" class="space-y-6">
            <div class="space-y-2">
              <label class="text-sm font-bold text-gray-700 dark:text-gray-300 ml-1 uppercase tracking-wider">Nombre</label>
              <input v-model="editForm.name" required type="text" class="w-full px-6 py-4 bg-gray-50 dark:bg-gray-900 border border-transparent dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:bg-white dark:focus:bg-gray-800 dark:text-white transition-all outline-none font-medium">
            </div>
            
            <div class="space-y-2">
              <label class="text-sm font-bold text-gray-700 dark:text-gray-300 ml-1 uppercase tracking-wider">Descripción</label>
              <textarea v-model="editForm.description" rows="3" class="w-full px-6 py-4 bg-gray-50 dark:bg-gray-900 border border-transparent dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:bg-white dark:focus:bg-gray-800 dark:text-white transition-all outline-none resize-none font-medium"></textarea>
            </div>
            
            <div class="flex gap-4 pt-4">
              <button type="submit" :disabled="updating" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-4 px-6 rounded-2xl font-black shadow-lg transition-all disabled:opacity-50">
                {{ updating ? 'GUARDANDO...' : 'GUARDAR CAMBIOS' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { libraryService } from '@/services/api'

const route = useRoute()
const router = useRouter()
const libraryId = route.params.id
const activeTab = ref('flashcards')
const library = ref(null)
const loading = ref(true)

const showEditModal = ref(false)
const updating = ref(false)
const editForm = ref({ name: '', description: '' })

const tabs = [
  { id: 'flashcards', label: 'Flashcards' },
  { id: 'notes', label: 'Notas' },
  { id: 'knowtionaries', label: 'Quizzes' }
]

const timeAgo = (dateStr) => {
  if (!dateStr) return 'recientemente'
  const date = new Date(dateStr)
  const now = new Date()
  const seconds = Math.floor((now - date) / 1000)
  if (seconds < 60) return 'hace un momento'
  const minutes = Math.floor(seconds / 60)
  if (minutes < 60) return `hace ${minutes} min`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `hace ${hours}h`
  const days = Math.floor(hours / 24)
  if (days < 30) return `hace ${days} días`
  return date.toLocaleDateString()
}

const loadLibrary = async () => {
  loading.value = true
  try {
    const response = await libraryService.getById(libraryId)
    library.value = response.data
    editForm.value = { name: library.value.name, description: library.value.description }
  } catch (error) {
    console.error('Error loading library:', error)
    router.push('/libraries')
  } finally {
    loading.value = false
  }
}

const openEditModal = () => {
  editForm.value = { name: library.value.name, description: library.value.description }
  showEditModal.value = true
}

const updateLibrary = async () => {
  updating.value = true
  try {
    await libraryService.update(libraryId, editForm.value)
    await loadLibrary()
    showEditModal.value = false
  } catch (error) {
    console.error('Error updating library:', error)
    alert('Error al actualizar la librería')
  } finally {
    updating.value = false
  }
}

const deleteLibrary = async () => {
  if (!confirm('¿Estás seguro de que quieres eliminar esta librería? Todos sus contenidos se perderán.')) return
  
  try {
    console.log('Eliminando librería:', libraryId)
    await libraryService.delete(libraryId)
    console.log('Eliminación exitosa')
    router.push('/libraries')
    // Fallback if router fails
    setTimeout(() => {
      if (window.location.pathname.includes(libraryId)) {
        window.location.href = '/libraries'
      }
    }, 500)
  } catch (error) {
    console.error('Error deleting library:', error)
    alert('Error al eliminar la librería: ' + (error.response?.data?.error || error.message))
  }
}

onMounted(loadLibrary)
</script>

<style scoped>
@keyframes zoom-in {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
.animate-in {
  animation: zoom-in 0.3s ease-out forwards;
}
</style>
