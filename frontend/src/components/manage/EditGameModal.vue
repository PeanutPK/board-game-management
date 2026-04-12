<template>
  <div v-if="modelValue" class="modal-backdrop" @click.self="emit('update:modelValue', false)">
    <section class="modal-panel shadow-md">
      <div class="modal-header">
        <h2>Edit Game</h2>
      </div>

      <form class="form-grid" @submit.prevent="submitEdit">
        <label class="field">
          <span>Title</span>
          <input v-model.trim="form.title" type="text" maxlength="100" required />
        </label>

        <label class="field field-full">
          <span>Description</span>
          <textarea v-model.trim="form.description" rows="4" maxlength="1000" required></textarea>
        </label>

        <label class="field">
          <span>Price</span>
          <input v-model.number="form.price" type="number" min="0" step="0.01" required />
        </label>

        <label class="field">
          <span>Rent</span>
          <input v-model.number="form.rent" type="number" min="0" step="0.01" required />
        </label>

        <label class="field">
          <span>Min Players</span>
          <input v-model.number="form.min_players" type="number" min="1" step="1" required />
        </label>

        <label class="field">
          <span>Max Players</span>
          <input v-model.number="form.max_players" type="number" :min="form.min_players || 1" step="1" required />
        </label>

        <label class="field">
          <span>Average Playtime</span>
          <input v-model.number="form.average_playtime" type="number" min="0" step="1" required />
        </label>

        <label class="field">
          <span>Recommended Age</span>
          <input v-model.number="form.recommended_age" type="number" min="0" step="1" required />
        </label>

        <label class="field">
          <span>Stock</span>
          <input v-model.number="form.stock" type="number" min="0" step="1" required />
        </label>

        <label class="field checkbox-field">
          <span>Available</span>
          <input v-model="form.is_available" type="checkbox" />
        </label>

        <div class="actions field-full">
          <button type="button" class="action-btn secondary" @click="emit('update:modelValue', false)">Cancel</button>
          <button type="submit" class="action-btn primary" :disabled="saving">
            {{ saving ? 'Saving...' : 'Save Changes' }}
          </button>
        </div>
      </form>
    </section>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import type { Game, GameUpdatePayload } from '@/api/games'

const props = defineProps<{
  modelValue: boolean
  game: Game | null
  saving: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  submit: [id: number, payload: GameUpdatePayload]
}>()

const form = reactive<GameUpdatePayload>({
  title: '',
  description: '',
  price: 0,
  rent: 0,
  min_players: 1,
  max_players: 1,
  average_playtime: 0,
  recommended_age: 0,
  stock: 0,
  is_available: true,
})

watch(
  () => props.game,
  (game) => {
    if (!game) {
      return
    }

    form.title = game.title
    form.description = game.description
    form.price = game.price
    form.rent = game.rent ?? Math.round((game.price / 3) * 100) / 100
    form.min_players = game.min_players ?? 1
    form.max_players = game.max_players ?? Math.max(1, game.min_players ?? 1)
    form.average_playtime = game.average_playtime ?? 0
    form.recommended_age = game.recommended_age ?? 0
    form.stock = game.stock
    form.is_available = game.is_available
  },
  { immediate: true },
)

function submitEdit() {
  if (!props.game) {
    return
  }

  const minPlayers = Math.max(1, Number(form.min_players || 1))
  const maxPlayers = Math.max(minPlayers, Number(form.max_players || minPlayers))

  emit('submit', props.game.id, {
    title: form.title,
    description: form.description,
    price: Math.max(0, Number(form.price || 0)),
    rent: Math.max(0, Number(form.rent || 0)),
    min_players: minPlayers,
    max_players: maxPlayers,
    average_playtime: Math.max(0, Number(form.average_playtime || 0)),
    recommended_age: Math.max(0, Number(form.recommended_age || 0)),
    stock: Math.max(0, Math.floor(Number(form.stock || 0))),
    is_available: Boolean(form.is_available),
  })
}
</script>
