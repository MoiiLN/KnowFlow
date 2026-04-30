<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-16">
        <div>
          <h1 class="text-5xl font-black text-gray-900 dark:text-white mb-3 tracking-tight">Mis Librerías</h1>
          <p class="text-xl text-gray-500 dark:text-gray-400 font-medium">Organiza y gestiona tu conocimiento personal.</p>
        </div>
        <button 
          @click="showModal = true" 
          class="group flex items-center px-10 py-5 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl font-black text-lg shadow-xl shadow-blue-500/25 transition-all active:scale-95"
        >
          <svg class="w-6 h-6 mr-3 group-hover:rotate-90 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 4v16m8-8H4" />
          </svg>
          Nueva Librería
        </button>
      </div>

      <!-- Libraries Grid -->
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="i in 3" :key="i" class="h-64 bg-gray-100 dark:bg-gray-800 rounded-[2.5rem] animate-pulse"></div>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
        <div 
          v-for="lib in libraries" 
          :key="lib.id" 
          class="group relative bg-white dark:bg-gray-800 p-10 rounded-[2.5rem] shadow-sm hover:shadow-2xl border border-gray-100 dark:border-gray-700 transition-all duration-500 cursor-pointer hover:-translate-y-2"
          @click="selectLibrary(lib)"
        >
          <!-- Card Decorator -->
          <div class="absolute top-0 right-0 w-32 h-32 bg-blue-50 dark:bg-blue-900/10 rounded-full -mr-12 -mt-12 group-hover:bg-blue-100 dark:group-hover:bg-blue-900/20 transition-colors duration-500"></div>
          
          <div class="relative">
            <div class="w-20 h-20 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-3xl flex items-center justify-center mb-8 shadow-lg shadow-blue-500/20 group-hover:scale-110 group-hover:rotate-3 transition-all duration-500">
              <span class="text-3xl font-black text-white">{{ lib.name?.charAt(0).toUpperCase() }}</span>
            </div>
            
            <h3 class="text-2xl font-black text-gray-900 dark:text-white mb-4 line-clamp-2 leading-tight group-hover:text-blue-600 transition-colors">
              {{ lib.name }}
            </h3>
            
            <p class="text-gray-500 dark:text-gray-400 font-medium mb-10 line-clamp-2 leading-relaxed">
              {{ lib.description || 'Explora el contenido de esta librería y sigue aprendiendo.' }}
            </p>
            
            <div class="flex items-center justify-between pt-6 border-t border-gray-50 dark:border-gray-700">
              <span class="px-5 py-2 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400 rounded-full text-xs font-black uppercase tracking-widest">
                VER CONTENIDO
              </span>
              <svg class="w-6 h-6 text-gray-300 group-hover:text-blue-500 group-hover:translate-x-2 transition-all duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="libraries.length === 0" class="col-span-full py-24 bg-gray-50/50 dark:bg-gray-800/30 border-4 border-dashed border-gray-200 dark:border-gray-700 rounded-[3.5rem] flex flex-col items-center justify-center text-center">
          <div class="w-28 h-28 bg-white dark:bg-gray-800 rounded-[2.5rem] shadow-xl flex items-center justify-center mb-8 text-gray-200">
            <svg class="w-14 h-14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <h3 class="text-3xl font-black text-gray-900 dark:text-white mb-3">Tu biblioteca está vacía</h3>
          <p class="text-gray-500 dark:text-gray-400 max-w-sm font-medium mb-10">Empieza por crear una librería para organizar tus flashcards y notas.</p>
          <button @click="showModal = true" class="px-10 py-5 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl font-black shadow-xl shadow-blue-500/20 transition-all hover:scale-105 active:scale-95">
            CREAR MI PRIMERA LIBRERÍA
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Nueva Librería -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-6 overflow-y-auto">
      <div class="fixed inset-0 bg-gray-900/60 backdrop-blur-md transition-opacity" @click="showModal = false"></div>
      
      <div class="relative bg-white dark:bg-gray-800 rounded-[2.5rem] shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-300">
        <div class="p-10">
          <div class="flex justify-between items-center mb-10">
            <h2 class="text-3xl font-black text-gray-900 dark:text-white tracking-tight">Nueva Librería</h2>
            <button @click="showModal = false" class="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full text-gray-400 transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit.prevent="createLibrary" class="space-y-8">
            <div class="space-y-2">
              <label class="text-sm font-bold text-gray-700 dark:text-gray-300 ml-1 uppercase tracking-wider">Nombre</label>
              <input 
                v-model="newLibrary.name" 
                required 
                type="text" 
                class="w-full px-6 py-4 bg-gray-50 dark:bg-gray-900 border border-transparent dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:bg-white dark:focus:bg-gray-800 dark:text-white transition-all outline-none font-medium" 
                placeholder="Ej: Biología Celular"
              >
            </div>
            
            <div class="space-y-2">
              <label class="text-sm font-bold text-gray-700 dark:text-gray-300 ml-1 uppercase tracking-wider">Descripción</label>
              <textarea 
                v-model="newLibrary.description" 
                rows="3" 
                class="w-full px-6 py-4 bg-gray-50 dark:bg-gray-900 border border-transparent dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:bg-white dark:focus:bg-gray-800 dark:text-white transition-all outline-none resize-none font-medium" 
                placeholder="Opcional: ¿Qué vas a estudiar aquí?"
              ></textarea>
            </div>
            
            <div class="flex gap-4 pt-4">
              <button 
                type="submit" 
                :disabled="creating" 
                class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-5 px-6 rounded-2xl font-black shadow-lg shadow-blue-500/20 transition-all disabled:opacity-50 active:scale-95"
              >
                {{ creating ? 'CREANDO...' : 'CREAR LIBRERÍA' }}
              </button>
              <button 
                type="button" 
                @click="showModal = false" 
                class="flex-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 py-5 px-6 rounded-2xl font-black hover:bg-gray-200 dark:hover:bg-gray-600 transition-all"
              >
                CANCELAR
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
import { useRouter } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import api from '@/services/api'

const router = useRouter()
const libraries = ref([])
const showModal = ref(false)
const newLibrary = ref({ name: '', description: '' })
const creating = ref(false)
const loading = ref(false)

const loadLibraries = async () => {
  loading.value = true
  try {
    const response = await api.get('libraries/')
    libraries.value = response.data
  } catch (error) {
    console.error('Error loading libraries:', error)
  } finally {
    loading.value = false
  }
}

const createLibrary = async () => {
  creating.value = true
  try {
    const formData = new FormData()
    formData.append('name', newLibrary.value.name)
    formData.append('description', newLibrary.value.description)
    await api.post('libraries/create/', formData)
    await loadLibraries()
    showModal.value = false
    newLibrary.value = { name: '', description: '' }
  } catch (error) {
    console.error('Error creating library:', error)
  } finally {
    creating.value = false
  }
}

const selectLibrary = (lib) => {
  router.push(`/libraries/${lib.id}`)
}

onMounted(loadLibraries)
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@keyframes zoom-in {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
.animate-in {
  animation: zoom-in 0.3s ease-out forwards;
}
</style>
