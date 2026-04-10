
<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-purple-50 to-pink-100">
    <div class="max-w-md w-full space-y-8 p-8 bg-white rounded-3xl shadow-2xl">
      <div>
        <div class="mx-auto h-20 w-20 bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl flex items-center justify-center shadow-xl">
          <svg class="h-10 w-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <h2 class="mt-6 text-center text-3xl font-bold text-gray-900">Únete a KnowFlow</h2>
        <p class="mt-2 text-center text-sm text-gray-600">Crea tu cuenta gratuita para empezar a estudiar</p>
      </div>
      <form @submit.prevent="signup" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Usuario *</label>
          <input 
            v-model="form.username" 
            required 
            class="w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent appearance-none shadow-sm" 
            placeholder="nombre de usuario"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Email *</label>
          <input 
            v-model="form.email" 
            type="email" 
            required 
            class="w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent appearance-none shadow-sm" 
            placeholder="tu-email@ejemplo.com"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Contraseña *</label>
          <input 
            v-model="form.password" 
            type="password" 
            required 
            class="w-full px-4 py-3 border border-gray-300 placeholder-gray-400 text-gray-900 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent appearance-none shadow-sm" 
            placeholder="tu contraseña"
          />
        </div>
        <div v-if="error" class="p-4 bg-red-50 border-l-4 border-red-400 rounded-xl">
          {{ error }}
        </div>
        <button
          type="submit" 
          :disabled="loading"
          class="group w-full flex items-center justify-center py-3 px-4 border border-transparent text-sm font-bold rounded-xl text-white bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="loading" class="flex items-center space-x-2">
            <svg class="animate-spin -ml-1 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12c0-3.042 1.135-5.824 3 5.291z"></path>
            </svg>
            Creando cuenta...
          </span>
          <span v-else>Crear Cuenta</span>
        </button>
      </form>
      <div class="text-center pt-6 border-t border-gray-200">
        <router-link to="/login" class="text-sm text-purple-600 hover:text-purple-700 font-medium">
          ¿Ya tienes cuenta? Inicia sesión
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()
const form = ref({
  username: '',
  email: '',
  password: ''
})
const loading = ref(false)
const error = ref('')

const signup = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await api.post('/accounts/api/signup/', form.value)
    if (response.data.success) {
      alert(`¡Cuenta creada! Usuario: ${response.data.user.username}\nRedirigiendo al dashboard...`)
      router.push('/dashboard')
    } else {
      error.value = response.data.error || 'Error en registro'
    }
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Error al crear cuenta'
  } finally {
    loading.value = false
  }
}
</script>

