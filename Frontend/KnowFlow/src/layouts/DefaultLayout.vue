<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header con perfil -->
    <header class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-gray-900">KnowFlow</h1>
          </div>
          
          <!-- User Profile Dropdown -->
          <div class="relative" v-if="authStore.isAuthenticated">
            <button @click="showProfile = !showProfile" class="flex items-center space-x-3 p-2 rounded-full hover:bg-gray-100 transition-colors">
              <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
                <span class="text-white font-semibold text-lg">{{ authStore.user?.username?.charAt(0)?.toUpperCase() || 'U' }}</span>
              </div>
              <div class="hidden md:block">
                <span class="font-medium text-gray-900">{{ authStore.user?.username }}</span>
              </div>
            </button>
            
            <!-- Dropdown -->
            <div v-if="showProfile" class="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg py-2 border border-gray-200 z-50">
              <div class="px-4 py-3 border-b border-gray-100">
                <p class="font-medium text-gray-900">{{ authStore.user?.username }}</p>
                <p class="text-sm text-gray-500">{{ authStore.user?.email }}</p>
              </div>
              <button @click="authStore.logout" class="w-full text-left px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                Cerrar sesión
              </button>
            </div>
          </div>
          
          <!-- Login button -->
          <router-link v-else to="/login" class="bg-blue-600 text-white px-6 py-2 rounded-xl hover:bg-blue-700 font-semibold transition-colors">
            Iniciar Sesión
          </router-link>
        </div>
      </div>
    </header>

    <!-- Sidebar Navigation -->
    <aside class="bg-white shadow-sm border-r w-64 fixed inset-y-0 left-0 transform -translate-x-full lg:translate-x-0 transition-transform duration-200 ease-in-out z-30" :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'">
      <nav class="p-6 space-y-4">
        <router-link to="/dashboard" class="flex items-center p-3 rounded-xl hover:bg-blue-50 text-gray-700 hover:text-blue-600 transition-colors font-medium">
          <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
          </svg>
          Dashboard
        </router-link>
        <router-link to="/libraries" class="flex items-center p-3 rounded-xl hover:bg-blue-50 text-gray-700 hover:text-blue-600 transition-colors font-medium">
          <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0H7m5 0v-5m0 0a1 1 0 00-1-1H6a1 1 0 00-1 1v5m6-5h2a1 1 0 001-1V9a1 1 0 00-1-1h-2a1 1 0 00-1 1v5z"/>
          </svg>
          Librerías
        </router-link>
        <router-link to="/flowcards" class="flex items-center p-3 rounded-xl hover:bg-blue-50 text-gray-700 hover:text-blue-600 transition-colors font-medium">
          <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          Flashcards
        </router-link>
        <router-link to="/notes" class="flex items-center p-3 rounded-xl hover:bg-blue-50 text-gray-700 hover:text-blue-600 transition-colors font-medium">
          <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
          </svg>
          Notas
        </router-link>
        <router-link to="/knowtionaries" class="flex items-center p-3 rounded-xl hover:bg-blue-50 text-gray-700 hover:text-blue-600 transition-colors font-medium">
          <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          Cuestionarios
        </router-link>
        <router-link to="/tasks" class="flex items-center p-3 rounded-xl hover:bg-blue-50 text-gray-700 hover:text-blue-600 transition-colors font-medium">
          <svg class="w-6 h-6 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
          Tareas
        </router-link>
      </nav>
    </aside>

    <!-- Mobile menu button -->
    <button @click="sidebarOpen = true" class="lg:hidden p-4 fixed top-4 left-4 z-40 bg-white rounded-xl shadow-lg">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
      </svg>
    </button>

    <!-- Overlay -->
    <div v-if="sidebarOpen" @click="sidebarOpen = false" class="fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden"></div>

    <!-- Main content -->
    <main class="lg:ml-64 p-6 lg:p-8 min-h-screen">
      <router-view/>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const sidebarOpen = ref(false)
const showProfile = ref(false)

const logout = () => {
  authStore.logout()
  showProfile.value = false
}

onMounted(() => {
  authStore.checkAuth()
})
</script>

