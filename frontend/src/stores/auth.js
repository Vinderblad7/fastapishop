import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authAPI } from '@/services/api'
import apiClient from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('access_token') || null)
  const isAuthenticated = ref(!!token.value)

  if (token.value) {
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }

  async function login(username, password) {
    try {
      const res = await authAPI.login(username, password)
      token.value = res.data.access_token
      localStorage.setItem('access_token', token.value)
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
      isAuthenticated.value = true
      return { success: true }
    } catch (err) {
      console.error('Login failed', err)
      const detail = err.response?.data?.detail
      let errorMsg = 'Неверное имя пользователя или пароль'
      
      if (typeof detail === 'string') {
        errorMsg = detail
      } else if (Array.isArray(detail)) {
        errorMsg = detail.map(e => e.msg).join(', ')
      }

      return { success: false, error: errorMsg }
    }
  }

  async function register(userData) {
    try {
      await authAPI.register(userData)
      return { success: true }
    } catch (err) {
      console.error('Registration failed', err)
      const detail = err.response?.data?.detail
      let errorMsg = 'Ошибка при регистрации'

      if (typeof detail === 'string') {
        errorMsg = detail
      } else if (Array.isArray(detail)) {
        errorMsg = detail.map(e => e.msg).join(', ')
      }

      return { success: false, error: errorMsg }
    }
  }

  function logout() {
    token.value = null
    localStorage.removeItem('access_token')
    delete apiClient.defaults.headers.common['Authorization']
    isAuthenticated.value = false
  }

  return { token, isAuthenticated, login, register, logout }
})