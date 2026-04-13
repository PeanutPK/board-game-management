<template>
  <nav class="navbar py-3">
    <div class="mx-auto flex w-full items-center justify-end sm:justify-between text-centergap-4">
      <router-link
        to="/"
        class="navbar-brand items-center gap-4 hidden sm:flex text-center"
        @click="closeMobileMenu"
      >
        <!-- <img
          :src="generatedLogo"
          alt="website logo"
          loading="lazy"
          class="object-center object-cover rounded-full size-20 transform scale-125"
        /> -->
        <div>
          <p>BOARD GAME</p>
          <p>Management</p>
        </div>
      </router-link>

      <button
        class="menu-toggle md:hidden"
        type="button"
        :aria-expanded="isMobileMenuOpen"
        aria-controls="nav-menu"
        aria-label="Toggle navigation"
        @click="toggleMobileMenu"
      >
        <span class="sr-only">Toggle menu</span>
        <span class="menu-icon" :class="{ 'menu-icon-open': isMobileMenuOpen }"></span>
      </button>

      <div id="nav-menu" class="right-navbar" :class="isMobileMenuOpen ? 'is-open' : 'is-closed'">
        <div v-if="isLoggedIn && userStore.userRole === 'admin'">
          <router-link to="/admin" class="nav-link" @click="closeMobileMenu">Admin</router-link>
        </div>
        <div v-if="isLoggedIn && isStaffOrAdmin">
          <router-link to="/manage" class="nav-link" @click="closeMobileMenu">Manage</router-link>
        </div>
        <router-link to="/game" class="nav-link" @click="closeMobileMenu">Game List</router-link>

        <div v-if="isLoggedIn" class="user-menu">
          <router-link to="/dashboard" class="nav-link" @click="closeMobileMenu"
            >Dashboard</router-link
          >
          <button @click="handleLogout" class="nav-link logout-btn" type="button">Logout</button>
        </div>

        <div v-else>
          <router-link to="/auth" class="nav-link" @click="closeMobileMenu">Login</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
defineOptions({
  name: 'AppNavbar',
})
import '@/assets/navbar.css'

// import generatedLogo from '../assets/generatedLogo.png'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { logout as logoutUser } from '../api/auth'
import { useUserStore } from '../stores/counter'

const userStore = useUserStore()
const isLoggedIn = computed(() => userStore.isLoggedIn)
const router = useRouter()
const isMobileMenuOpen = ref(false)
const isStaffOrAdmin = computed(() => {
  const role = userStore.userRole
  return role === 'staff' || role === 'admin'
})

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

function closeMobileMenu() {
  isMobileMenuOpen.value = false
}

function handleLogout() {
  logoutUser()
  userStore.logout()
  closeMobileMenu()
  router.push('/auth')
}
</script>

