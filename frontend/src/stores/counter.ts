import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { getToken } from '../api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(getToken())
  const isLoggedIn = computed(() => !!token.value)

  function setToken(newToken: string | null) {
    token.value = newToken
  }

  function logout() {
    token.value = null
    localStorage.removeItem('access_token')
  }

  return { token, isLoggedIn, setToken, logout }
})
