<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-blue-50 to-indigo-100">
    <div class="max-w-md w-full space-y-8">
      <div>
        <div class="mx-auto h-20 w-20 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center">
          <svg class="h-10 w-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
          </svg>
        </div>
        <h2 class="mt-6 text-center text-3xl font-bold text-gray-900">Inicia sesión en KnowFlow</h2>
        <p class="mt-2 text-center text-sm text-gray-600">Accede a tus librerías y contenido de estudio</p>
      </div>
      <form @submit.prevent="login" class="mt-8 space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700 mb-2">Usuario</label>
          <input
            v-model="form.username"
            type="text"
            required
            class="appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent shadow-sm"
            placeholder="Tu usuario"
          />
        </div>
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-2">Contraseña</label>
          <input
            v-model="form.password"
            type="password"
            required
            class="appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent shadow-sm"
            placeholder="Tu contraseña"
          />
        </div>
        <div v-if="error" class="text-red-600 text-sm p-3 bg-red-50 border border-red-200 rounded-xl">
          {{ error }}
        </div>
        <button
          type="submit"
          :disabled="loading"
          class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-all duration-200 shadow-xl hover:shadow-2xl hover:-translate-y-0.5"
        >
          <span v-if="loading" class="flex items-center space-x-2">
            <svg class="animate-spin -ml-1 h-5 w-5" fill="none" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" pathLength="1" class="opacity-25" />
              <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" class="opacity-75" pathLength="1" />
            </svg>
            <span>Iniciando...</span>
          </span>
          <span v-else>Acceder</span>
        </button>
      </form>
<div class="text-center">
        <router-link to="/signup" class="text-sm text-primary-600 hover:text-primary-700 font-medium">¿No tienes cuenta? Regístrate</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

const login = async () => {
  loading.value = true
  error.value = ''
  
  const success = await authStore.login(form.value)
  
  loading.value = false
  
  if (success) {
    router.push('/dashboard')
  } else {
    error.value = 'Credenciales inválidas. Intenta de nuevo.'
  }
}
</script>
