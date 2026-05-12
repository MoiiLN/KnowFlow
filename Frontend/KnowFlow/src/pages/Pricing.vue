<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto py-16 px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h1 class="text-5xl md:text-6xl font-black text-gray-900 dark:text-white tracking-tight mb-4">
          Elige tu plan
        </h1>
        <p class="text-xl text-gray-500 dark:text-gray-400 font-medium">
          Escala tu productividad con KnowFlow Pro
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 max-w-6xl mx-auto">
        <div class="bg-white dark:bg-gray-800 rounded-[3rem] shadow-sm border border-gray-100 dark:border-gray-700 p-10 transition-all duration-500 hover:shadow-2xl hover:-translate-y-2">
          <div class="mb-8">
            <h2 class="text-4xl font-black text-gray-900 dark:text-white mb-2">
              Knower
            </h2>
            <p class="text-gray-500 dark:text-gray-400 font-medium">
              Perfecto para empezar
            </p>
          </div>

          <div class="space-y-4 mb-10">
            <p class="flex items-center text-lg font-bold text-gray-700 dark:text-gray-300">
              ✔ 10 Knowtionaries
            </p>
            <p class="flex items-center text-lg font-bold text-gray-700 dark:text-gray-300">
              ✔ 10 Flashcards
            </p>
            <p class="flex items-center text-lg font-bold text-gray-700 dark:text-gray-300">
              ✔ 20 Tasks
            </p>
            <p class="flex items-center text-lg font-bold text-gray-700 dark:text-gray-300">
              ✔ 10 Notes
            </p>
          </div>

          <div class="pt-6 border-t border-gray-100 dark:border-gray-700">
            <p class="text-5xl font-black text-gray-900 dark:text-white">
              €0
            </p>
            <p class="text-sm font-bold text-gray-400 uppercase tracking-widest mt-2">
              Gratis para siempre
            </p>
          </div>
        </div>

        <div class="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-[3rem] shadow-2xl p-10 text-white relative overflow-hidden transition-all duration-500 hover:scale-[1.02]">
          <div class="absolute top-0 right-0 -mt-12 -mr-12 w-40 h-40 bg-white/10 rounded-full blur-3xl"></div>

          <div class="relative z-10">
            <div class="mb-8">
              <h2 class="text-4xl font-black mb-2">
                Pro
              </h2>
              <p class="text-blue-100 font-medium">
                Desbloquea todo tu potencial
              </p>
            </div>

            <div class="space-y-4 mb-10">
              <p class="flex items-center text-lg font-bold">
                ✔ Todo ilimitado
              </p>
              <p class="flex items-center text-lg font-bold">
                ✔ Mejor productividad
              </p>
              <p class="flex items-center text-lg font-bold">
                ✔ Prioridad futura
              </p>
            </div>

            <div class="pt-6 border-t border-white/20 mb-8">
              <p class="text-5xl font-black">
                €9.99
              </p>
              <p class="text-sm font-bold text-blue-100 uppercase tracking-widest mt-2">
                / mes
              </p>
            </div>

            <button
              class="w-full bg-white text-blue-600 hover:bg-blue-50 py-5 rounded-2xl font-black text-lg shadow-xl transition-all active:scale-95"
              @click="upgradePlan"
            >
              Mejorar a Pro
            </button>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { subscriptionService } from '@/services/api'

const upgradePlan = () => {
  window.open('https://paypal.me/KnowFlowCompany', '_blank')
}
</script>