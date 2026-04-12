<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <h1 class="text-4xl font-bold text-gray-900 mb-8">Dashboard KnowFlow</h1>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        <div class="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
          <h2 class="text-2xl font-semibold text-gray-900 mb-2">📚 Librerías</h2>
          <p class="text-3xl font-bold text-blue-600">12</p>
        </div>
        <div class="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
          <h2 class="text-2xl font-semibold text-gray-900 mb-2">🧠 Flashcards</h2>
          <p class="text-3xl font-bold text-green-600">89</p>
        </div>
        <div class="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
          <h2 class="text-2xl font-semibold text-gray-900 mb-2">📝 Notas</h2>
          <p class="text-3xl font-bold text-purple-600">23</p>
        </div>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div class="bg-white p-8 rounded-xl shadow-lg">
          <h3 class="text-xl font-semibold mb-4">Acciones rápidas</h3>
          <div class="space-y-3">
            <router-link to="/libraries" class="w-full block bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 text-center font-semibold transition-colors">
              + Nueva Librería
            </router-link>
            <router-link to="/flowcards" class="w-full block bg-green-600 text-white py-3 px-4 rounded-lg hover:bg-green-700 text-center font-semibold transition-colors">
              + Nueva Flashcard
            </router-link>
          </div>
        </div>
        <div class="bg-white p-8 rounded-xl shadow-lg">
          <h3 class="text-xl font-semibold mb-4">Próximas tareas</h3>
          <ul class="space-y-2">
            <li class="flex items-center p-3 bg-gray-50 rounded-lg">
              <div class="w-5 h-5 bg-gray-300 rounded-full mr-3"></div>
              <span>Revisar matemáticas</span>
            </li>
            <li class="flex items-center p-3 bg-gray-50 rounded-lg">
              <div class="w-5 h-5 bg-gray-300 rounded-full mr-3"></div>
              <span>Estudiar historia</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
    <Footer />
  </DefaultLayout>
</template>

<script setup>
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import Footer from '@/components/Footer.vue'
console.log('Dashboard loaded!')
</script>

