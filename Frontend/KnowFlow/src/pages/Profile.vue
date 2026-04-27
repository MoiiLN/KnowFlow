<template>
  <DefaultLayout>
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-12 relative group">
        <div class="w-32 h-32 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-2xl overflow-hidden relative">
          <img 
            v-if="avatarPreview || authStore.user?.avatar" 
            :src="avatarPreview || authStore.user?.avatar" 
            class="w-full h-full object-cover" 
            alt="Avatar"
          />
          <span v-else class="text-5xl font-bold text-white">{{ authStore.user?.username?.charAt(0).toUpperCase() }}</span>
          
          <label class="absolute inset-0 bg-black/50 text-white flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer">
            <span class="text-sm font-medium">Cambiar</span>
            <input type="file" class="hidden" accept="image/*" @change="handleFileUpload" />
          </label>
        </div>
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-2">{{ authStore.user?.username }}</h1>
      </div>
      
      <div class="grid md:grid-cols-2 gap-8">
        <div class="card p-8 bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">Estadísticas</h3>
          <div class="space-y-6">
            <div>
              <div class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Librerías creadas</div>
              <div class="text-3xl font-bold text-primary-600 dark:text-primary-400">12</div>
            </div>
            <div>
              <div class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Flashcards</div>
              <div class="text-3xl font-bold text-green-600 dark:text-green-400">156</div>
            </div>
            <div>
              <div class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Tareas completadas</div>
              <div class="text-3xl font-bold text-purple-600 dark:text-purple-400">89%</div>
            </div>
          </div>
        </div>
        
        <div class="card p-8 bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">Configuración</h3>
          <form @submit.prevent="saveProfile" class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Nombre de usuario</label>
              <input 
                type="text" 
                :value="authStore.user?.username" 
                class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-gray-50 dark:bg-gray-700 dark:text-white cursor-not-allowed opacity-70"
                disabled 
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Email</label>
              <input 
                v-model="form.email"
                type="email" 
                class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Biografía</label>
              <textarea 
                v-model="form.bio"
                rows="3"
                class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
                placeholder="Cuéntanos sobre ti..."
              ></textarea>
            </div>
            
            <div v-if="successMsg" class="text-green-600 text-sm font-medium">{{ successMsg }}</div>
            <div v-if="errorMsg" class="text-red-600 text-sm font-medium">{{ errorMsg }}</div>

            <button type="submit" :disabled="loading" class="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-6 rounded-xl font-semibold text-lg disabled:opacity-50 transition-colors">
              <span v-if="loading">Guardando...</span>
              <span v-else>Guardar cambios</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const authStore = useAuthStore()

const loading = ref(false)
const successMsg = ref('')
const errorMsg = ref('')

const form = ref({
  email: '',
  bio: ''
})

const avatarFile = ref<File | null>(null)
const avatarPreview = ref<string | null>(null)

const initForm = () => {
  if (authStore.user) {
    form.value.email = authStore.user.email || ''
    form.value.bio = authStore.user.bio || ''
  }
}

onMounted(() => initForm())
watch(() => authStore.user, () => initForm(), { deep: true })

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    const file = target.files[0]
    avatarFile.value = file
    avatarPreview.value = URL.createObjectURL(file)
  }
}

const saveProfile = async () => {
  loading.value = true
  successMsg.value = ''
  errorMsg.value = ''

  try {
    const formData = new FormData()
    formData.append('email', form.value.email)
    formData.append('bio', form.value.bio)
    if (avatarFile.value) {
      formData.append('avatar', avatarFile.value)
    }

    const response = await api.post('profile/edit/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    if (response.data.success) {
      successMsg.value = 'Perfil actualizado correctamente.'
      await authStore.checkAuth()
    } else {
      errorMsg.value = response.data.error || 'Error al guardar.'
    }
  } catch (error: any) {
    errorMsg.value = error.response?.data?.error || 'Error de conexión.'
  } finally {
    loading.value = false
  }
}
</script>

