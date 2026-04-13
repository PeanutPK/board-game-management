<template>
  <section class="manage-card shadow-md">
    <div class="header-row">
      <h2 class="title">Manage Stock</h2>
      <button
        type="button"
        class="action-btn secondary"
        :disabled="loading"
        @click="$emit('refresh')"
      >
        {{ loading ? 'Refreshing...' : 'Refresh' }}
      </button>
    </div>

    <div v-if="games.length === 0" class="empty">No games found.</div>

    <div v-else class="rows">
      <article v-for="game in games" :key="game.id" class="row-card">
        <div class="row-main">
          <h3 class="text-lg font-bold">{{ game.title }}</h3>
          <p class="border-2 p-1 border-gray-300 rounded-md max-h-25 overflow-auto">
            {{ game.description }}
          </p>
        </div>

        <div class="row-meta">
          <span>Price: ${{ game.price.toFixed(2) }}</span>
          <span>Rent: ${{ getRent(game).toFixed(2) }}</span>
          <span>Stock: {{ game.stock }}</span>
        </div>

        <div class="row-meta compact">
          <span>Players: {{ getMinPlayers(game) }}-{{ getMaxPlayers(game) }}</span>
          <span>Playtime: {{ getPlaytime(game) }}m</span>
          <span>Age: {{ getAge(game) }}+</span>
        </div>

        <div class="row-actions">
          <button
            type="button"
            class="action-btn secondary"
            :disabled="updatingGameId === game.id"
            @click="$emit('edit-game', game)"
          >
            Edit
          </button>

          <button
            type="button"
            class="btn minus"
            :disabled="updatingGameId === game.id || game.stock === 0"
            @click="$emit('adjust-stock', game, -1)"
          >
            -1
          </button>

          <button
            type="button"
            class="btn plus"
            :disabled="updatingGameId === game.id"
            @click="$emit('adjust-stock', game, 1)"
          >
            +1
          </button>

          <input
            :value="customStock[game.id] ?? game.stock"
            type="number"
            min="0"
            step="1"
            :disabled="updatingGameId === game.id"
            @input="updateCustomStock(game.id, $event)"
          />

          <button
            type="button"
            class="action-btn primary"
            :disabled="updatingGameId === game.id"
            @click="$emit('set-stock', game, Number(customStock[game.id] ?? game.stock))"
          >
            {{ updatingGameId === game.id ? 'Saving...' : 'Set Stock' }}
          </button>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import type { Game } from '@/api/games'

const props = defineProps<{
  games: Game[]
  loading: boolean
  updatingGameId: number | null
}>()

defineEmits<{
  refresh: []
  'adjust-stock': [game: Game, delta: number]
  'set-stock': [game: Game, stock: number]
  'edit-game': [game: Game]
}>()

const customStock = reactive<Record<number, number>>({})

watch(
  () => props.games,
  (newGames) => {
    for (const game of newGames) {
      customStock[game.id] = game.stock
    }
  },
  { immediate: true },
)

function updateCustomStock(gameId: number, event: Event) {
  const target = event.target as HTMLInputElement
  const parsed = Number(target.value)
  customStock[gameId] = Number.isFinite(parsed) && parsed >= 0 ? Math.floor(parsed) : 0
}

function getRent(game: Game): number {
  if (typeof game.rent === 'number') {
    return game.rent
  }
  return Math.round((game.price / 3) * 100) / 100
}

function getMinPlayers(game: Game): number {
  return typeof game.min_players === 'number' && game.min_players > 0 ? game.min_players : 1
}

function getMaxPlayers(game: Game): number {
  const minPlayers = getMinPlayers(game)
  if (typeof game.max_players === 'number' && game.max_players >= minPlayers) {
    return game.max_players
  }
  return minPlayers
}

function getPlaytime(game: Game): number {
  return typeof game.average_playtime === 'number' && game.average_playtime >= 0
    ? game.average_playtime
    : 0
}

function getAge(game: Game): number {
  return typeof game.recommended_age === 'number' && game.recommended_age >= 0
    ? game.recommended_age
    : 0
}
</script>
