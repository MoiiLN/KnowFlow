<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-950 dark:to-slate-900 transition-colors duration-500">
    <div class="max-w-md w-full space-y-10 p-12 bg-white dark:bg-gray-800 rounded-[3rem] shadow-2xl border border-gray-100 dark:border-gray-700 relative overflow-hidden">
      <!-- Decorator -->
      <div class="absolute top-0 right-0 w-32 h-32 bg-blue-600/5 rounded-full -mr-16 -mt-16"></div>
      
      <div class="relative">
        <div class="w-20 h-20 bg-blue-600 rounded-3xl flex items-center justify-center shadow-xl shadow-blue-500/30 mx-auto mb-8">
          <span class="text-3xl font-black text-white">KF</span>
        </div>
        <h2 class="text-4xl font-black text-gray-900 dark:text-white text-center tracking-tight mb-2">Bienvenido</h2>
        <p class="text-gray-500 dark:text-gray-400 text-center font-medium">Inicia sesión en tu cuenta de KnowFlow</p>
      </div>

      <form @submit.prevent="login" class="space-y-6 relative">
        <div class="space-y-2">
          <label class="text-xs font-black text-gray-400 dark:text-gray-500 uppercase tracking-[0.2em] ml-1">Usuario</label>
          <input v-model="form.username" type="text" placeholder="Tu nombre de usuario" required 
            class="w-full px-6 py-4 bg-gray-50 dark:bg-gray-900 border border-transparent dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:bg-white dark:focus:bg-gray-800 dark:text-white transition-all outline-none font-bold"
          >
        </div>
        <div class="space-y-2">
          <label class="text-xs font-black text-gray-400 dark:text-gray-500 uppercase tracking-[0.2em] ml-1">Contraseña</label>
          <input v-model="form.password" type="password" placeholder="••••••••" required 
            class="w-full px-6 py-4 bg-gray-50 dark:bg-gray-900 border border-transparent dark:border-gray-700 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:bg-white dark:focus:bg-gray-800 dark:text-white transition-all outline-none font-bold"
          >
        </div>
        
        <button type="submit" :disabled="loading" 
          class="w-full bg-blue-600 text-white py-5 px-6 rounded-2xl font-black text-lg shadow-xl shadow-blue-500/20 hover:bg-blue-700 transition-all active:scale-95 disabled:opacity-50 flex items-center justify-center mt-10"
        >
          <span v-if="loading" class="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
          <span v-else>ENTRAR AHORA</span>
        </button>
        
        <p v-if="error" class="text-rose-600 dark:text-rose-400 text-sm font-black text-center mt-4 bg-rose-50 dark:bg-rose-900/20 py-3 rounded-xl border border-rose-100 dark:border-rose-900/20">{{ error }}</p>
      </form>
      
      <div class="text-center pt-6">
        <p class="text-gray-500 dark:text-gray-400 font-bold text-sm">
          ¿No tienes cuenta? 
          <router-link to="/signup" class="text-blue-600 dark:text-blue-400 hover:underline ml-1">Regístrate gratis</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const form = ref({ username: '', password: '' })
const loading = ref(false)
const error = ref('')

const login = async () => {
  loading.value = true
  error.value = ''
  try {
    const success = await authStore.login(form.value)
    if (success) {
      router.push('/dashboard')
    } else {
      error.value = 'Usuario o contraseña incorrectos'
    }
  } catch (err) {
    error.value = 'Error al iniciar sesión'
  } finally {
    loading.value = false
  }
}
</script>
