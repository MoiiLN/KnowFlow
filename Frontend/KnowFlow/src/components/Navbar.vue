<template>
  <nav class="bg-white shadow-lg fixed w-full z-40 top-0 border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <router-link to="/dashboard" class="flex items-center space-x-2">
            <div class="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg">
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
            @click="console.log('Librerías clicked, going to /libraries')"
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
              <button @click.prevent="goToProfile; console.log('Avatar clicked')" class="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer">
                <div class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center shadow-md hover:scale-105 transition-transform">
                  <span class="font-semibold text-white text-sm">{{ authStore.user?.username?.charAt(0).toUpperCase() }}</span>
                </div>
                <span class="font-medium text-gray-900 hidden md:block hover:underline">{{ authStore.user?.username }}</span>
              </button>
              <div class="absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-2xl border border-gray-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 py-1">
                <div @click="goToProfile" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded-lg font-medium cursor-pointer">
                  Mi Perfil
                </div>
                <button 
                  @click="logout"
                  class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg font-medium transition-colors"
                >
                  Cerrar sesión
                </button>
              </div>
            </div>
          </div>
          <router-link v-else to="/login" class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all duration-200">
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
            @click="console.log('Mobile', item.label, 'clicked'); showMobileMenu = false"
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

const goToProfile = () => {
  router.push('/profile')
}

const logout = async () => {
  await authStore.logout()
  showMobileMenu.value = false
  router.push('/login')
}

onMounted(() => {
  authStore.checkAuth()
})
</script>
