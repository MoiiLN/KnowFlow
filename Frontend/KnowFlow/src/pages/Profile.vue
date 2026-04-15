<template>
  <DefaultLayout>
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-12">
        <div class="w-32 h-32 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-2xl">
          <span class="text-5xl font-bold text-white">{{ authStore.user?.username?.charAt(0).toUpperCase() }}</span>
        </div>
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-2">{{ authStore.user?.username }}</h1>
        <p class="text-xl text-gray-600 dark:text-gray-300 mb-8">{{ authStore.user?.email }}</p>
      </div>
      
      <div class="grid md:grid-cols-2 gap-8">
        <div class="card p-8">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">Estadísticas</h3>
          <div class="space-y-6">
            <div>
              <div class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Librerías creadas</div>
              <div class="text-3xl font-bold text-primary-600 dark:text-primary-400">12</div>
            </div>
            <div>
              <div class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Flashcards</div>
              <div class="text-3xl font-bold text-green-600 dark:text-green-400">156</div>
            </div>
            <div>
              <div class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Tareas completadas</div>
              <div class="text-3xl font-bold text-purple-600 dark:text-purple-400">89%</div>
            </div>
          </div>
        </div>
        
        <div class="card p-8">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">Configuración</h3>
          <div class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Nombre de usuario</label>
              <input 
                type="text" 
                :value="authStore.user?.username" 
                class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-primary-500 dark:bg-gray-800 dark:text-white"
                disabled 
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Email</label>
              <input 
                type="email" 
                :value="authStore.user?.email" 
                class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl focus:ring-2 focus:ring-primary-500 dark:bg-gray-800 dark:text-white"
                disabled 
              />
            </div>
            <button class="w-full btn-primary py-3 px-6 rounded-xl font-semibold text-lg">
              Cambiar contraseña
            </button>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
</script>

