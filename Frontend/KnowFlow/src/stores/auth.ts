import { ref } from 'vue'
import { defineStore } from 'pinia'
import api from '@/services/api'

export interface User {
  id: number
  username: string
  email: string
  bio?: string
  avatar?: string
  date_joined?: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const isAuthenticated = ref(false)
  const loading = ref(true)
  const initialized = ref(false)

  const checkAuth = async () => {
    try {
      const response = await api.get('me/')
      console.log('DEBUG: User data from me/ API:', response.data)
      user.value = response.data
      isAuthenticated.value = true
    } catch (error: any) {
      if (error.response?.status === 401 || error.response?.status === 403) {
        isAuthenticated.value = false
        user.value = null
      }
    } finally {
      loading.value = false
      initialized.value = true
    }
  }

  const login = async (credentials: { username: string; password: string }) => {
    user.value = null
    isAuthenticated.value = false

    try {
      const plainCredentials = { username: credentials.username, password: credentials.password }
      await api.post('login/', plainCredentials)
      await checkAuth()
      return isAuthenticated.value
    } catch (error) {
      console.error('Login failed:', error)
      user.value = null
      isAuthenticated.value = false
      return false
    }
  }

  const logout = async () => {
    try {
      await api.post('logout/')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      user.value = null
      isAuthenticated.value = false
    }
  }

  return {
    user,
    isAuthenticated,
    loading,
    initialized,
    checkAuth,
    login,
    logout
  }
})
