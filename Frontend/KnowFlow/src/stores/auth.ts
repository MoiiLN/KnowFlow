import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
const isAuthenticated = ref(JSON.parse(localStorage.getItem('knowflow_auth') || 'false'))
  const user = ref(null)
  const loading = ref(true)

  const checkAuth = async () => {
    loading.value = false
    isAuthenticated.value = false
  }

  const login = async (credentials) => {
    loading.value = true
    await new Promise(resolve => setTimeout(resolve, 1000))
    loading.value = false
  isAuthenticated.value = true
  localStorage.setItem('knowflow_auth', JSON.stringify(true))
    user.value = { username: credentials.username }
    return true
  }

  const logout = () => {
    isAuthenticated.value = false
    user.value = null
  }

  return {
    user,
    isAuthenticated,
    loading,
    login,
    logout,
    checkAuth
  }
})

