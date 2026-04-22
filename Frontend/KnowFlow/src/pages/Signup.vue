<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 bg-gradient-to-br from-slate-50 to-blue-50">
    <div class="max-w-md w-full space-y-8 p-8 bg-white rounded-2xl shadow-xl">
      <div>
        <h2 class="text-3xl font-bold text-gray-900 text-center">Crear cuenta</h2>
        <p class="text-gray-600 text-center mt-1">Únete a KnowFlow</p>
      </div>
      <form @submit.prevent="signup" class="space-y-4">
        <div>
          <input v-model="form.username" type="text" placeholder="Usuario" required 
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
        </div>
        <div>
          <input v-model="form.email" type="email" placeholder="Email" required 
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
        </div>
        <div>
          <input v-model="form.password" type="password" placeholder="Contraseña" required 
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
        </div>
        <button type="submit" :disabled="loading" 
          class="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 disabled:opacity-50 flex items-center justify-center"
        >
          <span v-if="loading">Creando...</span>
          <span v-else>Registrarse</span>
        </button>
        <p v-if="error" class="text-red-600 text-sm text-center">{{ error }}</p>
      </form>
      <div class="text-center">
        <router-link to="/login" class="text-blue-600 hover:text-blue-700">Ya tienes cuenta? Inicia sesión</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()
const form = ref({ username: '', email: '', password: '' })
const loading = ref(false)
const error = ref('')

const signup = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await api.post('/accounts/api/signup/', form.value)
    if (response.data.success) {
      // Backend auto-logs in, refresh auth state
      await authStore.checkAuth()
      router.push('/dashboard')
    } else {
      error.value = 'Error en el registro'
    }
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Error al crear cuenta'
  } finally {
    loading.value = false
  }
}
</script>

