<template>
  <nav class="bg-white/80 dark:bg-gray-900/80 backdrop-blur-md shadow-sm fixed w-full z-40 top-0 border-b border-gray-100 dark:border-gray-800 transition-colors duration-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-20">
        <!-- Logo -->
        <div class="flex items-center">
          <router-link to="/dashboard" class="flex items-center space-x-3 group">
            <div class="w-12 h-12 bg-blue-600 rounded-[1rem] flex items-center justify-center shadow-lg shadow-blue-500/30 group-hover:rotate-6 transition-transform duration-300">
              <span class="text-xl font-black text-white">KF</span>
            </div>
            <span class="text-2xl font-black text-gray-900 dark:text-white tracking-tighter">KnowFlow</span>
          </router-link>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden lg:flex items-center space-x-2">
          <router-link 
            v-for="item in navItems"
            :key="item.path"
            :to="item.path" 
            class="relative px-5 py-3 text-gray-500 dark:text-gray-400 font-bold rounded-xl hover:text-blue-600 dark:hover:text-blue-400 transition-all text-xs uppercase tracking-[0.15em] group"
          >
            {{ item.label }}
            <!-- Active indicator line -->
            <span 
              class="absolute bottom-1 left-1/2 -translate-x-1/2 w-0 h-1 bg-blue-600 rounded-full transition-all duration-300 group-hover:w-4"
              :class="{ 'w-8 !bg-blue-600': isRouteActive(item.path) }"
            ></span>
          </router-link>
        </div>

        <!-- Right side -->
        <div class="flex items-center space-x-4">
          <!-- Theme Toggle -->
          <button 
            @click="toggleTheme" 
            class="p-3 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 rounded-2xl hover:bg-gray-200 dark:hover:bg-gray-700 transition-all active:scale-90"
            title="Cambiar tema"
          >
            <svg v-if="!isDark" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
            <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 18v1m9-9h1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </button>

          <!-- User Section -->
          <div v-if="authStore.isAuthenticated" class="flex items-center">
            <div class="relative group">
              <div class="flex items-center space-x-3 p-2 rounded-2xl hover:bg-gray-100 dark:hover:bg-gray-800 transition-all cursor-pointer">
                <div class="w-11 h-11 bg-gray-200 dark:bg-gray-700 rounded-full flex items-center justify-center shadow-lg hover:scale-105 transition-transform overflow-hidden border-2 border-white dark:border-gray-800">
                  <img 
                    v-if="authStore.user?.avatar" 
                    :src="authStore.user.avatar" 
                    @error="(e) => { 
                      console.log('DEBUG: Avatar load failed, using fallback');
                      (e.target as HTMLImageElement).src = '/logo.png' 
                    }"
                    class="w-full h-full object-cover" 
                  />
                  <div v-else class="w-full h-full bg-blue-600 flex items-center justify-center">
                    <span class="text-white text-xs font-bold">{{ authStore.user?.username?.substring(0,2).toUpperCase() }}</span>
                  </div>
                </div>
                <span class="font-black text-gray-800 dark:text-white hidden md:block text-sm uppercase tracking-wider">{{ authStore.user?.username }}</span>
                <svg class="w-4 h-4 text-gray-400 group-hover:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </div>
              
              <!-- Dropdown Menu -->
              <div class="absolute right-0 mt-3 w-64 bg-white dark:bg-gray-800 rounded-3xl shadow-2xl border border-gray-100 dark:border-gray-700 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50 py-3 overflow-hidden origin-top-right">
                <div class="px-6 py-4 border-b border-gray-50 dark:border-gray-700 mb-2">
                  <p class="text-xs font-black text-gray-400 uppercase tracking-widest mb-1">Usuario</p>
                  <p class="font-black text-gray-900 dark:text-white truncate">{{ authStore.user?.email || authStore.user?.username }}</p>
                </div>
                <router-link to="/profile" class="flex items-center px-6 py-3 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 font-bold transition-colors">
                  <span class="mr-4 text-lg">👤</span> Mi Perfil
                </router-link>
                <div class="border-t border-gray-50 dark:border-gray-700 my-2"></div>
                <button 
                  @click="logout"
                  class="w-full text-left px-6 py-4 text-sm text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-900/20 font-black transition-colors"
                >
                  <span class="mr-4 text-lg">🚪</span> CERRAR SESIÓN
                </button>
              </div>
            </div>
          </div>
          <router-link v-else to="/login" class="bg-blue-600 hover:bg-blue-700 text-white font-black py-4 px-8 rounded-2xl shadow-xl shadow-blue-500/20 transition-all hover:-translate-y-1">
            CONECTAR
          </router-link>

          <!-- Mobile Toggle -->
          <button 
            @click="showMobileMenu = !showMobileMenu"
            class="lg:hidden p-3 rounded-2xl bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!showMobileMenu" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile menu -->
      <div v-if="showMobileMenu" class="lg:hidden bg-white dark:bg-gray-900 border-t border-gray-100 dark:border-gray-800 py-6 px-4 space-y-3 animate-in slide-in-from-top duration-300">
        <router-link 
          v-for="item in navItems" 
          :key="item.path"
          :to="item.path" 
          class="block px-6 py-4 rounded-2xl text-base font-black text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-gray-50 dark:hover:bg-gray-800 transition-all"
          @click="showMobileMenu = false"
        >
          {{ item.label }}
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const showMobileMenu = ref(false)
const isDark = ref(false)

const navItems = [
  { label: 'Dashboard', path: '/dashboard' },
  { label: 'Libraries', path: '/libraries' },
  { label: 'Flashcards', path: '/flowcards' },
  { label: 'Notes', path: '/notes' },
  { label: 'Knowtionaries', path: '/knowtionaries' },
  { label: 'Planner', path: '/planner' },
  { label: 'TimerFlow', path: '/timerflow' }
]

const isRouteActive = (path: string) => {
  return route.path === path
}

const toggleTheme = () => {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

const logout = async () => {
  await authStore.logout()
  showMobileMenu.value = false
  router.push('/login')
}

onMounted(() => {
  authStore.checkAuth()
  
  // Check system/local storage theme
  const savedTheme = localStorage.getItem('theme')
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  
  if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
})
</script>