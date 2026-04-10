<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-8">
        <div>
          <h1 class="text-4xl font-bold text-gray-900 mb-2">Mis Librerías</h1>
          <p class="text-xl text-gray-600">Organiza todo tu contenido de estudio</p>
        </div>
        <Button @click="showCreateModal = true" class="w-full lg:w-auto">
          + Nueva Librería
        </Button>
      </div>

      <!-- Libraries Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
        <div 
          v-for="library in libraries" 
          :key="library.id"
          class="group cursor-pointer card hover:shadow-2xl transition-all duration-300 overflow-hidden hover:-translate-y-2"
          @click="goToLibrary(library.id)"
        >
          <div class="p-6 h-48 flex flex-col justify-between">
            <div>
              <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center mb-4">
                <span class="text-xl font-bold text-white">{{ library.name.charAt(0).toUpperCase() }}</span>
              </div>
              <h3 class="font-bold text-xl text-gray-900 mb-2 line-clamp-2 group-hover:text-primary-600 transition-colors">{{ library.name }}</h3>
              <p class="text-gray-600 text-sm mb-4 line-clamp-2">{{ library.description || 'Sin descripción' }}</p>
            </div>
            <div class="text-right">
              <span class="px-3 py-1 bg-primary-100 text-primary-800 text-xs font-medium rounded-full">
                {{ library.contents }} items
              </span>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!libraries.length" class="col-span-full flex flex-col items-center justify-center py-24 text-center border-2 border-dashed border-gray-200 rounded-3xl">
          <div class="w-24 h-24 bg-gray-100 rounded-3xl flex items-center justify-center mb-6">
            <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16M17 5v2m0 0v2m0-2h2m-2 0h-2m-6 0h2m-2 0H9" />
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">No tienes librerías</h3>
          <p class="text-gray-600 mb-6 max-w-md">Crea tu primera librería para organizar flashcards, notas y cuestionarios.</p>
          <Button @click="showCreateModal = true" class="px-8 py-3 text-lg">Crear primera librería</Button>
        </div>
      </div>
    </div>

    <!-- Create Library Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-3xl shadow-2xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div class="p-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">Nueva Librería</h2>
          <form @submit.prevent="createLibrary" class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Nombre *</label>
              <input
                v-model="newLibrary.name"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="Nombre de tu librería"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Descripción</label>
              <textarea
                v-model="newLibrary.description"
                rows="3"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-vertical"
                placeholder="Describe el contenido de esta librería (opcional)"
              ></textarea>
            </div>
            <div class="flex space-x-3 pt-2">
              <Button type="submit" :loading="creating" class="flex-1">Crear Librería</Button>
              <Button type="button" variant="secondary" @click="showCreateModal = false" class="flex-1">Cancelar</Button>
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
import { libraryService } from '@/services/api'
import type { Library } from '@/types/index'

const router = useRouter()
const libraries = ref<Library[]>([])
const showCreateModal = ref(false)
const newLibrary = ref({ name: '', description: '' })
const creating = ref(false)

const loadLibraries = async () => {
  try {
    const response = await libraryService.getAll()
    libraries.value = response.data
  } catch (error) {
    console.error('Error loading libraries:', error)
  }
}

const createLibrary = async () => {
  creating.value = true
  try {
    await libraryService.create(newLibrary.value)
    showCreateModal.value = false
    newLibrary.value = { name: '', description: '' }
    loadLibraries()
  } catch (error) {
    console.error('Error creating library:', error)
  } finally {
    creating.value = false
  }
}

const goToLibrary = (id: number) => {
  router.push(`/libraries/${id}`)
}

onMounted(loadLibraries)
</script>

<style scoped>
.card {
  @apply bg-white shadow-lg rounded-2xl border border-gray-100 hover:shadow-2xl transition-all;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
