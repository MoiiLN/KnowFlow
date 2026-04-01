<script setup>
import { onMounted, ref } from "vue";
import api from "./services/api";

const flowcards = ref([]);

onMounted(async () => {
  const response = await api.get("flowcards/");
  flowcards.value = response.data;
});
</script>

<template>
  <h1>Flowcards</h1>

  <ul>
    <li v-for="card in flowcards" :key="card.id">
      {{ card.term }} - {{ card.definition }}
    </li>
  </ul>
</template>
