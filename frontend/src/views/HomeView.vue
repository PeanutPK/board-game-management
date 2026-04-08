<template>
  <div class="home">
    <div class="hero">
      <h1>Welcome to Board Game Management</h1>
      <p>Browse, book, and order your favorite board games</p>
      
      <div v-if="!isLoggedIn" class="auth-buttons">
        <button @click="showLoginForm = true" class="btn btn-primary">Login</button>
        <button @click="showRegisterForm = true" class="btn btn-secondary">Register</button>
      </div>
      
      <div v-else class="welcome-msg">
        <p>Welcome back! <router-link to="/dashboard">Go to Dashboard</router-link></p>
      </div>
    </div>

    <!-- Login Form -->
    <div v-if="showLoginForm" class="modal">
      <div class="modal-content">
        <span class="close" @click="showLoginForm = false">&times;</span>
        <h2>Login</h2>
        <form @submit.prevent="handleLogin">
          <input 
            v-model="loginForm.username" 
            type="text" 
            placeholder="Username" 
            required
          />
          <input 
            v-model="loginForm.password" 
            type="password" 
            placeholder="Password" 
            required
          />
          <button type="submit" class="btn btn-primary">Login</button>
          <p v-if="loginError" class="error">{{ loginError }}</p>
        </form>
      </div>
    </div>

    <!-- Register Form -->
    <div v-if="showRegisterForm" class="modal">
      <div class="modal-content">
        <span class="close" @click="showRegisterForm = false">&times;</span>
        <h2>Register</h2>
        <form @submit.prevent="handleRegister">
          <input 
            v-model="registerForm.email" 
            type="email" 
            placeholder="Email" 
            required
          />
          <input 
            v-model="registerForm.username" 
            type="text" 
            placeholder="Username" 
            required
          />
          <input 
            v-model="registerForm.password" 
            type="password" 
            placeholder="Password" 
            required
          />
          <button type="submit" class="btn btn-primary">Register</button>
          <p v-if="registerError" class="error">{{ registerError }}</p>
        </form>
      </div>
    </div>

    <!-- Games Preview -->
    <section class="games-preview">
      <h2>Featured Games</h2>
      <div class="games-grid">
        <div v-for="game in games" :key="game.id" class="game-card">
          <h3>{{ game.title }}</h3>
          <p>{{ game.description }}</p>
          <p class="price">${{ game.price.toFixed(2) }}</p>
          <p :class="game.is_available ? 'available' : 'unavailable'">
            {{ game.is_available ? 'Available' : 'Unavailable' }}
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import {AxiosError} from "axios";
import { ref, computed, onMounted } from 'vue'
import { login, register, saveToken, getToken } from '../api/auth'
import { getGames } from '../api/games'
import type { Game } from '../api/games'
import type { UserLogin, UserRegister } from '../api/auth'

const games = ref<Game[]>([])
const showLoginForm = ref(false)
const showRegisterForm = ref(false)
const loginError = ref('')
const registerError = ref('')

const loginForm = ref<UserLogin>({
  username: '',
  password: ''
})

const registerForm = ref<UserRegister>({
  email: '',
  username: '',
  password: ''
})

const isLoggedIn = computed(() => !!getToken())

onMounted(async () => {
  try {
    games.value = await getGames(0, 6)
  } catch (error) {
    console.error('Failed to fetch games:', error)
  }
})

async function handleLogin() {
  try {
    loginError.value = ''
    const response = await login(loginForm.value)
    saveToken(response.access_token)
    showLoginForm.value = false
    loginForm.value = { username: '', password: '' }
    window.location.reload()
  } catch (error) {
    if (error instanceof AxiosError) {
      loginError.value = 'Login failed. Please check your credentials.\n' + (error.response?.data?.detail || '')
    } else {
      loginError.value = 'An unexpected error occurred.'
    }
  }
}

async function handleRegister() {
  try {
    registerError.value = ''
    const response = await register(registerForm.value)
    saveToken(response.access_token)
    showRegisterForm.value = false
    registerForm.value = { email: '', username: '', password: '' }
    window.location.reload()
  } catch (error) {
    if (error instanceof AxiosError) {
      registerError.value = 'Registration failed. Please try again.\n' + (error.response?.data?.detail || '')
    } else {
      registerError.value = 'An unexpected error occurred.'
    }
  }
}
</script>
