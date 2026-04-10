<template>
  <DefaultLayout>
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-8">
        <div>
          <h1 class="text-4xl font-bold text-gray-900 mb-2">Tareas</h1>
          <p class="text-xl text-gray-600 mb-2">Gestiona tus objetivos de estudio</p>
          <div class="text-sm text-green-600 font-medium">¡{{ completedToday }} tareas completadas hoy!</div>
        </div>
        <Button @click="showCreateModal = true" class="w-full lg:w-auto">
          + Nueva Tarea
        </Button>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div class="card p-6 text-center">
          <div class="text-3xl font-bold text-primary-600 mb-1">{{ pendingTasks }}</div>
          <div class="text-sm text-gray-600 uppercase tracking-wide">Pendientes</div>
        </div>
        <div class="card p-6 text-center">
          <div class="text-3xl font-bold text-green-600 mb-1">{{ completedTasks }}</div>
          <div class="text-sm text-gray-600 uppercase tracking-wide">Completadas</div>
        </div>
        <div class="card p-6 text-center">
          <div class="text-3xl font-bold text-orange-600 mb-1">{{ overdueTasks }}</div>
          <div class="text-sm text-gray-600 uppercase tracking-wide">Atrasadas</div>
        </div>
        <div class="card p-6 text-center">
          <div class="text-3xl font-bold text-gray-600 mb-1">{{ totalTasks }}</div>
          <div class="text-sm text-gray-600 uppercase tracking-wide">Total</div>
        </div>
      </div>

      <!-- Tasks List -->
      <div class="space-y-3">
        <div 
          v-for="task in filteredTasks" 
          :key="task.id"
          class="group card p-6 hover:shadow-xl transition-all relative overflow-hidden"
        >
          <div class="flex items-start space-x-4">
            <!-- Checkbox -->
            <button 
              @click="toggleTask(task.id)"
              class="relative flex-shrink-0 w-6 h-6 mt-0.5 rounded-lg border-2 transition-all duration-200"
              :class="[
                task.completed 
                  ? 'border-green-400 bg-green-400' 
                  : 'border-gray-300 hover:border-primary-400 focus:border-primary-400 focus:ring-2 focus:ring-primary-400'
              ]"
            >
              <svg v-if="task.completed" class="w-4 h-4 text-white absolute inset-0 m-auto" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
            </button>

            <!-- Task Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between mb-1">
                <h3 
                  :class="[
                    'font-bold text-lg', 
                    task.completed ? 'line-through text-gray-500' : 'text-gray-900 group-hover:text-primary-600'
                  ]"
                >
                  {{ task.title }}
                </h3>
                <span v-if="task.due_date" class="px-2 py-1 rounded-full text-xs font-medium ml-2"
                  :class="isOverdue(task.due_date) ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'">
                  {{ formatDate(task.due_date) }}
                </span>
              </div>
              <p v-if="task.description" class="text-gray-600 mb-3 line-clamp-2">{{ task.description }}</p>
              <div class="flex items-center text-xs text-gray-500 space-x-4">
                <span>{{ formatDate(task.created_at) }}</span>
                <span v-if="task.completed">{{ formatDate(task.completed_at) }} ✓</span>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center space-x-2 ml-4 flex-shrink-0">
              <Button size="sm" variant="outline" @click.stop="editTask(task)">Editar</Button>
              <Button size="sm" variant="danger" @click.stop="deleteTask(task.id)">Eliminar</Button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!filteredTasks.length" class="text-center py-24 border-2 border-dashed border-gray-200 rounded-3xl">
        <div class="w-24 h-24 bg-gradient-to-r from-emerald-100 to-teal-100 rounded-3xl flex items-center justify-center mx-auto mb-6">
          <svg class="w-12 h-12 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <h3 class="text-2xl font-bold text-gray-900 mb-2">¡Sin tareas pendientes!</h3>
        <p class="text-gray-600 mb-6">Estás al día con tus objetivos. ¿Quieres añadir alguna tarea nueva?</p>
        <Button @click="showCreateModal = true">Nueva tarea</Button>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-3xl shadow-2xl max-w-md w-full">
        <div class="p-8">
          <h2 class="text-2xl font-bold text-gray-900 mb-6">{{ editingTask ? 'Editar Tarea' : 'Nueva Tarea' }}</h2>
          <form @submit.prevent="saveTask" class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Título *</label>
              <input
                v-model="form.title"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Descripción</label>
              <textarea
                v-model="form.description"
                rows="3"
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500"
              ></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Fecha límite (opcional)</label>
              <input type="date" v-model="form.due_date" class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500" />
            </div>
            <div class="flex space-x-3">
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
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import Button from '@/components/Button.vue'
import { taskService } from '@/services/api'
import type { Task } from '@/types/index'

const tasks = ref<Task[]>([])
const searchTerm = ref('')
const showCreateModal = ref(false)
const editingTask = ref<Task | null>(null)
const form = ref({ title: '', description: '', due_date: '' as string | null })
const saving = ref(false)

const filteredTasks = computed(() => {
  return tasks.value.filter(task => 
    task.title.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    task.description?.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

const stats = computed(() => {
  const total = tasks.value.length
  const completed = tasks.value.filter(t => t.completed).length
  const pending = total - completed
  const overdue = tasks.value.filter(t => !t.completed && t.due_date && isOverdue(t.due_date)).length
  const completedToday = tasks.value.filter(t => t.completed && isToday(t.completed_at)).length
  
  return { total, completed, pending, overdue, completedToday }
})

const loadTasks = async () => {
  try {
    const response = await taskService.getAll()
    tasks.value = response.data
  } catch (error) {
    console.error('Error loading tasks:', error)
  }
}

const toggleTask = async (id: number) => {
  const task = tasks.value.find(t => t.id === id)
  if (task) {
    task.completed = !task.completed
    if (task.completed) {
      task.completed_at = new Date().toISOString()
    }
    await taskService.update(id.toString(), task)
  }
}

const editTask = (task: Task) => {
  editingTask.value = task
  form.value = {
    title: task.title,
    description: task.description || '',
    due_date: task.due_date || ''
  }
  showCreateModal.value = true
}

const deleteTask = async (id: number) => {
  if (confirm('¿Eliminar esta tarea?')) {
    await taskService.delete(id.toString())
    loadTasks()
  }
}

const saveTask = async () => {
  saving.value = true
  try {
    if (editingTask.value) {
      await taskService.update(editingTask.value.id.toString(), form.value)
    } else {
      await taskService.create(form.value)
    }
    closeModal()
    loadTasks()
  } catch (error) {
    console.error('Error saving task:', error)
  } finally {
    saving.value = false
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingTask.value = null
  form.value = { title: '', description: '', due_date: '' }
}

const isOverdue = (dateString: string) => {
  return new Date(dateString) < new Date()
}

const isToday = (dateString: string) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const date = new Date(dateString)
  date.setHours(0, 0, 0, 0)
  return today.getTime() === date.getTime()
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('es-ES', { 
    day: 'numeric', 
    month: 'short' 
  })
}

onMounted(loadTasks)
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
