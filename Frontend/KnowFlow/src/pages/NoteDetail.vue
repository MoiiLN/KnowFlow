<template>
  <DefaultLayout>
    <div class="max-w-4xl mx-auto">
      <div class="card p-8 mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-6">{{ note.title }}</h1>
        <div class="prose prose-lg max-w-none">
          <div v-html="note.content"></div>
        </div>
        <div class="flex items-center justify-between mt-12 pt-8 border-t border-gray-200">
          <span class="text-sm text-gray-500">{{ formatDate(note.created_at) }}</span>
          <div class="flex space-x-3">
            <Button variant="outline">Editar</Button>
            <Button variant="danger">Eliminar</Button>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import Button from '@/components/Button.vue'

const note = ref({ title: 'Mi Nota', content: '<p>Contenido de la nota...</p>', created_at: new Date().toISOString() })

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('es-ES')
}
</script>
