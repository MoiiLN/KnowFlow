<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'

const items = ref([])

const fetchData = async () => {
  const res = await api.get('knowtionaries/')
  items.value = res.data
}

const deleteItem = async (id) => {
  await api.delete(`knowtionaries/${id}/`)
  fetchData()
}

onMounted(fetchData)
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Knowtionaries</h2>

    <router-link to="/knowtionaries/create"
      class="bg-green-500 text-white px-4 py-2 rounded mb-4 inline-block">
      Crear
    </router-link>

    <div v-for="item in items" :key="item.id"
      class="bg-white p-4 mb-2 rounded shadow flex justify-between">

      <span>{{ item.name }}</span>

      <div class="space-x-2">
        <router-link :to="`/knowtionaries/edit/${item.id}`"
          class="bg-yellow-400 px-2 py-1 rounded">
          Editar
        </router-link>

        <button @click="deleteItem(item.id)"
          class="bg-red-500 text-white px-2 py-1 rounded">
          Borrar
        </button>
      </div>
    </div>
  </div>
</template>