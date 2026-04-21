<template>
  <nav class="bg-white/80 backdrop-blur-md shadow-lg border-b border-gray-100 fixed w-full z-40 top-0">
    <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
      <!-- Logo -->
      <router-link to="/dashboard" class="flex items-center space-x-2 group">
        <div class="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg group-hover:scale-105 transition-all">
          <span class="text-xl font-bold text-white">KF</span>
        </div>
        <h1 class="text-2xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
          KnowFlow
        </h1>
      </router-link>

      <!-- Desktop Nav -->
      <div class="hidden md:flex items-center space-x-8">
        <router-link 
          v-for="item in navItems" 
          :key="item.path"
          :to="item.path" 
          class="px-4 py-2 text-gray-700 font-medium rounded-xl hover:bg-blue-50 hover:text-blue-600 transition-all group"
        >
          {{ item.label }}
        </router-link>
      </div>

      <!-- Right section -->
      <div class="flex items-center space-x-4">
        <template v-if="authStore.user">
          <!-- Profile dropdown -->
          <div class="relative">
            <button @click="showProfileMenu = !showProfileMenu" class="flex items-center space-x-3 p-2 rounded-xl hover:bg-gray-100 transition-colors">
              <div class="w-10 h-10 bg-gradient-to-br from-green-500 to-blue-500 rounded-xl flex items-center justify-center shadow-md">
                <span class="font-semibold text-white text-sm">{{ authStore.user.username.charAt(0).toUpperCase() }}</span>
              </div>
              <span class="font-medium text-gray-900 hidden md:inline">{{ authStore.user.username }}</span>
            </button>
            
            <!-- Profile dropdown menu -->
            <div v-if="showProfileMenu" class="absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-2xl border border-gray-200 z-50 py-1">
              <router-link 
                to="/profile" 
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg font-medium"
                @click="showProfileMenu = false"
              >
                Mi Perfil
              </router-link>
              <div class="border-t border-gray-100 my-1"></div>
              <button 
                @click="logout"
                class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg font-medium transition-colors"
              >
                Cerrar sesión
              </button>
            </div>
          </div>
          
          <!-- Theme Toggle -->
          <button
            @click="$emit('toggle-theme')"
            class="p-2.5 rounded-xl hover:bg-gray-100 transition-all"
            title="Cambiar tema"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </button>
        </template>
        
        <template v-else>
          <router-link 
            to="/login"
            class="px-6 py-2.5 font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-lg hover:shadow-xl transition-all"
          >
            Iniciar Sesión
          </router-link>
        </template>

        <!-- Mobile menu button -->
        <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden p-2 rounded-lg hover:bg-gray-100">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div v-if="mobileMenuOpen" class="md:hidden bg-white border-t border-gray-100 shadow-lg">
      <div class="px-4 py-4 space-y-2">
        <router-link 
          v-for="item in navItems" 
          :key="item.path"
          :to="item.path" 
          class="block px-4 py-3 rounded-xl hover:bg-blue-50 hover:text-blue-600 transition-colors"
          @click="mobileMenuOpen = false"
        >
          {{ item.label }}
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const mobileMenuOpen = ref(false)
const showProfileMenu = ref(false)

const navItems = [
  { label: 'Dashboard', path: '/dashboard' },
  { label: 'Librerías', path: '/libraries' },
  { label: 'Flashcards', path: '/flowcards' },
  { label: 'Notas', path: '/notes' },
  { label: 'Cuestionarios', path: '/knowtionaries' },
  { label: 'Tareas', path: '/tasks' }
]

const logout = async () => {
  showProfileMenu.value = false
  await authStore.logout()
  router.push('/login')
}

onMounted(() => {
  authStore.checkAuth()
})
</script>
