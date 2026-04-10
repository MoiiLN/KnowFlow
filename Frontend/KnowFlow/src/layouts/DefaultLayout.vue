<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
    <!-- Sidebar -->
    <aside class="fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform -translate-x-full lg:translate-x-0 lg:static lg:inset-0 transition-transform duration-300 ease-in-out" :class="{ 'translate-x-0': sidebarOpen }">
      <div class="h-full overflow-y-auto py-6 px-4">
        <div class="flex items-center space-x-2 mb-8">
          <h1 class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            KnowFlow
          </h1>
        </div>
        
        <nav class="space-y-2">
          <router-link 
            v-for="item in navItems" 
            :key="item.path"
            :to="item.path" 
            class="flex items-center px-4 py-3 rounded-xl text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-all group"
          >
            <component :is="item.icon" class="w-5 h-5 mr-3 group-hover:scale-110 transition-transform" />
            {{ item.label }}
          </router-link>
          
          <div v-if="authStore.user" class="mt-8 pt-6 border-t border-gray-100">
            <div class="text-sm text-gray-500 mb-3 px-1">Usuario</div>
            <router-link to="/profile" class="nav-item">
              <HeroIconUser class="w-5 h-5" />
              {{ authStore.user.username }}
            </router-link>
            <button @click="logout" class="w-full flex items-center px-4 py-3 text-left text-red-600 hover:bg-red-50 rounded-xl transition-all">
              <HeroIconLogout class="w-5 h-5 mr-3" />
              Cerrar sesión
            </button>
          </div>
        </nav>
      </div>
    </aside>

    <!-- Mobile menu button -->
    <div class="lg:hidden p-4">
      <button @click="sidebarOpen = !sidebarOpen" class="p-2 rounded-lg bg-white shadow-sm">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path v-if="!sidebarOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Main content -->
    <main class="lg:ml-64 p-6 lg:p-8">
      <slot />
    </main>

    <!-- Overlay for mobile sidebar -->
    <div v-if="sidebarOpen" @click="sidebarOpen = false" class="fixed inset-0 z-40 lg:hidden bg-black bg-opacity-50"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

interface NavItem {
  label: string
  path: string
  icon: any
}

const authStore = useAuthStore()
const sidebarOpen = ref(false)

const navItems: NavItem[] = [
  { label: 'Dashboard', path: '/dashboard', icon: 'HeroIconHome' },
  { label: 'Librerías', path: '/libraries', icon: 'HeroIconLibrary' },
  { label: 'Flashcards', path: '/flowcards', icon: 'HeroIconCard' },
  { label: 'Notas', path: '/notes', icon: 'HeroIconNote' },
  { label: 'Cuestionarios', path: '/knowtionaries', icon: 'HeroIconQuiz' },
  { label: 'Tareas', path: '/tasks', icon: 'HeroIconTask' },
]

const logout = async () => {
  await authStore.logout()
}

// Icons as simple SVG components
const HeroIconHome = { template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>' }
const HeroIconLibrary = { template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h-4m-6 0H5a2 2 0 01-2-2V5a2 2 0 012-2h10.5a1 1 0 01.707.293l1.5 1.5a1 1 0 01.293.707V21z"/></svg>' }
const HeroIconCard = { template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>' }
const HeroIconNote = { template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>' }
const HeroIconQuiz = { template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>' }
const HeroIconTask = { template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>' }
const HeroIconUser = { template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>' }
const HeroIconLogout = { template: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>' }

onMounted(() => {
  authStore.checkAuth()
})
</script>
