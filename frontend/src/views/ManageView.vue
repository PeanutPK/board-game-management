<template>
  <section class="view">
    <section class="view-hero shadow-md">
      <div>
        <p class="eyebrow">Manager</p>
        <h1>Inventory Management</h1>
        <p class="subtext">Manage board game inventory, pricing, and stock levels.</p>
      </div>

      <button class="action-btn secondary" type="button" @click="isAddGameModalOpen = true">
        Add New Game
      </button>
    </section>

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
      <section class="stats-grid">
        <article class="stat-card shadow-md">
          <h3>Total Games</h3>
          <p>{{ totalGames }}</p>
        </article>
        <article class="stat-card shadow-md">
          <h3>Available</h3>
          <p>{{ availableCount }}</p>
        </article>
        <article class="stat-card shadow-md">
          <h3>Low Stock (&lt; 5)</h3>
          <p>{{ lowStockCount }}</p>
        </article>
      </section>

      <div class="layout-grid">
        <ManageStockTable
          :games="games"
          :loading="isLoadingGames"
          :updating-game-id="updatingGameId"
          :errorMessage="errorMessage"
          :successMessage="successMessage"
          :search-query="searchQuery"
          :sort-by="sortBy"
          :page-size="pageSize"
          :current-page="currentPage"
          :total-pages="totalPages"
          :total-games="totalGames"
          @refresh="loadGames"
          @adjust-stock="handleAdjustStock"
          @set-stock="handleSetStock"
          @edit-game="openEditModal"
          @search-change="handleSearchChange"
          @sort-change="handleSortChange"
          @page-size-change="handlePageSizeChange"
          @page-change="goToPage"
        />
      </div>

      <div
        v-if="isAddGameModalOpen"
        class="modal-backdrop"
        @click.self="isAddGameModalOpen = false"
      >
        <ManageGameForm :key="gameFormKey" :submitting="isAddingGame" @submit="handleCreateGame" />
      </div>

      <EditGameModal
        v-model="isEditModalOpen"
        :game="selectedGame"
        :saving="isSavingGameEdit"
        @submit="handleEditGame"
      />
    </template>
  </section>
</template>

<script setup lang="ts">
import '@/assets/gamelist.css'
import '@/assets/manage.css'

import { computed, onMounted, ref } from 'vue'
import type { Game, GameCreate, GameUpdatePayload, PaginatedGamesResponse } from '@/api/games'
import { createGame, getGames, updateGame } from '@/api/games'
import EditGameModal from '@/components/manage/EditGameModal.vue'
import ManageGameForm from '@/components/manage/GameForm.vue'
import ManageStockTable from '@/components/manage/StockTable.vue'
import { useUserStore } from '@/stores/counter'

const userStore = useUserStore()

const games = ref<Game[]>([])
const isLoadingGames = ref(false)
const isAddingGame = ref(false)
const updatingGameId = ref<number | null>(null)
const gameFormKey = ref(0)
const isAddGameModalOpen = ref(false)
const isEditModalOpen = ref(false)
const isSavingGameEdit = ref(false)
const selectedGame = ref<Game | null>(null)
const errorMessage = ref('')
const successMessage = ref('')

// Pagination and filtering state
const currentPage = ref(1)
const pageSize = ref(10)
const totalGames = ref(0)
const totalPages = ref(1)
const searchQuery = ref('')
const sortBy = ref<'title' | 'price_asc' | 'price_desc' | 'rating' | 'stock'>('title')

const canManage = computed(() => {
  const role = userStore.userRole
  return role === 'staff' || role === 'admin'
})

const availableCount = computed(() => games.value.filter((game) => game.is_available).length)
const lowStockCount = computed(() => games.value.filter((game) => game.stock < 5).length)

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
    const skip = (currentPage.value - 1) * pageSize.value
    const response: PaginatedGamesResponse = await getGames(
      skip,
      pageSize.value,
      false,
      searchQuery.value,
      -1,
      -1,
      sortBy.value,
    )

    games.value = response.items
    totalGames.value = response.total
    totalPages.value = response.total_pages
    currentPage.value = response.page
  } catch (error) {
    console.error('Failed to fetch games:', error)
    setErrorMessage('Failed to load games. Please try again.')
  } finally {
    isLoadingGames.value = false
  }
}

function resetToFirstPage() {
  currentPage.value = 1
  loadGames()
}

function handleSearchChange(value: string) {
  searchQuery.value = value
  resetToFirstPage()
}

function handleSortChange(value: 'title' | 'price_asc' | 'price_desc' | 'rating' | 'stock') {
  sortBy.value = value
  resetToFirstPage()
}

function handlePageSizeChange(value: number) {
  pageSize.value = value
  resetToFirstPage()
}

function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    loadGames()
  }
}

async function handleCreateGame(payload: GameCreate) {
  isAddingGame.value = true
  try {
    await createGame(payload)
    gameFormKey.value += 1
    isAddGameModalOpen.value = false
    setSuccessMessage('Game added successfully.')
    resetToFirstPage()
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
    await updateGame(game.id, { stock, is_available: stock > 0 })
    setSuccessMessage(`Stock updated for ${game.title}.`)
    await loadGames()
  } catch (error) {
    console.error('Failed to update stock:', error)
    setErrorMessage(`Failed to update stock for ${game.title}.`)
  } finally {
    updatingGameId.value = null
  }
}

function openEditModal(game: Game) {
  selectedGame.value = game
  isEditModalOpen.value = true
}

async function handleEditGame(gameId: number, payload: GameUpdatePayload) {
  isSavingGameEdit.value = true
  try {
    await updateGame(gameId, payload)
    isEditModalOpen.value = false
    setSuccessMessage('Game details updated successfully.')
    await loadGames()
  } catch (error) {
    console.error('Failed to update game details:', error)
    setErrorMessage('Failed to update game details. Please check the data and try again.')
  } finally {
    isSavingGameEdit.value = false
  }
}
</script>
