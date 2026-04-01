<template>
  <div class="min-h-screen bg-gray-100">
    <Navbar />

    <div class="p-6">
      <slot />
    </div>
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
</script>