<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'

const items = ref([])

const fetchData = async () => {
  const res = await api.get('flowcards/')
  items.value = res.data
}

onMounted(fetchData)
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Flowcards</h2>

    <router-link to="/flowcards/create"
      class="bg-green-500 text-white px-4 py-2 rounded mb-4 inline-block">
      Crear
    </router-link>

    <div v-for="item in items" :key="item.id"
      class="bg-white p-4 mb-2 rounded shadow">

      <h3 class="font-semibold">{{ item.title }}</h3>
      <p class="text-gray-600">{{ item.content }}</p>

    </div>
  </div>
</template>