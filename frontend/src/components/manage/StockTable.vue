<template>
  <section class="manage-card">
    <div class="header-row">
      <h2 class="title">Manage Stock</h2>
      <button type="button" class="refresh" :disabled="loading" @click="$emit('refresh')">
        {{ loading ? 'Refreshing...' : 'Refresh' }}
      </button>
    </div>

    <div v-if="games.length === 0" class="empty">No games found.</div>

    <div v-else class="rows">
      <article v-for="game in games" :key="game.id" class="row-card">
        <div class="row-main">
          <h3>{{ game.title }}</h3>
          <p>{{ game.description }}</p>
        </div>

        <div class="row-meta">
          <span>Price: ${{ game.price.toFixed(2) }}</span>
          <span>Stock: {{ game.stock }}</span>
        </div>

        <div class="row-actions">
          <button
            type="button"
            class="btn soft"
            :disabled="updatingGameId === game.id || game.stock === 0"
            @click="$emit('adjust-stock', game, -1)"
          >
            -1
          </button>

          <button
            type="button"
            class="btn soft"
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
            class="btn"
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
</script>

<style scoped>
.manage-card {
  background: #f8f9fb;
  border: 1px solid #d9dde5;
  border-radius: 12px;
  padding: 1rem;
}

.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.title {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 700;
}

.refresh {
  border: 1px solid #c4cad6;
  border-radius: 8px;
  padding: 0.45rem 0.7rem;
  background: #fff;
  cursor: pointer;
}

.rows {
  display: grid;
  gap: 0.75rem;
}

.row-card {
  border: 1px solid #d6dce7;
  background: #fff;
  border-radius: 10px;
  padding: 0.75rem;
}

.row-main h3 {
  margin: 0;
}

.row-main p {
  margin: 0.25rem 0 0;
  color: #4a5060;
}

.row-meta {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
  color: #232838;
  font-weight: 600;
}

.row-actions {
  margin-top: 0.65rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  align-items: center;
}

.btn {
  border: 0;
  border-radius: 8px;
  padding: 0.45rem 0.75rem;
  background: #145c9e;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
}

.btn.soft {
  background: #2f3c56;
}

input {
  width: 110px;
  border: 1px solid #c4cad6;
  border-radius: 8px;
  padding: 0.45rem 0.55rem;
}

button:disabled,
.refresh:disabled,
input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.empty {
  color: #4a5060;
}
</style>
