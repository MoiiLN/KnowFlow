<template>
  <div>
    <Navbar />

    <div class="min-h-screen bg-gray-100 pt-28 px-6 md:px-8 pb-12">
      <div class="max-w-7xl mx-auto">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6 mb-10">
          <div>
            <h1 class="text-4xl md:text-5xl font-black text-gray-900 tracking-tight">
              Planner Mensual
            </h1>
            <p class="text-lg md:text-xl text-gray-500 mt-2 font-medium">
              Organiza tus tareas y objetivos de forma inteligente
            </p>
          </div>

          <button
            @click="openNewTaskModal(selectedDate || today)"
            class="bg-blue-600 hover:bg-blue-700 text-white font-black px-8 py-4 rounded-2xl shadow-lg shadow-blue-500/20 transition-all hover:-translate-y-1"
          >
            + Nueva Tarea
          </button>
        </div>

        <div class="grid grid-cols-1 xl:grid-cols-4 gap-8">
          <!-- Calendar -->
          <div class="xl:col-span-3 bg-white rounded-[2rem] shadow-sm border border-gray-100 p-6 md:p-8">
            <!-- Navigation -->
            <div class="flex items-center justify-between mb-8">
              <button
                @click="changeMonth(-1)"
                class="w-12 h-12 rounded-2xl bg-gray-100 hover:bg-gray-200 flex items-center justify-center text-gray-700 font-bold transition"
              >
                ←
              </button>

              <h2 class="text-2xl md:text-3xl font-black text-gray-900 capitalize">
                {{ currentMonthLabel }}
              </h2>

              <button
                @click="changeMonth(1)"
                class="w-12 h-12 rounded-2xl bg-gray-100 hover:bg-gray-200 flex items-center justify-center text-gray-700 font-bold transition"
              >
                →
              </button>
            </div>

            <!-- Weekdays -->
            <div class="grid grid-cols-7 gap-3 mb-4">
              <div
                v-for="day in weekDays"
                :key="day"
                class="text-center text-xs font-black uppercase tracking-widest text-gray-400 py-3"
              >
                {{ day }}
              </div>
            </div>

            <div class="grid grid-cols-7 gap-3">
              <div
                v-for="day in calendarDays"
                :key="day.date"
                @click="selectDay(day.date)"
                class="min-h-[130px] rounded-3xl border p-3 transition cursor-pointer"
                :class="[
                  day.isCurrentMonth
                    ? 'bg-gray-50 border-gray-100 hover:bg-blue-50'
                    : 'bg-gray-50/50 border-gray-50 text-gray-300',
                  selectedDate === day.date ? '!border-blue-500 ring-2 ring-blue-100' : ''
                ]"
              >
                <div class="flex justify-between items-center mb-3">
                  <span
                    class="text-sm font-black"
                    :class="
                      day.isToday
                        ? 'text-blue-600'
                        : day.isCurrentMonth
                        ? 'text-gray-800'
                        : 'text-gray-300'
                    "
                  >
                    {{ day.day }}
                  </span>

                  <span
                    v-if="day.isToday"
                    class="w-2 h-2 bg-blue-600 rounded-full"
                  ></span>
                </div>

                <div class="space-y-2">
                  <div
                    v-for="task in day.tasks.slice(0, 3)"
                    :key="task.id"
                    @click.stop="openEditTaskModal(task)"
                    class="text-xs font-bold px-3 py-2 rounded-2xl truncate"
                    :class="priorityClasses(task.priority)"
                  >
                    {{ task.name }}
                  </div>

                  <div
                    v-if="day.tasks.length > 3"
                    class="text-xs font-bold text-gray-400 px-2"
                  >
                    +{{ day.tasks.length - 3 }} más
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="space-y-8">
            <div class="bg-white rounded-[2rem] shadow-sm border border-gray-100 p-6">
              <div class="flex items-center justify-between mb-6">
                <h3 class="text-2xl font-black text-gray-900">Próximas</h3>
              </div>

              <div class="space-y-4">
                <div
                  v-for="task in upcomingTasks"
                  :key="task.id"
                  @click="openEditTaskModal(task)"
                  class="p-4 rounded-3xl bg-gray-50 border border-gray-100 cursor-pointer hover:bg-gray-100 transition"
                >
                  <div class="flex items-start justify-between mb-2">
                    <h4 class="font-black text-gray-900 text-sm truncate">
                      {{ task.name }}
                    </h4>

                    <span
                      class="w-3 h-3 rounded-full ml-2"
                      :class="dotPriority(task.priority)"
                    ></span>
                  </div>

                  <p class="text-xs text-gray-500 font-medium">
                    {{ formatDisplayDate(task.due_date) }}
                  </p>
                </div>

                <p
                  v-if="!upcomingTasks.length"
                  class="text-sm text-gray-400 font-medium"
                >
                  No hay tareas próximas.
                </p>
              </div>
            </div>

            <!-- Stats -->
            <div class="bg-white rounded-[2rem] shadow-sm border border-gray-100 p-6">
              <h3 class="text-2xl font-black text-gray-900 mb-6">
                Objetivos
              </h3>

              <div class="space-y-5">
                <div>
                  <div class="flex justify-between text-sm font-bold mb-2">
                    <span>Tareas completadas</span>
                    <span>{{ completedPercentage }}%</span>
                  </div>

                  <div class="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      class="h-full bg-blue-600 rounded-full"
                      :style="{ width: completedPercentage + '%' }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div><!-- max-w -->
    </div><!-- main -->

    <!-- Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4"
    >
      <div class="bg-white rounded-[2rem] w-full max-w-lg p-8 shadow-2xl">
        <h3 class="text-3xl font-black text-gray-900 mb-6">
          {{ editingTask ? 'Editar Tarea' : 'Nueva Tarea' }}
        </h3>

        <form @submit.prevent="saveTask" class="space-y-4">
          <input
            v-model="form.name"
            required
            type="text"
            placeholder="Título"
            class="w-full px-5 py-4 rounded-2xl bg-gray-100 border-0 focus:ring-2 focus:ring-blue-500 font-bold"
          />

          <textarea
            v-model="form.description"
            placeholder="Descripción"
            class="w-full px-5 py-4 rounded-2xl bg-gray-100 border-0 focus:ring-2 focus:ring-blue-500 font-medium"
          ></textarea>

          <input
            v-model="form.due_date"
            required
            type="date"
            class="w-full px-5 py-4 rounded-2xl bg-gray-100 border-0 focus:ring-2 focus:ring-blue-500"
          />

          <select
            v-model="form.priority"
            class="w-full px-5 py-4 rounded-2xl bg-gray-100 border-0 focus:ring-2 focus:ring-blue-500 font-bold"
          >
            <option value="low">Prioridad baja</option>
            <option value="medium">Prioridad media</option>
            <option value="high">Prioridad alta</option>
          </select>

          <div class="flex gap-4 pt-4">
            <button
              type="button"
              @click="closeModal"
              class="flex-1 py-4 rounded-2xl bg-gray-100 hover:bg-gray-200 font-black text-gray-700"
            >
              Cancelar
            </button>

            <button
              type="submit"
              class="flex-1 py-4 rounded-2xl bg-blue-600 hover:bg-blue-700 text-white font-black"
            >
              Guardar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Navbar from '@/components/Navbar.vue'
