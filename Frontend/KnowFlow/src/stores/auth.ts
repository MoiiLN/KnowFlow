
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
      // Test Django session with protected endpoint
      await api.get('/libraries/')
      // If no 401, user is authenticated via session
      isAuthenticated.value = true
      // Try to get user info
      try {
        const response = await api.get('/api/users/me/') // Adjust if endpoint exists
        user.value = response.data
      } catch {
        // No user endpoint, use dummy
        user.value = { id: 1, username: 'Usuario', email: 'user@example.com' } as User
      }
    } catch (error: any) {
      if (error.response?.status === 401 || error.response?.status === 403) {
        isAuthenticated.value = false
        user.value = null
      }
    } finally {
      loading.value = false
    }
  }

  const login = async (credentials: { username: string; password: string }) => {
    try {
      // Django login endpoint - adjust if different
      await api.post('/accounts/login/', credentials)
      await checkAuth()
      return true
    } catch (error) {
      console.error('Login failed:', error)
      return false
    }
  }

  const logout = async () => {
    try {
      await api.post('/accounts/logout/')
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
    checkAuth,
    login,
    logout
  }
})

