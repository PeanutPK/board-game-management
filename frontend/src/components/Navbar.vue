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

// import generatedLogo from '../assets/generatedLogo.png'
import { computed, ref } from 'vue'
import { logout as logoutUser } from '../api/auth'
import { useUserStore } from '../stores/counter'

const userStore = useUserStore()
const isLoggedIn = computed(() => userStore.isLoggedIn)
const isMobileMenuOpen = ref(false)

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
  window.location.href = '/'
}
</script>

<style scoped>
.navbar-brand {
  font-size: 1.05rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  text-decoration: none;
}

.menu-toggle {
  position: relative;
  width: 2.2rem;
  height: 2.2rem;
  border-radius: 0.55rem;
  border: 1px solid rgba(255, 255, 255, 0.45);
  background: rgba(255, 255, 255, 0.1);
}

.menu-icon,
.menu-icon::before,
.menu-icon::after {
  display: block;
  position: absolute;
  left: 50%;
  width: 1.15rem;
  height: 2px;
  background: var(--color-cgainsboro);
  transform: translateX(-50%);
  transition:
    transform 0.2s ease,
    opacity 0.2s ease;
  content: '';
}

.menu-icon {
  top: 50%;
}

.menu-icon::before {
  top: -0.38rem;
}

.menu-icon::after {
  top: 0.38rem;
}

.menu-icon-open {
  background: transparent;
}

.menu-icon-open::before {
  transform: translateX(-50%) translateY(0.38rem) rotate(45deg);
}

.menu-icon-open::after {
  transform: translateX(-50%) translateY(-0.38rem) rotate(-45deg);
}

.right-navbar {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.48rem 0.8rem;
  border-radius: 0.6rem;
  border: 1px solid transparent;
  color: var(--color-cgainsboro);
  text-decoration: none;
  font-weight: 600;
  transition:
    background-color 0.2s ease,
    border-color 0.2s ease,
    transform 0.2s ease;
}

.nav-link:hover {
  background: var(--color-cdarkslategray);
  border-color: var(--color-cblack);
}

.nav-link.router-link-active {
  background: var(--color-cdarkslategray);
  border-color: var(--color-cdarkslategray);
}

.nav-link:active {
  transform: translateY(1px);
}

.logout-btn {
  cursor: pointer;
  background: var(--color-cindianred);
}

/* hamburger menu */
@media (max-width: 767px) {
  .right-navbar {
    position: absolute;
    top: 4rem;
    left: 1rem;
    right: 1rem;
    z-index: 20;
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
    padding: 0.85rem;
    border-radius: 0.9rem;
    border: 1px solid var(--color-cdarkslategray);
    background: var(--color-cblack);
    backdrop-filter: blur(4px);
    box-shadow: 0 14px 30px rgba(0, 0, 0, 0.22);
  }

  .right-navbar.is-closed {
    display: none;
  }

  .right-navbar.is-open {
    display: flex;
  }

  .nav-link,
  .logout-btn {
    width: 100%;
  }

  .user-menu {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }
}
</style>
