<template>
  <nav class="bg-white shadow p-4 flex justify-between items-center">
    <h1 class="font-bold text-xl">Knowflow</h1>

    <div class="space-x-4">
      <router-link to="/" class="hover:text-blue-500">Home</router-link>
      <router-link to="/knowtionaries" class="hover:text-blue-500">Knowtionaries</router-link>
      <router-link to="/flowcards" class="hover:text-blue-500">Flowcards</router-link>
    </div>
  </nav>
</template>