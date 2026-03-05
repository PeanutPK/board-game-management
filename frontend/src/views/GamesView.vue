<template>
  <div class="games-view">
    <h1>Board Games</h1>

    <div class="toolbar">
      <button class="btn-primary" @click="openCreateModal">+ Add Game</button>
    </div>

    <div v-if="loading" class="loading">Loading games…</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="grid">
      <GameCard
        v-for="game in games"
        :key="game.id"
        :game="game"
        @edit="openEditModal"
        @delete="deleteGame"
      />
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h2>{{ editingGame ? 'Edit Game' : 'Add Game' }}</h2>
        <form @submit.prevent="saveGame">
          <label>Title
            <input v-model="form.title" required />
          </label>
          <label>Genre
            <input v-model="form.genre" required />
          </label>
          <label>Min Players
            <input v-model.number="form.min_players" type="number" min="1" required />
          </label>
          <label>Max Players
            <input v-model.number="form.max_players" type="number" min="1" required />
          </label>
          <label>Available Copies
            <input v-model.number="form.available_copies" type="number" min="0" required />
          </label>
          <label>Description
            <textarea v-model="form.description" rows="3"></textarea>
          </label>
          <div class="modal-actions">
            <button type="button" @click="closeModal">Cancel</button>
            <button type="submit" class="btn-primary">Save</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { gamesApi } from '../services/api'
import GameCard from '../components/GameCard.vue'

const games = ref([])
const loading = ref(false)
const error = ref(null)
const showModal = ref(false)
const editingGame = ref(null)

const defaultForm = () => ({
  title: '',
  genre: '',
  min_players: 2,
  max_players: 4,
  available_copies: 1,
  description: '',
})

const form = ref(defaultForm())

async function fetchGames() {
  loading.value = true
  error.value = null
  try {
    const res = await gamesApi.list()
    games.value = res.data
  } catch (e) {
    error.value = 'Failed to load games. Is the backend running?'
  } finally {
    loading.value = false
  }
}

function openCreateModal() {
  editingGame.value = null
  form.value = defaultForm()
  showModal.value = true
}

function openEditModal(game) {
  editingGame.value = game
  form.value = { ...game }
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

async function saveGame() {
  try {
    if (editingGame.value) {
      await gamesApi.update(editingGame.value.id, form.value)
    } else {
      await gamesApi.create(form.value)
    }
    closeModal()
    fetchGames()
  } catch (e) {
    alert('Failed to save game.')
  }
}

async function deleteGame(game) {
  if (!confirm(`Delete "${game.title}"?`)) return
  try {
    await gamesApi.remove(game.id)
    fetchGames()
  } catch (e) {
    alert('Failed to delete game.')
  }
}

onMounted(fetchGames)
</script>

<style scoped>
.games-view {
  padding: 2rem;
}

.toolbar {
  margin-bottom: 1.5rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.2rem;
}

.loading,
.error {
  text-align: center;
  padding: 2rem;
  color: #888;
}

.error {
  color: #c0392b;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: #fff;
  border-radius: 12px;
  padding: 2rem;
  width: 420px;
  max-width: 95vw;
}

.modal h2 {
  margin-top: 0;
}

form label {
  display: flex;
  flex-direction: column;
  margin-bottom: 0.8rem;
  font-size: 0.9rem;
  color: #444;
}

form input,
form textarea {
  margin-top: 0.25rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1rem;
}

.btn-primary {
  background: #42b883;
  color: white;
  border: none;
  padding: 0.5rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
}

.btn-primary:hover {
  background: #33a06f;
}
</style>
