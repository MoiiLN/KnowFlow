<template>
  <DefaultLayout>
    <div class="max-w-7xl mx-auto">
      <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-8">
        <div>
          <h1 class="text-4xl font-bold text-gray-900 mb-2">Tareas</h1>
          <p class="text-xl text-gray-600">Organiza tu día de estudio</p>
        </div>
        <button class="btn-primary px-8 py-3 w-full lg:w-auto">+ Nueva Tarea</button>
      </div>
      <div class="card">
        <p class="text-gray-500 text-center py-20">Funcionalidad de tareas en desarrollo...</p>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '../layouts/DefaultLayout.vue'
</script>
