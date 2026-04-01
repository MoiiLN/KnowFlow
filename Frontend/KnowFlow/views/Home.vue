<template>
  <div>
    <h1 class="text-3xl font-bold mb-6">Dashboard</h1>

    <div class="grid grid-cols-2 gap-6">
      <router-link to="/knowtionaries"
        class="bg-white p-6 rounded shadow hover:shadow-lg transition">
        <h2 class="text-xl font-semibold">📚 Knowtionaries</h2>
      </router-link>

      <router-link to="/flowcards"
        class="bg-white p-6 rounded shadow hover:shadow-lg transition">
        <h2 class="text-xl font-semibold">🧠 Flowcards</h2>
      </router-link>
    </div>
  </div>
</template>