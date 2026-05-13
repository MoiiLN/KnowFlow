<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto py-12 lg:py-16 px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center mb-12">
        <div>
          <h1 class="text-4xl font-black text-gray-900 dark:text-white mb-2 tracking-tight">Tareas</h1>
          <p class="text-xl text-gray-500 dark:text-gray-400 font-medium">Organiza tu día de estudio</p>
        </div>
        <button @click="showModal = true" class="bg-indigo-600 text-white px-8 py-3 rounded-xl hover:bg-indigo-700 font-semibold shadow-lg hover:shadow-xl">
          + Nueva Tarea
        </button>
      </div>

      <!-- Filters -->
      <div class="mb-12 flex flex-wrap gap-4">
        <button @click="filter = 'all'" :class="['px-8 py-3 rounded-2xl font-black transition-all active:scale-95 text-sm uppercase tracking-widest', filter === 'all' ? 'bg-indigo-600 text-white shadow-xl shadow-indigo-500/20' : 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700']">
          Todas
        </button>
        <button @click="filter = 'pending'" :class="['px-8 py-3 rounded-2xl font-black transition-all active:scale-95 text-sm uppercase tracking-widest', filter === 'pending' ? 'bg-orange-500 text-white shadow-xl shadow-orange-500/20' : 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700']">
          Pendientes
        </button>
        <button @click="filter = 'completed'" :class="['px-8 py-3 rounded-2xl font-black transition-all active:scale-95 text-sm uppercase tracking-widest', filter === 'completed' ? 'bg-green-500 text-white shadow-xl shadow-green-500/20' : 'bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700']">
          Completadas
        </button>
      </div>

      <!-- Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="task in filteredTasks" :key="task.id" @click="editTask(task)" class="group cursor-pointer">
          <div class="bg-white dark:bg-gray-800 rounded-[2.5rem] p-10 shadow-sm hover:shadow-2xl hover:-translate-y-2 transition-all h-full border border-gray-100 dark:border-gray-700 duration-500" :class="task.completed ? 'border-green-200 dark:border-green-900 bg-green-50/30 dark:bg-green-900/10' : ''">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center space-x-3">
                <div class="w-14 h-14 rounded-2xl flex items-center justify-center font-black text-lg shadow-inner" :class="task.completed ? 'bg-green-100 dark:bg-green-900/40 text-green-700 dark:text-green-400' : 'bg-indigo-100 dark:bg-indigo-900/40 text-indigo-700 dark:text-indigo-400'">
                  {{ task.name.substring(0,2).toUpperCase() }}
                </div>
                <div>
                  <h3 class="font-black text-2xl text-gray-900 dark:text-white line-clamp-1 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">{{ task.name }}</h3>
                  <p class="text-sm text-gray-400 dark:text-gray-500 font-bold uppercase tracking-widest">{{ formatDate(task.created_at) }}</p>
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
            <p class="text-gray-500 dark:text-gray-400 font-medium leading-relaxed line-clamp-3 mb-10">{{ task.description }}</p>
            <div class="flex items-center justify-between">
              <span class="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm font-medium">
                Prioridad {{ task.priority || 'Media' }}
              </span>
              <button @click.stop="deleteTask(task)" 
                :class="[
                  'p-2 rounded-xl transition-all duration-300',
                  confirmingDelete === task.id 
                    ? 'bg-red-500 text-white shadow-lg scale-110 animate-pulse' 
                    : 'text-gray-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/30'
                ]">
                <svg v-if="confirmingDelete !== task.id" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m7-10V4a1 1 0 00-1-1h-4m-2 0H9m-7 1a1 1 0 001 1h12a1 1 0 001-1V5a1 1 0 00-1-1H8a1 1 0 00-1 1z" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
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
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 overflow-y-auto">
      <div class="fixed inset-0 bg-gray-900/60 backdrop-blur-md transition-opacity" @click="closeModal"></div>
      
      <div class="bg-white dark:bg-gray-800 rounded-[2.5rem] shadow-2xl w-full max-w-2xl transform transition-all relative overflow-hidden border border-gray-100 dark:border-gray-700">
        <!-- Decoration -->
        <div class="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600"></div>
        
        <div class="p-8 sm:p-10">
          <div class="flex justify-between items-center mb-8">
            <div>
              <h2 class="text-3xl font-black text-gray-900 dark:text-white tracking-tight">{{ editing ? 'Editar' : 'Nueva' }} Tarea</h2>
              <p class="text-gray-500 dark:text-gray-400 font-medium">Organiza tus objetivos de hoy</p>
            </div>
            <button @click="closeModal" class="p-3 bg-gray-50 dark:bg-gray-900 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 rounded-2xl transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit.prevent="saveTask" class="space-y-8">
            <!-- Name Input -->
            <div class="space-y-3">
              <label class="text-xs font-black text-gray-400 dark:text-gray-500 uppercase tracking-widest px-1">Nombre de la Tarea</label>
              <input 
                v-model="form.name" 
                required 
                placeholder="¿Qué tienes que hacer?"
                class="w-full px-6 py-4 bg-gray-50 dark:bg-gray-900 border border-transparent dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white dark:focus:bg-gray-800 dark:text-white transition-all outline-none font-medium text-lg"
              >
            </div>

            <!-- Description -->
            <div class="space-y-3">
              <label class="text-xs font-black text-gray-400 dark:text-gray-500 uppercase tracking-widest px-1">Descripción Detallada</label>
              <textarea 
                v-model="form.description" 
                rows="6" 
                placeholder="Añade más detalles sobre esta tarea..."
                class="w-full px-6 py-4 bg-gray-50 dark:bg-gray-900 border border-transparent dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white dark:focus:bg-gray-800 dark:text-white transition-all outline-none font-medium resize-none"
              ></textarea>
            </div>

            <!-- Options Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-3">
                <label class="text-xs font-black text-gray-400 dark:text-gray-500 uppercase tracking-widest px-1">Prioridad</label>
                <div class="relative">
                  <select 
                    v-model="form.priority" 
                    class="w-full appearance-none px-6 py-4 bg-gray-50 dark:bg-gray-900 border border-transparent dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white dark:focus:bg-gray-800 dark:text-white transition-all outline-none font-medium"
                  >
                    <option value="Alta">Alta 🔥</option>
                    <option value="Media">Media ⚡</option>
                    <option value="Baja">Baja 🌱</option>
                  </select>
                  <div class="absolute right-6 top-1/2 -translate-y-1/2 pointer-events-none text-gray-400">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            <!-- Footer Buttons -->
            <div class="flex gap-4 pt-4">
              <button 
                type="button" 
                @click="closeModal" 
                class="flex-1 px-8 py-4 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded-2xl font-bold hover:bg-gray-200 dark:hover:bg-gray-600 transition-all"
              >
                Cancelar
              </button>
              <button 
                type="submit" 
                :disabled="saving" 
                class="flex-[2] px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-2xl font-bold shadow-xl shadow-indigo-500/20 hover:shadow-2xl hover:shadow-indigo-500/40 hover:-translate-y-0.5 active:translate-y-0 transition-all disabled:opacity-50"
              >
                <div class="flex items-center justify-center gap-2">
                  <svg v-if="saving" class="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ saving ? 'Guardando...' : (editing ? 'Actualizar Tarea' : 'Crear Tarea') }}
                </div>
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
import { useRouter } from 'vue-router'
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
    const response = await api.get('tasks/')
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

const confirmingDelete = ref<number | null>(null)

const deleteTask = async (task: Task) => {
  if (confirmingDelete.value !== task.id) {
    confirmingDelete.value = task.id
    // Reset after 3 seconds if not clicked again
    setTimeout(() => {
      if (confirmingDelete.value === task.id) confirmingDelete.value = null
    }, 3000)
    return
  }

  try {
    await api.post(`/tasks/${task.id}/delete/`)
    tasks.value = tasks.value.filter(t => t.id !== task.id)
    confirmingDelete.value = null
  } catch (error) {
    console.error('Error deleting task:', error)
  }
}

const router = useRouter()

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
      await api.post('tasks/create/', data)
    }
    
    await loadTasks()
    closeModal()
    router.push('/planner')
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
