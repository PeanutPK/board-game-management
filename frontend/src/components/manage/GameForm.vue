<template>
  <section class="manage-card shadow-md">
    <div class="panel-header">
      <h2>Add New Game</h2>
      <p class="form-note">
        Create complete metadata for a board game. Rent defaults to one-third of price.
      </p>
    </div>
    <form class="form-grid" @submit.prevent="submitForm">
      <label class="field">
        <span>Title</span>
        <input v-model.trim="form.title" type="text" maxlength="100" required />
      </label>

      <label class="field field-full">
        <span>Description</span>
        <textarea v-model.trim="form.description" rows="3" maxlength="1000" required></textarea>
      </label>

      <label class="field">
        <span>Price</span>
        <input v-model.number="form.price" type="number" min="0" step="0.01" required />
      </label>

      <label class="field">
        <span>Rent (auto)</span>
        <input :value="computedRent.toFixed(2)" type="number" step="0.01" disabled />
      </label>

      <label class="field">
        <span>Min Players</span>
        <input v-model.number="form.min_players" type="number" min="1" step="1" required />
      </label>

      <label class="field">
        <span>Max Players</span>
        <input
          v-model.number="form.max_players"
          type="number"
          :min="form.min_players || 1"
          step="1"
          required
        />
      </label>

      <label class="field">
        <span>Average Playtime (minutes)</span>
        <input v-model.number="form.average_playtime" type="number" min="0" step="1" required />
      </label>

      <label class="field">
        <span>Recommended Age</span>
        <input v-model.number="form.recommended_age" type="number" min="0" step="1" required />
      </label>

      <label class="field">
        <span>Initial Stock</span>
        <input v-model.number="form.stock" type="number" min="0" step="1" required />
      </label>

      <div class="actions field-full">
        <button type="submit" :disabled="submitting" class="action-btn primary">
          {{ submitting ? 'Adding...' : 'Add Game' }}
        </button>
      </div>
    </form>
  </section>
</template>

<script setup lang="ts">
import { computed, reactive } from 'vue'
import type { GameCreate } from '@/api/games'

defineProps<{
  submitting: boolean
}>()

const emit = defineEmits<{
  submit: [payload: GameCreate]
}>()

const form = reactive<GameCreate>({
  title: '',
  description: '',
  price: 0,
  rent: 0,
  min_players: 1,
  max_players: 4,
  average_playtime: 60,
  recommended_age: 8,
  stock: 0,
})

const computedRent = computed(() => {
  const price = Number.isFinite(form.price) ? Math.max(form.price, 0) : 0
  return Math.round((price / 3) * 100) / 100
})

function submitForm() {
  if (
    form.price < 0 ||
    form.stock < 0 ||
    form.min_players < 1 ||
    form.max_players < form.min_players
  ) {
    return
  }

  emit('submit', {
    title: form.title,
    description: form.description,
    price: form.price,
    rent: computedRent.value,
    min_players: form.min_players,
    max_players: form.max_players,
    average_playtime: Math.max(0, form.average_playtime),
    recommended_age: Math.max(0, form.recommended_age),
    stock: form.stock,
  })

  form.title = ''
  form.description = ''
  form.price = 0
  form.rent = 0
  form.min_players = 1
  form.max_players = 4
  form.average_playtime = 60
  form.recommended_age = 8
  form.stock = 0
}
</script>
