<template>
  <section class="home-view">
    <div class="left-info">
      <img :src="generatedLogo" alt="Board Game Management logo" class="info-logo" />
    </div>
    <div class="right-info">
      <h1 v-if="getUsername()" class="text-cblack">
        <div class="flex justify-center md:justify-start">
          Welcome&nbsp;
          <p class="text-cdarkslategray font-extrabold underline">
            {{ getUsername() }}
          </p>
        </div>
        to Board Game Management
      </h1>
      <h1 v-else class="text-cblack">Welcome Guest to Board Game Management</h1>
      <p class="info-subtitle">Browse, book, and order your favorite board games in one place.</p>

      <div class="info-stats">
        <div class="stat-pill">
          <span class="stat-label">Games Listed</span>
          <strong>{{ gameStats.total }}</strong>
        </div>
        <div class="stat-pill">
          <span class="stat-label">Available Now</span>
          <strong>{{ gameStats.available }}</strong>
        </div>
      </div>
      <div class="info-link">
        <router-link to="/game" class="browse-link">
          <p>Start Browsing</p>
          <Icon icon="mdi:arrow-right" style="font-size: 24px; font-weight: bolder" />
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import '@/assets/home.css'
import generatedLogo from '@/assets/generatedLogo.png'

import { Icon } from '@iconify/vue'
import { ref, onMounted } from 'vue'
import { getUsername } from '@/api/auth'
import { getGameStats } from '@/api/games'

const gameStats = ref<{ total: number; available: number }>({ total: 0, available: 0 })

onMounted(async () => {
  try {
    gameStats.value = await getGameStats()
    console.log('Game stats fetched successfully:', gameStats.value)
  } catch (error) {
    console.error('Failed to fetch game stats:', error)
  }
})
</script>
