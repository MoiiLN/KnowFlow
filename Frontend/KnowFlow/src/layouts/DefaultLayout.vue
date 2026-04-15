
<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
    <Navbar />
    <main class="pt-20 lg:pl-64 p-6 lg:p-8">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">

import Navbar from '../components/Navbar.vue'

</script>

