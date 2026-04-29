<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-950 dark:to-slate-900 transition-colors duration-500">
    <div class="max-w-md w-full space-y-10 p-12 bg-white dark:bg-gray-800 rounded-[3rem] shadow-2xl border border-gray-100 dark:border-gray-700 relative overflow-hidden">
      <!-- Decorator -->
      <div class="absolute top-0 left-0 w-32 h-32 bg-indigo-600/5 rounded-full -ml-16 -mt-16"></div>
      
      <div class="relative">
        <div class="w-20 h-20 bg-indigo-600 rounded-3xl flex items-center justify-center shadow-xl shadow-indigo-500/30 mx-auto mb-8">
          <span class="text-3xl font-black text-white">KF</span>
        </div>
        <h2 class="text-4xl font-black text-gray-900 dark:text-white text-center tracking-tight mb-2">Crear Cuenta</h2>
        <p class="text-gray-500 dark:text-gray-400 text-center font-medium">Únete a la comunidad de KnowFlow</p>
      </div>

      <form @submit.prevent="signup" class="space-y-6 relative">
        <div class="space-y-2">
          <label class="text-xs font-black text-gray-400 dark:text-gray-500 uppercase tracking-[0.2em] ml-1">Usuario</label>
          <input v-model="form.username" type="text" placeholder="Cómo te llamaremos" required 
            class="w-full px-6 py-4 bg-gray-50 dark:bg-gray-900 border border-transparent dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white dark:focus:bg-gray-800 dark:text-white transition-all outline-none font-bold"
          >
        </div>
        
        <div class="space-y-2">
          <label class="text-xs font-black text-gray-400 dark:text-gray-500 uppercase tracking-[0.2em] ml-1">Email</label>
          <input v-model="form.email" type="email" placeholder="tu@email.com" required 
            class="w-full px-6 py-4 bg-gray-50 dark:bg-gray-900 border border-transparent dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white dark:focus:bg-gray-800 dark:text-white transition-all outline-none font-bold"
          >
        </div>

        <div class="space-y-2">
          <label class="text-xs font-black text-gray-400 dark:text-gray-500 uppercase tracking-[0.2em] ml-1">Contraseña</label>
          <input v-model="form.password" type="password" placeholder="••••••••" required 
            class="w-full px-6 py-4 bg-gray-50 dark:bg-gray-900 border border-transparent dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:bg-white dark:focus:bg-gray-800 dark:text-white transition-all outline-none font-bold"
          >
        </div>
        
        <button type="submit" :disabled="loading" 
          class="w-full bg-indigo-600 text-white py-5 px-6 rounded-2xl font-black text-lg shadow-xl shadow-indigo-500/20 hover:bg-indigo-700 transition-all active:scale-95 disabled:opacity-50 flex items-center justify-center mt-10"
        >
          <span v-if="loading" class="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
          <span v-else>COMENZAR AHORA</span>
        </button>
        
        <p v-if="error" class="text-rose-600 dark:text-rose-400 text-sm font-black text-center mt-4 bg-rose-50 dark:bg-rose-900/20 py-3 rounded-xl border border-rose-100 dark:border-rose-900/20">{{ error }}</p>
      </form>
      
      <div class="text-center pt-6">
        <p class="text-gray-500 dark:text-gray-400 font-bold text-sm">
          ¿Ya tienes cuenta? 
          <router-link to="/login" class="text-indigo-600 dark:text-indigo-400 hover:underline ml-1">Inicia sesión</router-link>
        </p>
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
    const payload = {
      username: form.value.username,
      email: form.value.email,
      password: form.value.password
    }

    const response = await api.post('signup/', payload)

    if (response.data.success) {
      form.value = { username: '', email: '', password: '' }
      await authStore.checkAuth()
      router.push('/dashboard')
    } else {
      error.value = 'Error en el registro. Revisa los datos.'
    }
  } catch (err) {
    const data = err.response?.data
    error.value = data?.error || 'Error al crear cuenta. Intenta de nuevo.'
  } finally {
    loading.value = false
  }
}
</script>
