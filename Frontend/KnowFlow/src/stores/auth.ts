import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/services/api'

export interface User {
  id: number
  username: string
  email: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const isAuthenticated = ref(false)
  const loading = ref(true)

  const checkAuth = async () => {
    try {
      const response = await api.get('/users/me/')
      user.value = response.data
      isAuthenticated.value = true
    } catch (error) {
      user.value = null
      isAuthenticated.value = false
    } finally {
      loading.value = false
    }
  }

  const login = async (credentials: { username: string; password: string }) => {
    try {
      const response = await api.post('/accounts/api/login/', credentials)
      if (response.data.success) {
        user.value = response.data.user
        isAuthenticated.value = true
        return true
      }
      return false
    } catch (error) {
      return false
    }
  }

  const logout = async () => {
    try {
      await api.post('/accounts/logout/')
    } finally {
      user.value = null
      isAuthenticated.value = false
    }
  }

  return {
    user,
    isAuthenticated,
    loading,
    checkAuth,
    login,
    logout
  }
})
