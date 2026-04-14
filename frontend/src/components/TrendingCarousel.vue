<template>
  <section class="trending-section shadow-md">
    <div class="panel-header">
      <div>
        <p class="eyebrow">Trending</p>
        <h2>Highest Rated Games</h2>
      </div>
      <p class="section-subtitle">Ranked by average rating from the game catalog.</p>
    </div>

    <div v-if="loading" class="loading-card">Loading trending games...</div>

    <div v-else-if="trendingGames.length === 0" class="empty-state">
      No trending games found yet.
    </div>

    <div v-else class="trending-carousel">
      <article v-if="currentTrendingGame" class="trend-card carousel-slide">
        <div class="trend-top">
          <div>
            <p class="trend-rank">Top rated #{{ currentTrendIndex + 1 }}</p>
            <h3>{{ currentTrendingGame.title }}</h3>
          </div>
          <span class="rating-badge">{{ formatRating(currentTrendingGame.average_rating) }}</span>
        </div>

        <p class="description">{{ currentTrendingGame.description }}</p>

        <div class="detail-grid compact">
          <div class="detail-item">
            <span>Price</span>
            <strong>${{ currentTrendingGame.price.toFixed(2) }}</strong>
          </div>
          <div class="detail-item">
            <span>Players</span>
            <strong>{{ formatPlayers(currentTrendingGame) }}</strong>
          </div>
          <div class="detail-item">
            <span>Playtime</span>
            <strong>{{ formatPlaytime(currentTrendingGame) }}</strong>
          </div>
        </div>

        <div class="flex justify-between items-center">
          <div class="trend-actions">
            <router-link :to="`/game/${currentTrendingGame.id}`" class="action-btn tertiary">
              Details
            </router-link>
            <button
              @click="$emit('rent', currentTrendingGame)"
              :disabled="!isLoggedIn || !currentTrendingGame.is_available"
              class="action-btn primary"
              type="button"
            >
              Rent
            </button>
            <button
              @click="$emit('buy', currentTrendingGame)"
              :disabled="!isLoggedIn || currentTrendingGame.stock === 0"
              class="action-btn secondary"
              type="button"
            >
              Buy
            </button>
          </div>
          <p v-if="currentTrendingGame.stock > 0">Stock: {{ currentTrendingGame.stock }}</p>
          <p v-else class="error-message">Out of Stock</p>
        </div>
      </article>

      <div v-if="trendingGames.length > 1" class="carousel-controls">
        <button class="carousel-btn" type="button" @click="showPrevious">&lt;</button>
        <div class="carousel-dots">
          <button
            v-for="(_game, index) in trendingGames"
            :key="index"
            class="carousel-dot"
            :class="{ active: index === currentTrendIndex }"
            :aria-label="`Go to trending game ${index + 1}`"
            type="button"
            @click="goTo(index)"
          ></button>
        </div>
        <button class="carousel-btn" type="button" @click="showNext">&gt;</button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { getToken } from '@/api/auth'
import type { Game } from '@/api/games'

const props = defineProps<{
  trendingGames: Game[]
  loading: boolean
  currentTrendIndex: number
}>()

const emit = defineEmits<{
  rent: [game: Game]
  buy: [game: Game]
  updateIndex: [index: number]
}>()

const isLoggedIn = computed(() => !!getToken())

const currentTrendingGame = computed(() => {
  if (props.trendingGames.length === 0) {
    return null
  }
  return props.trendingGames[props.currentTrendIndex] ?? null
})

function showPrevious() {
  if (props.trendingGames.length === 0) return
  const newIndex =
    (props.currentTrendIndex - 1 + props.trendingGames.length) % props.trendingGames.length
  emit('updateIndex', newIndex)
}

function showNext() {
  if (props.trendingGames.length === 0) return
  const newIndex = (props.currentTrendIndex + 1) % props.trendingGames.length
  emit('updateIndex', newIndex)
}

function goTo(index: number) {
  if (index < 0 || index >= props.trendingGames.length) return
  emit('updateIndex', index)
}

function formatRating(rating: number | null): string {
  if (rating === null || rating === undefined) {
    return 'NR'
  }
  return rating.toFixed(1)
}

function formatPlayers(game: Game): string {
  const minPlayers = game.min_players ?? 0
  const maxPlayers = game.max_players ?? 0

  if (!minPlayers && !maxPlayers) {
    return 'N/A'
  }

  if (minPlayers === maxPlayers) {
    return `${minPlayers}`
  }

  return `${minPlayers}-${maxPlayers}`
}

function formatPlaytime(game: Game): string {
  if (!game.average_playtime) {
    return 'N/A'
  }

  return `${game.average_playtime} mins`
}
</script>
