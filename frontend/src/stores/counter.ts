import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { getUsername, getRole, getToken } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(getToken())
  const isLoggedIn = computed(() => !!token.value)
  const userRole = ref<string | null>(getRole())
  const username = ref<string | null>(getUsername())

  function setToken(newToken: string | null) {
    token.value = newToken
  }

  function setRole(newRole: string | null) {
    userRole.value = newRole
  }

  function setUsername(newUsername: string | null) {
    username.value = newUsername
  }

  function logout() {
    token.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_role')
    localStorage.removeItem('username')
  }

  return { token, isLoggedIn, userRole, setToken, setRole, setUsername, logout }
})