import { ref, computed, onMounted } from 'vue'
import dayjs from 'dayjs'
import 'dayjs/locale/es'
import { taskService } from '@/services/api'

dayjs.locale('es')

const tasks = ref<any[]>([])
const currentDate = ref(dayjs())
const selectedDate = ref(dayjs().format('YYYY-MM-DD'))
const today = dayjs().format('YYYY-MM-DD')

const showModal = ref(false)
const editingTask = ref<any | null>(null)

const form = ref({
  name: '',
  description: '',
  due_date: today,
  priority: 'medium'
})

const weekDays = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']

const currentMonthLabel = computed(() =>
  currentDate.value.format('MMMM YYYY')
)

const calendarDays = computed(() => {
  const startOfMonth = currentDate.value.startOf('month')
  const endOfMonth = currentDate.value.endOf('month')

  const startDate = startOfMonth.startOf('week').add(1, 'day')
  const endDate = endOfMonth.endOf('week').add(1, 'day')

  const days = []
  let day = startDate

  while (day.isBefore(endDate) || day.isSame(endDate, 'day')) {
    const dateStr = day.format('YYYY-MM-DD')

    days.push({
      date: dateStr,
      day: day.date(),
      isToday: dateStr === today,
      isCurrentMonth: day.month() === currentDate.value.month(),
      tasks: tasks.value.filter(task => task.due_date === dateStr)
    })

    day = day.add(1, 'day')
  }

  return days
})

