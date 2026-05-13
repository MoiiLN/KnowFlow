<template>
  <DefaultLayout>
    <div class="max-w-6xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div class="bg-white dark:bg-gray-800 shadow-sm rounded-[2.5rem] border border-gray-100 dark:border-gray-700 overflow-hidden transition-colors duration-300">
        <div class="p-8 md:p-12 border-b border-gray-50 dark:border-gray-700 bg-gray-50/30 dark:bg-gray-900/10">
          <div class="flex flex-col md:flex-row items-center md:items-start gap-10">
            <div class="relative group">
              <div class="w-40 h-40 rounded-[2rem] overflow-hidden bg-gray-100 dark:bg-gray-900 border-4 border-white dark:border-gray-700 shadow-xl transition-transform duration-500 group-hover:scale-105">
                <img 
                  v-if="authStore.user?.avatar" 
                  :src="authStore.user.avatar" 
                  @error="(e) => { (e.target as HTMLImageElement).src = '/logo.png' }"
                  class="w-full h-full object-cover" 
                />
                <div v-else class="w-full h-full flex items-center justify-center bg-blue-600">
                  <span class="text-white text-4xl font-black">{{ authStore.user?.username?.substring(0,2).toUpperCase() }}</span>
                </div>
              </div>
              <label class="absolute -bottom-3 -right-3 w-12 h-12 bg-blue-600 text-white rounded-2xl flex items-center justify-center cursor-pointer shadow-lg hover:bg-blue-700 transition-all active:scale-90 z-10 border-4 border-white dark:border-gray-800">
                <input type="file" class="hidden" @change="handleAvatarChange" accept="image/*" />
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                </svg>
              </label>
            </div>

            <div class="text-center md:text-left flex-1 pt-4">
              <div class="flex flex-col md:flex-row md:items-center gap-4 mb-4">
                <h1 class="text-4xl font-black text-gray-900 dark:text-white tracking-tighter">{{ authStore.user?.username }}</h1>
                <span class="inline-flex px-4 py-1.5 bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 rounded-full text-xs font-black uppercase tracking-widest border border-blue-200 dark:border-blue-800">
                  {{ authStore.user?.role === 'K' ? '🚀 Knower' : '👤 Miembro' }}
                </span>
              </div>
              <p class="text-gray-500 dark:text-gray-400 font-bold text-lg mb-6">{{ authStore.user?.email }}</p>

              <div class="flex flex-wrap justify-center md:justify-start gap-4">
                <div class="inline-flex items-center gap-3 px-6 py-3 bg-orange-50 dark:bg-orange-900/20 text-orange-600 dark:text-orange-400 rounded-2xl border border-orange-100 dark:border-orange-800/50 shadow-sm">
                  <span class="text-xl">🔥</span>
                  <span class="font-black text-sm uppercase tracking-wider">Racha de {{ userStats.streak }} Días</span>
                </div>
                <div class="inline-flex items-center gap-3 px-6 py-3 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-2xl border border-blue-100 dark:border-blue-800/50 shadow-sm">
                  <span class="font-black text-xs uppercase tracking-widest">Desde {{ memberSince }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-5 border-b border-gray-50 dark:border-gray-700 bg-white dark:bg-gray-800">
          <div v-for="stat in displayedStats" :key="stat.label" class="p-8 text-center border-r border-b md:border-b-0 border-gray-50 dark:border-gray-700 last:border-r-0 hover:bg-gray-50/50 dark:hover:bg-gray-900/30 transition-colors">
            <div class="text-3xl mb-3 transition-transform duration-300 hover:scale-125">{{ stat.icon }}</div>
            <p class="text-[10px] font-black text-gray-400 dark:text-gray-500 uppercase tracking-[0.2em] mb-2">{{ stat.label }}</p>
            <p class="text-3xl font-black text-gray-900 dark:text-white">{{ stat.value }}</p>
          </div>
        </div>

        <div class="p-8 md:p-12">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-12">
            <div>
              <h3 class="text-2xl font-black text-gray-900 dark:text-white mb-4 tracking-tight">Gestión de Perfil</h3>
              <p class="text-gray-500 dark:text-gray-400 font-medium leading-relaxed">Actualiza tus datos de acceso y mantén tu cuenta de KnowFlow siempre al día.</p>

              <div class="mt-8 p-6 bg-blue-50 dark:bg-blue-900/10 rounded-3xl border border-blue-100 dark:border-blue-900/20">
                <h4 class="text-sm font-black text-blue-600 uppercase tracking-widest mb-3">
                  Suscripción
                </h4>

                <p class="text-sm font-bold text-gray-700 dark:text-gray-300 mb-4">
                  Plan actual:
                  <span class="text-blue-600 dark:text-blue-400">
                    {{ isPremium ? 'Pro' : 'Knower' }}
                  </span>
                </p>

                <router-link
                  v-if="!isPremium"
                  to="/pricing"
                  class="block w-full text-center py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-black text-[10px] uppercase tracking-widest transition-all active:scale-95"
                >
                  Mejorar a Pro
                </router-link>

                <div
                  v-else
                  class="w-full text-center py-3 bg-green-100 dark:bg-green-900/20 text-green-600 dark:text-green-400 rounded-xl font-black text-[10px] uppercase tracking-widest"
                >
                  Pro Activo
                </div>
              </div>

              <div class="mt-10 p-6 bg-rose-50 dark:bg-rose-900/10 rounded-3xl border border-rose-100 dark:border-rose-900/20">
                <h4 class="text-sm font-black text-rose-600 uppercase tracking-widest mb-2">Zona Crítica</h4>
                <p class="text-xs text-rose-500/70 font-bold mb-4">La eliminación de la cuenta es permanente.</p>
                <button
                  @click="handleDeleteAccount"
                  class="w-full py-3 bg-white dark:bg-gray-900 text-rose-600 border-2 border-rose-600 rounded-xl font-black text-[10px] uppercase tracking-widest hover:bg-rose-600 hover:text-white transition-all active:scale-95"
                >
                  Borrar Cuenta
                </button>
              </div>
            </div>

            <div class="lg:col-span-2">
              <form @submit.prevent="handleUpdateProfile" class="space-y-8">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div class="space-y-3">
                    <label class="text-xs font-black text-gray-400 dark:text-gray-500 uppercase tracking-widest px-1">Usuario</label>
                    <input
                      type="text"
                      v-model="profileData.username"
                      disabled
                      class="w-full px-6 py-4 bg-gray-50 dark:bg-gray-900/50 border border-gray-100 dark:border-gray-700 rounded-2xl text-gray-400 font-bold cursor-not-allowed shadow-inner"
                    />
                  </div>
                  <div class="space-y-3">
                    <label class="text-xs font-black text-gray-400 dark:text-gray-500 uppercase tracking-widest px-1">Email</label>
                    <input
                      type="email"
                      v-model="profileData.email"
                      class="w-full px-6 py-4 bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-2xl text-gray-900 dark:text-white font-bold focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all shadow-sm"
                    />
                  </div>
                </div>

                <div class="flex justify-end pt-4">
                  <button
                    type="submit"
                    :disabled="updating"
                    class="bg-blue-600 hover:bg-blue-700 text-white font-black py-5 px-14 rounded-[2rem] shadow-xl shadow-blue-500/20 transition-all active:scale-95 disabled:opacity-50 flex items-center gap-3"
                  >
                    {{ updating ? 'GUARDANDO...' : 'GUARDAR CAMBIOS' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import DefaultLayout from '../layouts/DefaultLayout.vue'
import { useAuthStore } from '../stores/auth'
import { useSubscriptionStore } from '../stores/subscription'
import { profileService } from '../services/api'

const authStore = useAuthStore()
const subscriptionStore = useSubscriptionStore()
const router = useRouter()
const updating = ref(false)

const profileData = ref({
  username: '',
  email: ''
})

const userStats = ref({
  libraries: 0,
  flashcards: 0,
  notes: 0,
  tasks: 0,
  knowtionaries: 0,
  streak: 0
})

const memberSince = ref('...')

const isPremium = computed(() =>
  subscriptionStore.usage?.subscription_plan === 'premium'
)

const displayedStats = computed(() => [
  { label: 'Librerías', icon: '📁', value: userStats.value.libraries },
  { label: 'Flashcards', icon: '🎴', value: userStats.value.flashcards },
  { label: 'Notas', icon: '📝', value: userStats.value.notes },
  { label: 'Tareas', icon: '✅', value: userStats.value.tasks },
  { label: 'Knowtionaries', icon: '❓', value: userStats.value.knowtionaries }
])

const handleAvatarChange = async (event: Event) => {
  const input = event.target as HTMLInputElement
  if (!input.files?.length) return

  const formData = new FormData()
  formData.append('avatar', input.files[0])

  try {
    const response = await profileService.update(formData)
    // Añadimos un timestamp para romper la caché del navegador
    const updatedUser = response.data.user
    if (updatedUser.avatar) {
      updatedUser.avatar = `${updatedUser.avatar}${updatedUser.avatar.includes('?') ? '&' : '?'}t=${Date.now()}`
    }
    authStore.user = updatedUser
    alert('¡Foto de perfil actualizada!')
  } catch (error) {
    console.error('Error updating avatar:', error)
  }
}

const handleUpdateProfile = async () => {
  updating.value = true
  const formData = new FormData()
  formData.append('email', profileData.value.email)

  try {
    const response = await profileService.update(formData)
    authStore.user = response.data.user
    alert('¡Perfil actualizado!')
  } catch (error) {
    console.error('Error updating profile:', error)
  } finally {
    updating.value = false
  }
}

const handleDeleteAccount = async () => {
  if (confirm('¿Deseas eliminar tu cuenta?')) {
    try {
      await profileService.deleteAccount()
      authStore.logout()
      router.push('/login')
    } catch (error) {
      console.error('Error deleting account:', error)
    }
  }
}

const loadData = async () => {
  if (authStore.user) {
    profileData.value = {
      username: authStore.user.username,
      email: authStore.user.email || ''
    }

    if (authStore.user.stats) {
      userStats.value = authStore.user.stats
    } else {
      await authStore.checkAuth()
      if (authStore.user?.stats) userStats.value = authStore.user.stats
    }

    if (authStore.user.date_joined) {
      const date = new Date(authStore.user.date_joined)
      const month = date.toLocaleDateString('es-ES', { month: 'long' })
      const year = date.getFullYear()
      memberSince.value = `${month} de ${year}`
    }
  }
}

onMounted(async () => {
  await loadData()
  await subscriptionStore.fetchUsage()
})
</script>
