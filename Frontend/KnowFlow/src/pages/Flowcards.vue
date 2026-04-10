<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-8">
        <div>
          <h1 class="text-4xl font-bold text-gray-900 mb-2">Flashcards</h1>
          <p class="text-xl text-gray-600">Aprende con repetición espaciada</p>
        </div>
        <Button @click="showCreateModal = true" class="w-full lg:w-auto">
          + Nueva Flashcard
        </Button>
      </div>

      <!-- Filter & Search -->
      <div class="card mb-8 p-6">
        <div class="flex flex-col md:flex-row gap-4 items-center md:items-stretch">
          <div class="flex-1">
            <input
              v-model="searchTerm"
              @input="filterCards"
              placeholder="Buscar flashcards..."
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
          <Button variant="outline" class="px-6">Filtros</Button>
        </div>
      </div>

      <!-- Flashcards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="card in filteredCards" 
          :key="card.slug"
          class="card overflow-hidden hover:shadow-2xl group cursor-pointer transition-all"
          @click="editCard(card)"
        >
          <div class="p-6 h-48 flex flex-col justify-between bg-gradient-to-br from-blue-50 to-indigo-50 group-hover:from-blue-100">
            <div>
              <div class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 mb-4">
                {{ card.library ? 'En librería' : 'Sin librería' }}
              </div>
              <h3 class="font-bold text-lg text-gray-900 mb-2 line-clamp-1 group-hover:text-primary-600">{{ card.term }}</h3>
              <p class="text-gray-600 text-sm line-clamp-2">{{ card.definition }}</p>
            </div>
            <div class="flex items-center justify-between pt-2">
              <span class="text-xs text-gray-500">Creada: {{ formatDate(card.created_at) }}</span>
              <button @click.stop="studyCard(card.slug)" class="px-3 py-1 bg-gradient-to-r from-primary-500 to-primary-600 text-white text-xs rounded-lg hover:from-primary-600 hover:to-primary-700 transition-all">
                Estudiar
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!filteredCards.length" class="col-span-full flex flex-col items-center justify-center py-24 text-center border-2 border-dashed border-gray-200 rounded-3xl col-span-1 md:col-span-2 lg:col-span-3">
          <div class="w-24 h-24 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-3xl flex items-center justify-center mb-6 p-6">
            <svg class="w-12 h-12 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 5 7.5c1.323 0 2.5 1.177 2.5 2.5s1.177 2.5 2.5 2.5 2.5-1.177 2.5-2.5S9.168 7.323 10.5 7.5c0.832 0 1.246.477 1.5 1.5 3 3z" />
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">{{ searchTerm ? 'No se encontraron flashcards' : 'No tienes flashcards' }}</h3>
          <p class="text-gray-600 mb-6 max-w-md">{{ searchTerm ? 'Intenta con otras palabras.' : 'Crea tu primera flashcard para empezar a estudiar.' }}</p>
          <Button @click="showCreateModal = true" class="px-8 py-3 text-lg">Crear flashcard</Button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-3xl shadow-2xl max-w-md w-full">
        <div class="p-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">{{ editingCard ? 'Editar Flashcard' : 'Nueva Flashcard' }}</h2>
          <form @submit.prevent="saveCard" class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Término *</label>
              <input
                v-model="form.term"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500"
                placeholder="Concepto o pregunta"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Definición *</label>
              <textarea
                v-model="form.definition"
                required
                rows="4"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 resize-vertical"
                placeholder="Explicación o respuesta"
              ></textarea>
            </div>
            <div class="flex space-x-3 pt-2">
              <Button type="submit" :loading="saving" class="flex-1">Guardar</Button>
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
import { flowcardService } from '@/services/api'
import type { Flowcard } from '@/types/index'

const router = useRouter()
const flowcards = ref<Flowcard[]>([])
const filteredCards = ref<Flowcard[]>([])
const searchTerm = ref('')
const showCreateModal = ref(false)
const editingCard = ref<Flowcard | null>(null)
const form = ref({ term: '', definition: '' })
const saving = ref(false)

const loadFlowcards = async () => {
  try {
    const response = await flowcardService.getAll()
    flowcards.value = response.data
    filteredCards.value = flowcards.value
  } catch (error) {
    console.error('Error loading flowcards:', error)
  }
}

const filterCards = () => {
  if (!searchTerm.value) {
    filteredCards.value = flowcards.value
    return
  }
  filteredCards.value = flowcards.value.filter(card =>
    card.term.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    card.definition.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
}

const studyCard = (slug: string) => {
  router.push(`/flowcards/study/${slug}`)
}

const editCard = (card: Flowcard) => {
  editingCard.value = card
  form.value = { term: card.term, definition: card.definition }
  showCreateModal.value = true
}

const closeModal = () => {
  showCreateModal.value = false
  editingCard.value = null
  form.value = { term: '', definition: '' }
}

const saveCard = async () => {
  saving.value = true
  try {
    if (editingCard.value) {
      await flowcardService.update(editingCard.value.slug, form.value)
    } else {
      await flowcardService.create(form.value)
    }
    closeModal()
    loadFlowcards()
  } catch (error) {
    console.error('Error saving card:', error)
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

onMounted(loadFlowcards)
</script>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
