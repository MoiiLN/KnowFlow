<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto py-12 lg:py-16 px-4 sm:px-6 lg:px-8">
      <!-- Header Section -->
      <div class="relative overflow-hidden bg-gradient-to-br from-emerald-600 to-teal-700 rounded-[2.5rem] p-8 md:p-12 mb-12 shadow-2xl shadow-emerald-500/20">
        <div class="absolute top-0 right-0 -mt-12 -mr-12 w-64 h-64 bg-white/10 rounded-full blur-3xl"></div>
        <div class="absolute bottom-0 left-0 -mb-12 -ml-12 w-48 h-48 bg-emerald-400/20 rounded-full blur-2xl"></div>
        
        <div class="relative flex flex-col md:flex-row md:items-center justify-between gap-8">
          <div class="max-w-2xl">
            <h1 class="text-4xl md:text-5xl font-extrabold text-white mb-4 tracking-tight">Flashcards</h1>
            <p class="text-emerald-50 text-lg md:text-xl font-medium opacity-90">
              Potencia tu memoria con repetición espaciada. Tienes <span class="font-bold underline">{{ cards.length }}</span> cartas listas para revisar.
            </p>
          </div>
          
          <div class="flex flex-wrap gap-4">
            <button 
              v-if="cards.length > 0"
              @click="studyAll" 
              class="flex items-center px-8 py-4 bg-white text-emerald-700 rounded-2xl font-bold text-lg shadow-xl hover:bg-emerald-50 hover:scale-105 transition-all active:scale-95 group"
            >
              <svg class="w-6 h-6 mr-2 group-hover:rotate-12 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Estudiar Sesión
            </button>
            
            <button 
              @click="showModal = true" 
              class="flex items-center px-8 py-4 bg-emerald-500/30 backdrop-blur-md border border-white/20 text-white rounded-2xl font-bold text-lg hover:bg-emerald-500/40 transition-all active:scale-95 group"
            >
              <svg class="w-6 h-6 mr-2 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3m0 0v3m0-3h3m-3 0H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Nueva Carta
            </button>
          </div>
        </div>
      </div>

      <!-- Search and Filter -->
      <div v-if="cards.length > 0" class="mb-8 flex items-center bg-white dark:bg-gray-800 p-2 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 max-w-md">
        <svg class="w-5 h-5 ml-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input 
          v-model="searchTerm"
          type="text" 
          placeholder="Buscar por término o definición..." 
          class="w-full bg-transparent border-none focus:ring-0 text-gray-700 dark:text-gray-200 px-3 py-2"
        />
      </div>

      <!-- Cards Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div 
          v-for="card in filteredCards" 
          :key="card.id" 
          class="group relative bg-white dark:bg-gray-800 rounded-3xl p-6 shadow-sm hover:shadow-xl border border-gray-100 dark:border-gray-700 transition-all duration-300 hover:-translate-y-1 cursor-pointer"
          @click="editCard(card)"
        >
          <!-- Card Decorator -->
          <div class="absolute top-0 right-0 w-24 h-24 bg-emerald-50 dark:bg-emerald-900/10 rounded-full -mr-12 -mt-12 group-hover:bg-emerald-100 dark:group-hover:bg-emerald-900/20 transition-colors"></div>
          
          <div class="relative h-full flex flex-col">
            <div class="mb-4">
              <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400 mb-3">
                FLASHCARD
              </span>
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2 line-clamp-2 leading-tight group-hover:text-emerald-600 transition-colors">
                {{ card.term }}
              </h3>
              <p class="text-gray-600 dark:text-gray-400 text-sm line-clamp-3 leading-relaxed">
                {{ card.definition }}
              </p>
            </div>
            
            <div class="mt-auto pt-4 border-t border-gray-50 dark:border-gray-700 flex items-center justify-between">
              <div class="flex items-center text-gray-400 text-xs font-medium">
                <svg class="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {{ timeAgo(card.created_at) }}
              </div>
              <div class="text-emerald-500 opacity-0 group-hover:opacity-100 transition-opacity">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="filteredCards.length === 0" class="col-span-full py-20 flex flex-col items-center justify-center text-center">
          <div class="w-32 h-32 bg-gray-50 dark:bg-gray-800 rounded-[3rem] flex items-center justify-center mb-6 shadow-inner text-gray-300">
            <svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            {{ searchTerm ? 'Sin coincidencias' : 'Tu colección está vacía' }}
          </h3>
          <p class="text-gray-500 dark:text-gray-400 max-w-sm">
            {{ searchTerm ? 'Prueba con otros términos de búsqueda.' : 'Crea tu primera flashcard para empezar a estudiar hoy mismo.' }}
          </p>
          <button 
            v-if="!searchTerm"
            @click="showModal = true" 
            class="mt-8 px-10 py-4 bg-emerald-600 hover:bg-emerald-700 text-white rounded-2xl font-bold shadow-lg shadow-emerald-600/20 transition-all"
          >
            Crear Primera Carta
          </button>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 z-[60] flex items-center justify-center p-4 sm:p-6 overflow-y-auto">
      <div class="fixed inset-0 bg-gray-900/60 backdrop-blur-sm transition-opacity" @click="closeModal"></div>
      
      <div class="relative bg-white dark:bg-gray-800 rounded-[2rem] shadow-2xl w-full max-w-lg overflow-hidden transition-all transform animate-in fade-in zoom-in duration-300">
        <div class="px-8 pt-8 pb-4 flex justify-between items-center">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
            {{ editing ? 'Editar Flashcard' : 'Nueva Flashcard' }}
          </h2>
          <button @click="closeModal" class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full text-gray-400 transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-8">
          <form @submit.prevent="saveCard" class="space-y-6">
            <div class="space-y-2">
              <label class="text-sm font-bold text-gray-700 dark:text-gray-300 ml-1 uppercase tracking-wider">Término o Pregunta</label>
              <input 
                v-model="form.term" 
                required 
                type="text" 
                placeholder="Ej: Mitocondria"
                class="w-full px-5 py-4 bg-gray-50 dark:bg-gray-900 border border-transparent dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-emerald-500 focus:bg-white dark:focus:bg-gray-800 dark:text-white transition-all outline-none"
              >
            </div>
            
            <div class="space-y-2">
              <label class="text-sm font-bold text-gray-700 dark:text-gray-300 ml-1 uppercase tracking-wider">Definición o Respuesta</label>
              <textarea 
                v-model="form.definition" 
                required 
                rows="4" 
                placeholder="Ej: Organelo encargado de la producción de ATP..."
                class="w-full px-5 py-4 bg-gray-50 dark:bg-gray-900 border border-transparent dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-emerald-500 focus:bg-white dark:focus:bg-gray-800 dark:text-white transition-all outline-none resize-none"
              ></textarea>
            </div>
            
            <div class="flex flex-col sm:flex-row gap-4 pt-4">
              <button 
                type="submit" 
                :disabled="saving" 
                class="flex-1 px-8 py-4 bg-emerald-600 hover:bg-emerald-700 text-white rounded-2xl font-bold shadow-lg shadow-emerald-600/20 transition-all disabled:opacity-50 active:scale-95"
              >
                {{ saving ? 'Guardando...' : 'Guardar Flashcard' }}
              </button>
              <button 
                type="button" 
                @click="closeModal" 
                class="px-8 py-4 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-2xl font-bold hover:bg-gray-200 dark:hover:bg-gray-600 transition-all"
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import api from '@/services/api'