const upcomingTasks = computed(() =>
  [...tasks.value]
    .filter(task =>
      task.due_date &&
      !task.completed &&
      (
        dayjs(task.due_date).isSame(dayjs(), 'day') ||
        dayjs(task.due_date).isAfter(dayjs(), 'day')
      )
    )
    .sort(
      (a, b) =>
        dayjs(a.due_date).unix() - dayjs(b.due_date).unix()
    )
    .slice(0, 5)
)

const completedPercentage = computed(() => {
  if (!tasks.value.length) return 0

  const completed = tasks.value.filter(t => t.completed).length
  return Math.round((completed / tasks.value.length) * 100)
})

const loadTasks = async () => {
  try {
    const response = await taskService.getMonthly(
      currentDate.value.month() + 1,
      currentDate.value.year()
    )

    tasks.value = response.data.map((task: any) => ({
      id: task.id,
      name: task.name,
      description: task.description || '',
      due_date: task.due_date || task.created_at?.split('T')[0],
      priority: task.priority || 'medium',
      completed: task.completed || false
    }))
  } catch (error) {
    console.error('Error cargando tareas:', error)
  }
}

const changeMonth = async (direction: number) => {
  currentDate.value = currentDate.value.add(direction, 'month')
  await loadTasks()
}

const selectDay = (date: string) => {
  selectedDate.value = date
}

const openNewTaskModal = (date: string) => {
  editingTask.value = null

  form.value = {
    name: '',
    description: '',
    due_date: date,
    priority: 'medium'
  }

  showModal.value = true
}

const openEditTaskModal = (task: any) => {
  editingTask.value = task

  form.value = {
    name: task.name,
    description: task.description || '',
    due_date: task.due_date,
    priority: task.priority || 'medium'
  }

  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const saveTask = async () => {
  try {
    let savedTask

    if (editingTask.value) {
      const response = await taskService.update(
        editingTask.value.id,
        form.value
      )

      savedTask = response.data.task

      const index = tasks.value.findIndex(
        t => t.id === editingTask.value.id
      )

      if (index !== -1) {
        tasks.value[index] = {
          ...tasks.value[index],
          ...savedTask,
          due_date: form.value.due_date,
          priority: form.value.priority,
          description: form.value.description
        }
      }
    } else {
      const response = await taskService.create(form.value)

      savedTask = response.data.task

      tasks.value.push({
        id: savedTask.id,
        name: form.value.name,
        description: form.value.description,
        due_date: form.value.due_date,
        priority: form.value.priority,
        completed: false
      })
    }

    tasks.value.sort(
      (a, b) =>
        dayjs(a.due_date).unix() - dayjs(b.due_date).unix()
    )

    closeModal()

    await loadTasks()
  } catch (error) {
    console.error('Error guardando tarea:', error)
  }
}


const formatDisplayDate = (date: string) =>
  dayjs(date).format('DD MMM')

const priorityClasses = (priority: string) => {
  switch (priority) {
    case 'high':
      return 'bg-red-500 text-white'
    case 'low':
      return 'bg-green-500 text-white'
    default:
      return 'bg-blue-600 text-white'
  }
}

const dotPriority = (priority: string) => {
  switch (priority) {
    case 'high':
      return 'bg-red-500'
    case 'low':
      return 'bg-green-500'
    default:
      return 'bg-blue-600'
  }
}
const toggleTaskCompletion = async (task: any) => {
  try {
    const updatedTask = {
      ...task,
      completed: !task.completed
    }

    await taskService.update(task.id, updatedTask)

    const index = tasks.value.findIndex(t => t.id === task.id)

    if (index !== -1) {
      tasks.value[index].completed = updatedTask.completed
    }
  } catch (error) {
    console.error('Error actualizando tarea:', error)
  }
}

onMounted(() => {
  loadTasks()
})
</script>