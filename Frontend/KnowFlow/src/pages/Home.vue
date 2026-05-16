<template>
  <DefaultLayout>
    <div class="relative overflow-hidden">
      <!-- Background Decorations -->
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full -z-10 overflow-hidden pointer-events-none">
        <div class="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-400/20 rounded-full blur-[120px] animate-pulse"></div>
        <div class="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-indigo-400/20 rounded-full blur-[120px] animate-pulse" style="animation-delay: 2s"></div>
      </div>

      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-12 pb-24 md:pt-20 md:pb-32">
        <div class="text-center">
          <div class="inline-flex items-center px-4 py-2 rounded-full bg-blue-50 dark:bg-blue-900/30 border border-blue-100 dark:border-blue-800 mb-8 animate-fade-in">
            <span class="flex h-2 w-2 rounded-full bg-blue-600 mr-3"></span>
            <span class="text-sm font-bold text-blue-700 dark:text-blue-300 uppercase tracking-widest">Revoluciona tu aprendizaje</span>
          </div>
          
          <h1 class="text-6xl md:text-8xl font-black tracking-tighter mb-8 leading-none">
            <span class="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 dark:from-white dark:via-blue-100 dark:to-white bg-clip-text text-transparent">Know</span><span class="text-blue-600">Flow</span>
          </h1>
          
          <p class="max-w-2xl mx-auto text-xl md:text-2xl text-gray-500 dark:text-gray-400 font-medium mb-12 leading-relaxed">
            La plataforma definitiva para organizar tu conocimiento, crear flujos de estudio inteligentes y dominar cualquier materia con facilidad.
          </p>

          <div class="flex flex-col sm:flex-row items-center justify-center gap-6 mb-20">
            <router-link 
              to="/signup" 
              class="w-full sm:w-auto px-10 py-5 bg-blue-600 hover:bg-blue-700 text-white font-black rounded-2xl shadow-2xl shadow-blue-500/30 transition-all hover:-translate-y-1 active:scale-95 text-lg uppercase tracking-wider"
            >
              Empieza Gratis
            </router-link>
            <router-link 
              to="/login" 
              class="w-full sm:w-auto px-10 py-5 bg-white dark:bg-gray-800 text-gray-900 dark:text-white font-black rounded-2xl border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-all hover:-translate-y-1 active:scale-95 text-lg uppercase tracking-wider shadow-sm"
            >
              Iniciar Sesión
            </router-link>
          </div>

          <!-- Feature Grid -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-left mt-12">
            <div class="bg-white/50 dark:bg-gray-800/50 backdrop-blur-xl p-10 rounded-[3rem] border border-gray-100 dark:border-gray-700 hover:shadow-2xl transition-all duration-500 group">
              <div class="w-16 h-16 bg-blue-100 dark:bg-blue-900/40 rounded-2xl flex items-center justify-center text-3xl mb-8 group-hover:scale-110 transition-transform">📚</div>
              <h3 class="text-2xl font-black text-gray-900 dark:text-white mb-4">Librerías Inteligentes</h3>
              <p class="text-gray-500 dark:text-gray-400 font-medium">Organiza todo tu material de estudio en un solo lugar con nuestra estructura intuitiva de carpetas y archivos.</p>
            </div>
            
            <div class="bg-white/50 dark:bg-gray-800/50 backdrop-blur-xl p-10 rounded-[3rem] border border-gray-100 dark:border-gray-700 hover:shadow-2xl transition-all duration-500 group">
              <div class="w-16 h-16 bg-emerald-100 dark:bg-emerald-900/40 rounded-2xl flex items-center justify-center text-3xl mb-8 group-hover:scale-110 transition-transform">🧠</div>
              <h3 class="text-2xl font-black text-gray-900 dark:text-white mb-4">Flowcards Activas</h3>
              <p class="text-gray-500 dark:text-gray-400 font-medium">Utiliza la repetición espaciada y el recuerdo activo para memorizar conceptos complejos de forma permanente.</p>
            </div>
            
            <div class="bg-white/50 dark:bg-gray-800/50 backdrop-blur-xl p-10 rounded-[3rem] border border-gray-100 dark:border-gray-700 hover:shadow-2xl transition-all duration-500 group">
              <div class="w-16 h-16 bg-orange-100 dark:bg-orange-900/40 rounded-2xl flex items-center justify-center text-3xl mb-8 group-hover:scale-110 transition-transform">⏱️</div>
              <h3 class="text-2xl font-black text-gray-900 dark:text-white mb-4">TimerFlow Focus</h3>
              <p class="text-gray-500 dark:text-gray-400 font-medium">Gestiona tu tiempo con técnicas de productividad integradas para mantener el enfoque en tus sesiones de estudio.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '../layouts/DefaultLayout.vue'
</script>

<style scoped>
@keyframes fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
  animation: fade-in 1s ease-out forwards;
}
</style>