const router = useRouter()
const route = useRoute()
const cards = ref([])

const searchTerm = ref('')
const showModal = ref(false)
const editing = ref(null)
const form = ref({ term: '', definition: '' })
const saving = ref(false)

const filteredCards = computed(() => {
  if (!searchTerm.value) return cards.value
  return cards.value.filter(card => 
    card.term.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    card.definition.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

const timeAgo = (dateStr) => {
  if (!dateStr) return 'Recientemente'
  const date = new Date(dateStr)
  if (isNaN(date.getTime())) return 'Recientemente'
  
  const now = new Date()
  const seconds = Math.floor((now - date) / 1000)
  
  let interval = Math.floor(seconds / 31536000)
  if (interval >= 1) return `hace ${interval} año${interval > 1 ? 's' : ''}`
  
  interval = Math.floor(seconds / 2592000)
  if (interval >= 1) return `hace ${interval} mes${interval > 1 ? 'es' : ''}`
  
  interval = Math.floor(seconds / 86400)
  if (interval >= 1) return `hace ${interval} día${interval > 1 ? 's' : ''}`
  
  interval = Math.floor(seconds / 3600)
  if (interval >= 1) return `hace ${interval} hora${interval > 1 ? 's' : ''}`
  
  interval = Math.floor(seconds / 60)
  if (interval >= 1) return `hace ${interval} min`
  
  return 'hace un momento'
}

const studyAll = () => {
  if (cards.value.length > 0) {
    router.push(`/flowcards/study/${cards.value[0].id}`)
  }
}

const editCard = (card) => {
  editing.value = card.id
  form.value = { term: card.term, definition: card.definition }
  showModal.value = true
}

const closeModal = () => {
  editing.value = null
  form.value = { term: '', definition: '' }
  showModal.value = false
}

const saveCard = async () => {
  saving.value = true
  try {
    if (editing.value) {
      await api.post(`flowcards/${editing.value}/edit/`, form.value)
    } else {
      const createData = {
        ...form.value,
        name: form.value.term.substring(0, 50),
        slug: form.value.term.toLowerCase().replace(/\s+/g, '-').substring(0, 50).replace(/[^a-z0-9-]/g, '') + '-' + Date.now()
      }
      if (route.query.library_id) {
        createData.library_id = route.query.library_id
      }
      await api.post('flowcards/add/', createData)
    }
    await loadCards()
    closeModal()
    if (route.query.library_id) {
      router.push(`/libraries/${route.query.library_id}`)
    }
  } catch (error) {
    console.error('Error saving card:', error)
  } finally {
    saving.value = false
  }
}

const loadCards = async () => {
  try {
    const response = await api.get('flowcards/')
    cards.value = response.data
  } catch (error) {
    console.error('Error loading cards:', error)
  }
}

onMounted(() => {
  loadCards()
  if (route.query.library_id) {
    showModal.value = true
  }
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  -webkit-line-clamp: 2;
}
.line-clamp-3 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  -webkit-line-clamp: 3;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-in {
  animation: fade-in 0.4s ease-out forwards;
}
</style>
