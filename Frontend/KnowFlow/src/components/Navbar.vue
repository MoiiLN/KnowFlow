
<template>
  <nav class="bg-white shadow-lg fixed w-full z-40 top-0 border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <router-link to="/dashboard" class="flex items-center space-x-2">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
              <span class="text-lg font-bold text-white">KF</span>
            </div>
            <span class="ml-2 text-xl font-bold text-gray-900">KnowFlow</span>
          </router-link>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-8">
          <router-link 
            to="/dashboard" 
            class="px-3 py-2 text-gray-700 font-medium rounded-md hover:bg-gray-100 hover:text-blue-600 transition-colors"
          >
            Dashboard
          </router-link>
          <router-link 
            to="/libraries" 
            class="px-3 py-2 text-gray-700 font-medium rounded-md hover:bg-gray-100 hover:text-blue-600 transition-colors"
          >
            Librerías
          </router-link>
          <router-link 
            to="/flowcards" 
            class="px-3 py-2 text-gray-700 font-medium rounded-md hover:bg-gray-100 hover:text-blue-600 transition-colors"
          >
            Flashcards
          </router-link>
          <router-link 
            to="/notes" 
            class="px-3 py-2 text-gray-700 font-medium rounded-md hover:bg-gray-100 hover:text-blue-600 transition-colors"
          >
            Notas
          </router-link>

          <router-link 
            to="/knowtionaries" 
            class="px-3 py-2 text-gray-700 font-medium rounded-md hover:bg-gray-100 hover:text-blue-600 transition-colors"
          >
            Knowtionaries
          </router-link>
          <router-link 
            to="/tasks" 
            class="px-3 py-2 text-gray-700 font-medium rounded-md hover:bg-gray-100 hover:text-blue-600 transition-colors"
          >
            Tareas
          </router-link>
        </div>

        <!-- Right side -->
        <div class="flex items-center space-x-4">
          <!-- User profile or login -->
          <div v-if="authStore.isAuthenticated" class="flex items-center space-x-3">
            <div class="relative group">
              <button class="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 transition-colors">
                <div class="w-10 h-10 bg-gradient-to-br from-green-500 to-blue-600 rounded-full flex items-center justify-center shadow-md">
                  <span class="font-semibold text-white text-sm">{{ authStore.user?.username?.charAt(0).toUpperCase() }}</span>
                </div>
                <span class="font-medium text-gray-900 hidden md:block">{{ authStore.user?.username }}</span>
              </button>
              <div class="absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-2xl border border-gray-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 py-1">
                <router-link 
                  to="/profile" 
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg font-medium"
                >
                  Mi Perfil
                </router-link>
                <button 
                  @click="logout"
                  class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg font-medium transition-colors"
                >
                  Cerrar sesión
                </button>
              </div>
            </div>
          </div>
          <router-link v-else to="/login" class="btn-primary px-5 py-2">
            Iniciar Sesión
          </router-link>

          <!-- Mobile menu button -->
          <button 
            @click="showMobileMenu = !showMobileMenu"
            class="md:hidden p-2 rounded-lg hover:bg-gray-100 text-gray-700"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile menu -->
      <div v-if="showMobileMenu" class="md:hidden bg-white border-t border-gray-200">
        <div class="px-2 pt-2 pb-3 space-y-1">
          <router-link 
            v-for="item in navItems" 
            :key="item.path"
            :to="item.path" 
            class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-gray-50"
            @click="showMobileMenu = false"
          >
            {{ item.label }}
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const showMobileMenu = ref(false)

const navItems = [
  { label: 'Dashboard', path: '/dashboard' },
  { label: 'Librerías', path: '/libraries' },
  { label: 'Flashcards', path: '/flowcards' },
  { label: 'Notas', path: '/notes' },
{ label: 'Knowtionaries', path: '/knowtionaries' },
  { label: 'Tareas', path: '/tasks' }
]

const logout = async () => {
  await authStore.logout()
  showMobileMenu.value = false
  router.push('/login')
}

onMounted(() => {
  authStore.checkAuth()
})
</script>

<style scoped>
.btn-primary {
  @apply bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-medium py-2 px-4 rounded-lg shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all duration-200;
}
</style>

