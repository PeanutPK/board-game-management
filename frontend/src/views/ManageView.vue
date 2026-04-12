<template>
  <section class="manage-view">
    <header class="page-head">
      <h1>Inventory Management</h1>
      <p>Add board games and manage stock levels.</p>
    </header>

    <div v-if="!userStore.isLoggedIn" class="guard-card">
      <h2>Login Required</h2>
      <p>Please sign in to access inventory tools.</p>
      <router-link to="/auth" class="guard-link">Go to Login</router-link>
    </div>

    <div v-else-if="!canManage" class="guard-card">
      <h2>Access Denied</h2>
      <p>Only staff and admin users can manage stock.</p>
      <router-link to="/" class="guard-link">Go Home</router-link>
    </div>

    <template v-else>
      <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success-msg">{{ successMessage }}</p>

      <div class="layout-grid">
        <ManageGameForm :key="gameFormKey" :submitting="isAddingGame" @submit="handleCreateGame" />
        <ManageStockTable
          :games="games"
          :loading="isLoadingGames"
          :updating-game-id="updatingGameId"
          @refresh="loadGames"
          @adjust-stock="handleAdjustStock"
          @set-stock="handleSetStock"
        />
      </div>
    </template>
  </section>
</template>

<script setup lang="ts">
import '@/assets/manage.css'

import { computed, onMounted, ref } from 'vue'
import type { Game, GameCreate } from '@/api/games'
import { createGame, getGames, updateGame } from '@/api/games'
import ManageGameForm from '@/components/manage/GameForm.vue'
import ManageStockTable from '@/components/manage/StockTable.vue'
import { useUserStore } from '@/stores/counter'

const userStore = useUserStore()

const games = ref<Game[]>([])
const isLoadingGames = ref(false)
const isAddingGame = ref(false)
const updatingGameId = ref<number | null>(null)
const gameFormKey = ref(0)
const errorMessage = ref('')
const successMessage = ref('')

const canManage = computed(() => {
  const role = userStore.userRole
  return role === 'staff' || role === 'admin'
})

onMounted(async () => {
  if (canManage.value) {
    await loadGames()
  }
})

function setSuccessMessage(message: string) {
  successMessage.value = message
  errorMessage.value = ''
}

function setErrorMessage(message: string) {
  errorMessage.value = message
  successMessage.value = ''
}

async function loadGames() {
  if (!canManage.value) {
    return
  }

  isLoadingGames.value = true
  try {
    games.value = await getGames(0, 100)
  } catch (error) {
    console.error('Failed to fetch games:', error)
    setErrorMessage('Failed to load games. Please try again.')
  } finally {
    isLoadingGames.value = false
  }
}

async function handleCreateGame(payload: GameCreate) {
  isAddingGame.value = true
  try {
    await createGame(payload)
    gameFormKey.value += 1
    setSuccessMessage('Game added successfully.')
    await loadGames()
  } catch (error) {
    console.error('Failed to create game:', error)
    setErrorMessage('Failed to add game. Check the form and try again.')
  } finally {
    isAddingGame.value = false
  }
}

async function handleAdjustStock(game: Game, delta: number) {
  const nextStock = Math.max(0, game.stock + delta)
  await persistStock(game, nextStock)
}

async function handleSetStock(game: Game, stock: number) {
  const normalizedStock = Number.isFinite(stock) ? Math.max(0, Math.floor(stock)) : 0
  await persistStock(game, normalizedStock)
}

async function persistStock(game: Game, stock: number) {
  updatingGameId.value = game.id
  try {
    await updateGame(game.id, { stock })
    setSuccessMessage(`Stock updated for ${game.title}.`)
    await loadGames()
  } catch (error) {
    console.error('Failed to update stock:', error)
    setErrorMessage(`Failed to update stock for ${game.title}.`)
  } finally {
    updatingGameId.value = null
  }
}
</script>
