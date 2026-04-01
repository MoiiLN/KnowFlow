<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route = useRoute()
const router = useRouter()

const name = ref('')

const fetchItem = async () => {
  const res = await api.get(`knowtionaries/${route.params.id}/`)
  name.value = res.data.name
}

const updateItem = async () => {
  await api.put(`knowtionaries/${route.params.id}/`, {
    name: name.value
  })

  router.push('/')
}

onMounted(fetchItem)
</script>

<template>
  <div class="max-w-md mx-auto bg-white p-6 rounded shadow">
    <h2 class="text-xl font-bold mb-4">Editar</h2>

    <input v-model="name"
      class="w-full border p-2 mb-4" />

    <button @click="updateItem"
      class="bg-blue-500 text-white px-4 py-2 rounded w-full">
      Actualizar
    </button>
  </div>
</template>