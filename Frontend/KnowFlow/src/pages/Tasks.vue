<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto">
      <div class="flex justify-between items-center mb-12">
        <div>
          <h1 class="text-4xl font-bold text-gray-900 mb-2">Tareas</h1>
          <p class="text-xl text-gray-600">Organiza tu día de estudio</p>
        </div>
        <button @click="showModal = true" class="bg-indigo-600 text-white px-8 py-3 rounded-xl hover:bg-indigo-700 font-semibold shadow-lg hover:shadow-xl">
          + Nueva Tarea
        </button>
      </div>

      <!-- Filters -->
      <div class="mb-8 flex gap-4">
        <button @click="filter = 'all'" :class="['px-6 py-2 rounded-xl font-medium transition-all', filter === 'all' ? 'bg-indigo-600 text-white shadow-lg' : 'bg-gray-100 hover:bg-gray-200']">
          Todas
        </button>
        <button @click="filter = 'pending'" :class="['px-6 py-2 rounded-xl font-medium transition-all', filter === 'pending' ? 'bg-orange-500 text-white shadow-lg' : 'bg-gray-100 hover:bg-gray-200']">
          Pendientes
        </button>
        <button @click="filter = 'completed'" :class="['px-6 py-2 rounded-xl font-medium transition-all', filter === 'completed' ? 'bg-green-500 text-white shadow-lg' : 'bg-gray-100 hover:bg-gray-200']">
          Completadas
        </button>
      </div>

      <!-- Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="task in filteredTasks" :key="task.id" @click="editTask(task)" class="group cursor-pointer">
          <div class="bg-white rounded-2xl p-8 shadow-lg hover:shadow-2xl hover:-translate-y-2 transition-all h-full border" :class="task.completed ? 'border-green-200 bg-green-50/50' : 'border-gray-200'">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center space-x-3">
                <div class="w-12 h-12 rounded-xl flex items-center justify-center font-bold text-sm" :class="task.completed ? 'bg-green-100 text-green-700' : 'bg-indigo-100 text-indigo-700'">
                  {{ task.name.substring(0,2).toUpperCase() }}
                </div>
                <div>
                  <h3 class="font-bold text-xl text-gray-900 line-clamp-1 group-hover:text-indigo-600">{{ task.name }}</h3>
                  <p class="text-sm text-gray-500">{{ formatDate(task.created_at) }}</p>
                </div>
              </div>
              <button @click.stop="toggleComplete(task)" class="w-12 h-12 rounded-xl flex items-center justify-center shadow-md transition-all" :class="task.completed ? 'bg-green-500 text-white hover:bg-green-600 shadow-green-300' : 'bg-gray-200 hover:bg-gray-300'">
                <svg v-if="task.completed" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </button>
            </div>
            <p class="text-gray-700 leading-relaxed line-clamp-3 mb-6">{{ task.description }}</p>
            <div class="flex items-center justify-between">
              <span class="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm font-medium">
                Prioridad {{ task.priority || 'Media' }}
              </span>
              <button @click.stop="deleteTask(task)" class="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-xl transition-all">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m7-10V4a1 1 0 00-1-1h-4m-2 0H9m-7 1a1 1 0 001 1h12a1 1 0 001-1V5a1 1 0 00-1-1H8a1 1 0 00-1 1z" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <div v-if="filteredTasks.length === 0" class="col-span-full flex flex-col items-center justify-center py-24 border-2 border-dashed border-gray-300 rounded-3xl">
          <div class="w-20 h-20 bg-indigo-100 rounded-2xl flex items-center justify-center mb-6">
            <svg class="w-10 h-10 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012 2h2a2 2 0 012-2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">{{ filter === 'pending' ? 'Sin tareas pendientes' : 'Sin tareas completadas' }}</h3>
          <p class="text-gray-600 mb-8">{{ filter === 'all' ? 'Crea tu primera tarea' : 'Marca tareas como completadas' }}</p>
          <button @click="showModal = true" class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-8 py-4 rounded-2xl font-semibold shadow-xl hover:shadow-2xl">
            + Nueva tarea
          </button>
        </div>
      </div>

      <!-- Modal -->
      <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-3xl max-w-md w-full max-h-[90vh] overflow-hidden shadow-2xl">
          <div class="p-8">
            <div class="flex items-center justify-between mb-8">
              <h2 class="text-2xl font-bold text-gray-900">{{ editing ? 'Editar' : 'Nueva' }} Tarea</h2>
              <button @click="closeModal" class="text-gray-400 hover:text-gray-600 p-2">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <form @submit.prevent="saveTask">
              <div class="mb-6">
                <label class="block text-sm font-semibold text-gray-700 mb-2">Nombre *</label>
                <input v-model="form.name" required class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500">
              </div>
              <div class="mb-6">
                <label class="block text-sm font-semibold text-gray-700 mb-2">Descripción</label>
                <textarea v-model="form.description" rows="4" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500"></textarea>
              </div>
              <div class="mb-6">
                <label class="block text-sm font-semibold text-gray-700 mb-2">Prioridad</label>
                <select v-model="form.priority" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500">
                  <option value="Alta">Alta</option>
                  <option value="Media">Media</option>
                  <option value="Baja">Baja</option>
                </select>
              </div>
              <div class="flex gap-3 justify-end">
                <button type="button" @click="closeModal" class="flex-1 px-6 py-3 bg-gray-200 text-gray-800 rounded-xl hover:bg-gray-300">
                  Cancelar
                </button>
                <button type="submit" :disabled="saving" class="flex-1 px-6 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 shadow-lg disabled:opacity-50">
                  {{ saving ? 'Guardando...' : 'Guardar' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import api from '@/services/api'
import type { AxiosResponse } from 'axios'

interface Task {
  id: number
  name: string
  description: string
  completed: boolean
  created_at: string
  priority?: string
}

const tasks = ref<Task[]>([])
const searchTerm = ref('')
const filter = ref<'all' | 'pending' | 'completed'>('all')
const showModal = ref(false)
const editing = ref<number | null>(null)
const form = ref({ name: '', description: '', priority: 'Media' })
const saving = ref(false)

const filteredTasks = computed(() => {
  let filtered = tasks.value.filter(task => 
    task.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    task.description.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
  
  if (filter.value === 'pending') filtered = filtered.filter(task => !task.completed)
  if (filter.value === 'completed') filtered = filtered.filter(task => task.completed)
  
  return filtered
})

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('es-ES', { 
    day: 'numeric', 
    month: 'short' 
  })
}

const loadTasks = async () => {
  try {
    const response = await api.get('/tasks/')
    tasks.value = response.data
  } catch (error) {
    console.error('Error loading tasks:', error)
  }
}

const toggleComplete = async (task: Task) => {
  try {
    task.completed = !task.completed
    await api.post(`/tasks/edit/${task.id}/`, { completed: task.completed })
  } catch (error) {
    console.error('Error updating task:', error)
    loadTasks() // Reload
  }
}

const closeModal = () => {
  editing.value = null
  form.value = { name: '', description: '', priority: 'Media' }
  showModal.value = false
}

const editTask = (task: Task) => {
  editing.value = task.id
  form.value = { 
    name: task.name, 
    description: task.description || '', 
    priority: task.priority || 'Media' 
  }
  showModal.value = true
}

const deleteTask = async (task: Task) => {
  if (confirm('¿Eliminar esta tarea?')) {
    try {
      await api.post(`/tasks/delete/${task.id}/`)
      tasks.value = tasks.value.filter(t => t.id !== task.id)
    } catch (error) {
      console.error('Error deleting task:', error)
    }
  }
}

const saveTask = async () => {
  saving.value = true
  try {
    const data = new FormData()
    data.append('name', form.value.name)
    data.append('description', form.value.description)
    data.append('priority', form.value.priority)
    
    if (editing.value) {
      await api.post(`/tasks/edit/${editing.value}/`, data)
    } else {
      await api.post('/tasks/create/', data)
    }
    
    await loadTasks()
    closeModal()
  } catch (error) {
    console.error('Error saving task:', error)
    alert('Error al guardar tarea')
  } finally {
    saving.value = false
  }
}

onMounted(loadTasks)
</script>

<style scoped>
.line-clamp-1, .line-clamp-3 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.line-clamp-1 {
  -webkit-line-clamp: 1;
}
.line-clamp-3 {
  -webkit-line-clamp: 3;
}
</style>
