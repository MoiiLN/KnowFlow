<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center mb-12">
        <div>
          <h1 class="text-4xl font-bold text-gray-900">Mis Librerías</h1>
          <p class="text-xl text-gray-600 mt-2">Organiza tu contenido de estudio</p>
        </div>
        <button @click="showModal = true" class="bg-blue-600 text-white px-8 py-3 rounded-xl hover:bg-blue-700 font-semibold shadow-lg hover:shadow-xl transition-all">
          + Nueva Librería
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="lib in libraries" :key="lib.id" class="bg-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all cursor-pointer group hover:-translate-y-2" @click="selectLibrary(lib)">
          <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mb-6 mx-auto group-hover:scale-110 transition-transform">
            <span class="text-2xl font-bold text-white">{{ lib.name.charAt(0).toUpperCase() }}</span>
          </div>
          <h3 class="text-xl font-bold text-gray-900 mb-3 text-center line-clamp-2">{{ lib.name }}</h3>
          <p class="text-gray-600 text-center mb-6 line-clamp-2">{{ lib.description }}</p>
          <div class="flex items-center justify-center">
            <span class="px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
              {{ lib.items }} items
            </span>
          </div>
        </div>

        <div v-if="libraries.length === 0" class="col-span-full flex flex-col items-center justify-center py-24 border-2 border-dashed border-gray-300 rounded-3xl">
          <div class="w-24 h-24 bg-gray-100 rounded-3xl flex items-center justify-center mb-6">
            <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0H7m5 0v-5m0 0a1 1 0 00-1-1H6a1 1 0 00-1 1v5m6-5h2a1 1 0 001-1V9a1 1 0 00-1-1h-2a1 1 0 00-1 1v5z" />
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">Sin librerías</h3>
          <p class="text-gray-600 mb-6">Crea tu primera librería para comenzar</p>
          <button @click="showModal = true" class="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-2xl font-semibold shadow-xl hover:shadow-2xl hover:scale-105 transition-all">
            Crear primera librería
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Nueva Librería -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-6">
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-md transform transition-all">
        <div class="p-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">Nueva Librería</h2>
          <form @submit.prevent="createLibrary">
            <div class="mb-6">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Nombre</label>
              <input v-model="newLibrary.name" required type="text" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="Nombre de la librería">
            </div>
            <div class="mb-8">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Descripción</label>
              <textarea v-model="newLibrary.description" rows="3" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="Descripción opcional..."></textarea>
            </div>
            <div class="flex gap-3">
              <button type="submit" :disabled="creating" class="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-xl font-semibold hover:shadow-xl transition-all disabled:opacity-50">
                {{ creating ? 'Creando...' : 'Crear Librería' }}
              </button>
              <button type="button" @click="showModal = false" class="flex-1 bg-gray-200 text-gray-800 py-3 px-6 rounded-xl font-semibold hover:bg-gray-300 transition-all">
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
    const response = await api.get('/libraries/')
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
    await api.post('/libraries/create/', formData)
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
</style>

