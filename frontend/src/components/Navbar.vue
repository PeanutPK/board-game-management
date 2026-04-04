<template>
  <nav class="navbar">
    <div class="navbar-container">
      <router-link to="/" class="navbar-brand"> 🎲 Board Game Management </router-link>

      <button class="hamburger" @click="toggleMenu" :class="{ active: isMenuOpen }">
        <span></span>
        <span></span>
        <span></span>
      </button>

      <div class="nav-menu" :class="{ active: isMenuOpen }">
        <router-link to="/" class="nav-link" @click="isMenuOpen = false">Home</router-link>
        <router-link to="/inventory" class="nav-link" @click="isMenuOpen = false"
          >Inventory</router-link
        >

        <div v-if="isLoggedIn" class="user-menu">
          <router-link to="/dashboard" class="nav-link" @click="isMenuOpen = false">
            Dashboard
          </router-link>
          <button @click="handleLogout" class="nav-link logout-btn">Logout</button>
        </div>
        <div v-else class="auth-menu">
          <router-link to="/" class="nav-link" @click="isMenuOpen = false">Login</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
defineOptions({
  name: 'AppNavbar',
})

import { ref, computed } from 'vue'
import { logout as logoutUser } from '../api/auth'
import { useUserStore } from '../stores/counter'

const isMenuOpen = ref(false)
const userStore = useUserStore()
const isLoggedIn = computed(() => userStore.isLoggedIn)

function toggleMenu() {
  isMenuOpen.value = !isMenuOpen.value
}

function handleLogout() {
  logoutUser()
  userStore.logout()
  isMenuOpen.value = false
  window.location.href = '/'
}
</script>

<style scoped>
.navbar {
  background-color: #333;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand {
  color: white;
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: bold;
  transition: color 0.3s;
}

.navbar-brand:hover {
  color: #4caf50;
}

.hamburger {
  display: none;
  flex-direction: column;
  background: none;
  border: none;
  cursor: pointer;
  gap: 0.4rem;
}

.hamburger span {
  width: 25px;
  height: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 2px;
}

@media (max-width: 768px) {
  .hamburger {
    display: flex;
  }

  .hamburger.active span:nth-child(1) {
    transform: rotate(-45deg) translate(-8px, 8px);
  }

  .hamburger.active span:nth-child(2) {
    opacity: 0;
  }

  .hamburger.active span:nth-child(3) {
    transform: rotate(45deg) translate(-7px, -7px);
  }
}

.nav-menu {
  display: flex;
  gap: 1rem;
  align-items: center;
}

@media (max-width: 768px) {
  .nav-menu {
    position: absolute;
    left: 0;
    top: 60px;
    width: 100%;
    background-color: #222;
    flex-direction: column;
    gap: 0;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s;
  }

  .nav-menu.active {
    max-height: 300px;
  }
}

.nav-link {
  color: white;
  text-decoration: none;
  transition: color 0.3s;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

.nav-link:hover {
  color: #4caf50;
  background-color: rgba(76, 175, 80, 0.1);
}

@media (max-width: 768px) {
  .nav-link {
    display: block;
    width: 100%;
    text-align: left;
    border-radius: 0;
    padding: 1rem;
    border-bottom: 1px solid #444;
  }
}

.user-menu,
.auth-menu {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

@media (max-width: 768px) {
  .user-menu,
  .auth-menu {
    flex-direction: column;
    width: 100%;
    gap: 0;
  }
}

.logout-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem 1rem;
  color: white;
}

.logout-btn:hover {
  color: #d32f2f;
}

@media (max-width: 768px) {
  .logout-btn {
    display: block;
    width: 100%;
    text-align: left;
    border-radius: 0;
    padding: 1rem;
    border-bottom: 1px solid #444;
  }
}
</style>
