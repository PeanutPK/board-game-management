<template>
  <section class="view-hero shadow-md">
    <div>
      <div>
        <p class="eyebrow">Game detail</p>
        <h1>{{ game.title }}</h1>
        <p class="subtext">Explore the game and share your review with other players.</p>
      </div>

      <div class="detail-actions">
        <button
          type="button"
          class="action-btn primary"
          :disabled="!isLoggedIn || !game.is_available"
          @click="emit('rent')"
        >
          Rent
        </button>
        <button
          type="button"
          class="action-btn secondary"
          :disabled="!isLoggedIn || game.stock === 0"
          @click="emit('buy')"
        >
          Buy
        </button>
        <router-link to="/game" class="action-btn tertiary">Back to Games</router-link>
      </div>
    </div>

    <div class="detail-meta">
      <span :class="`availability ${game.is_available ? 'available' : 'unavailable'}`">
        {{ game.is_available ? 'Available' : 'Unavailable' }}
      </span>
      <div class="flex gap-[0.7rem]">
        <span class="stat-pill">{{ reviewCount }} Reviews</span>
        <span class="stat-pill">Community Rating: {{ displayAverageRating }}</span>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Game } from '@/api/games'

defineProps<{
  game: Game
  isLoggedIn: boolean
  reviewCount: number
  displayAverageRating: string
}>()

const emit = defineEmits<{
  (e: 'rent'): void
  (e: 'buy'): void
}>()
</script>
