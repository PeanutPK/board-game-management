<template>
  <section class="game-summary shadow-md">
    <div class="panel-header">
      <div>
        <p class="eyebrow">Game detail</p>
        <h2>Game Summary</h2>
      </div>
      <p class="subtext">Explore the game and share your review with other players.</p>
    </div>

    <section class="detail-card">
      <div class="detail-grid">
        <div class="detail-item">
          <span>Price</span>
          <strong>${{ game.price.toFixed(2) }}</strong>
        </div>
        <div class="detail-item">
          <span>Rent</span>
          <strong>{{ game.rent !== null ? `$${game.rent.toFixed(2)}` : 'Not available' }}</strong>
        </div>
        <div class="detail-item">
          <span>Stock</span>
          <strong>{{ game.stock }}</strong>
        </div>
        <div class="detail-item">
          <span>Players</span>
          <strong>{{ formatPlayers(game.min_players, game.max_players) }}</strong>
        </div>
      </div>

      <div class="detail-grid compact" style="margin-top: 1rem">
        <div class="detail-item">
          <span>Playtime</span>
          <strong>{{ formatPlaytime(game.average_playtime) }}</strong>
        </div>
        <div class="detail-item">
          <span>Age</span>
          <strong>{{ formatAge(game.recommended_age) }}</strong>
        </div>
        <div class="detail-item">
          <span>Catalog Rating</span>
          <strong>{{ formatRating(game.average_rating) }}</strong>
        </div>
      </div>

      <p class="description" style="margin-top: 1rem">{{ game.description }}</p>
    </section>
  </section>
</template>

<script setup lang="ts">
import type { Game } from '@/api/games'

defineProps<{ game: Game }>()

function formatRating(rating: number | null): string {
  if (rating === null || rating === undefined) {
    return 'NR'
  }

  return rating.toFixed(1)
}

function formatPlayers(minPlayers: number | null, maxPlayers: number | null): string {
  if (!minPlayers && !maxPlayers) {
    return 'N/A'
  }

  if (!maxPlayers || minPlayers === maxPlayers) {
    return `${minPlayers ?? maxPlayers ?? 'N/A'} players`
  }

  return `${minPlayers ?? '?'}-${maxPlayers} players`
}

function formatPlaytime(playtime: number | null): string {
  if (!playtime) {
    return 'N/A'
  }

  return `${playtime} min`
}

function formatAge(age: number | null): string {
  if (!age) {
    return 'N/A'
  }

  return `${age}+`
}
</script>
