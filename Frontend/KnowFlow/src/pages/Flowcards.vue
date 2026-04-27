<template>
  <DefaultLayout>

    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center mb-12">
        <div>
          <h1 class="text-4xl font-bold text-gray-900">Flashcards</h1>
          <p class="text-xl text-gray-600 mt-2">Aprende con repetición espaciada</p>
        </div>
        <button @click="showModal = true" class="bg-emerald-600 text-white px-8 py-3 rounded-xl hover:bg-emerald-700 font-semibold shadow-lg hover:shadow-xl transition-all">
          + Nueva Flashcard
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="card in filteredCards" :key="card.id" class="bg-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all cursor-pointer group hover:-translate-y-2" @click="editCard(card)">
          <div class="bg-gradient-to-br from-blue-50 to-indigo-50 p-6 rounded-xl mb-6 group-hover:from-blue-100">
            <h3 class="font-bold text-lg text-gray-900 mb-2 line-clamp-1">{{ card.term }}</h3>
            <p class="text-gray-600 text-sm line-clamp-2">{{ card.definition }}</p>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-xs text-gray-500">{{ formatDate(card.created) }}</span>
            <button @click.stop="studyCard(card.id)" class="px-4 py-2 bg-gradient-to-r from-emerald-500 to-teal-500 text-white text-sm rounded-lg hover:from-emerald-600 hover:to-teal-600 transition-all">
              Estudiar →
            </button>
          </div>
        </div>

        <div v-if="filteredCards.length === 0" class="col-span-full flex flex-col items-center justify-center py-24 border-2 border-dashed border-gray-300 rounded-3xl">
          <div class="w-24 h-24 bg-gradient-to-br from-emerald-100 to-teal-100 rounded-3xl flex items-center justify-center mb-6 p-6">
            <svg class="w-12 h-12 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 5 7.5c1.323 0 2.5 1.177 2.5 2.5s1.177 2.5 2.5 2.5 2.5-1.177 2.5-2.5S9.168 7.323 10.5 7.5c0.832 0 1.246.477 1.5 1.5 3 3z" />
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">{{ searchTerm ? 'Sin resultados' : 'Sin flashcards' }}</h3>
          <p class="text-gray-600 mb-6">Comienza creando tu primera flashcard</p>
          <button @click="showModal = true" class="bg-gradient-to-r from-emerald-600 to-teal-600 text-white px-8 py-4 rounded-2xl font-semibold shadow-xl hover:shadow-2xl">
            Crear flashcard
          </button>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-6">
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-md">
        <div class="p-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">{{ editing ? 'Editar' : 'Nueva' }} Flashcard</h2>
          <form @submit.prevent="saveCard">
            <div class="mb-6">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Término</label>
              <input v-model="form.term" required type="text" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500">
            </div>
            <div class="mb-8">
              <label class="block text-sm font-semibold text-gray-700 mb-2">Definición</label>
              <textarea v-model="form.definition" required rows="4" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500"></textarea>
            </div>
            <div class="flex gap-3">
              <button type="submit" :disabled="saving" class="flex-1 bg-gradient-to-r from-emerald-600 to-teal-600 text-white py-3 px-6 rounded-xl font-semibold hover:shadow-xl disabled:opacity-50">
                {{ saving ? 'Guardando...' : 'Guardar' }}
              </button>
              <button type="button" @click="closeModal" class="flex-1 bg-gray-200 text-gray-800 py-3 px-6 rounded-xl font-semibold hover:bg-gray-300">
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
import { useRouter } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import api from '@/services/api'

const router = useRouter()
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

const formatDate = (date) => new Date(date).toLocaleDateString('es-ES')

const studyCard = (id) => router.push(`/flowcards/study/${id}`)

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
    let updatedCards = cards.value
    if (editing.value) {
      // Edit
      await api.post(`/flowcards/edit/${editing.value}/`, form.value)
    } else {
      // Create - mock library_content_id = 1 (ajusta según tu backend)
      const createData = {
        ...form.value,
        library_content_id: 1,  // Necesitas ID de LibraryContent real
        name: form.value.term.substring(0, 50),
        slug: form.value.term.toLowerCase().replace(/\\s+/g, '-').substring(0, 50)
      }
      await api.post('flowcards/add/', createData)
    }
    // Reload
    await loadCards()
  } catch (error) {
    console.error('Error saving card:', error)
    alert('Error al guardar flashcard. Ver console.')
  } finally {
    closeModal()
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

onMounted(loadCards)
</script>

<style scoped>
.line-clamp-1, .line-clamp-2 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.line-clamp-1 { -webkit-line-clamp: 1; }
.line-clamp-2 { -webkit-line-clamp: 2; }
</style>

