<template>
  <div class="view">
    <section class="view-hero shadow-md">
      <div>
        <p class="eyebrow">Browse games</p>
        <h1>Game List</h1>
        <p class="subtext">Explore the catalog and check the highest rated games first.</p>
      </div>
    </section>

    <TrendingCarousel
      :trending-games="trendingGames"
      :loading="loading"
      :current-trend-index="currentTrendIndex"
      @rent="openBookingModal"
      @buy="openOrderModal"
      @update-index="currentTrendIndex = $event"
    />

    <section v-if="isGameListReady" class="list-section shadow-md">
      <div class="section-head">
        <div class="panel-header">
          <div>
            <p class="eyebrow">List</p>
            <h2>All Games</h2>
          </div>
        </div>

        <div class="filters">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search games..."
            class="search-input"
            @input="resetToFirstPage"
          />
          <select v-model="sortBy" class="sort-select" @change="resetToFirstPage">
            <option value="title">Sort by Title</option>
            <option value="rating">Sort by Rating</option>
            <option value="price_asc">Sort by Price (Low to High)</option>
            <option value="price_desc">Sort by Price (High to Low)</option>
            <option value="stock">Sort by Stock</option>
          </select>
          <select
            v-model.number="pageSize"
            class="page-size-select"
            @change="handlePageSizeChange"
          >
            <option :value="12">12 per page</option>
            <option :value="20">20 per page</option>
            <option :value="40">40 per page</option>
          </select>
        </div>
      </div>

      <div v-if="loading" class="loading-card">Loading games...</div>

      <div v-else-if="games.length === 0" class="empty-state">
        <p>No games found</p>
      </div>

      <div v-else class="games-grid">
        <article v-for="game in games" :key="game.id" class="game-card">
          <div class="game-header">
            <h3>{{ game.title }}</h3>
            <span :class="`availability ${game.is_available ? 'available' : 'unavailable'}`">
              {{ game.is_available ? 'Available' : 'Unavailable' }}
            </span>
          </div>

          <p class="description">{{ game.description }}</p>

          <div class="detail-grid">
            <div class="detail-item">
              <span>Rating</span>
              <strong>{{ formatRating(game.average_rating) }}</strong>
            </div>
            <div class="detail-item">
              <span>Price</span>
              <strong>${{ game.price.toFixed(2) }}</strong>
            </div>
            <div class="detail-item">
              <span>Stock</span>
              <strong>{{ game.stock }} units</strong>
            </div>
            <div class="detail-item">
              <span>Players</span>
              <strong>{{ formatPlayers(game) }}</strong>
            </div>
          </div>

          <div class="actions">
            <button
              @click="openBookingModal(game)"
              :disabled="!isLoggedIn || !game.is_available"
              class="action-btn primary"
              type="button"
            >
              Rent
            </button>
            <button
              @click="openOrderModal(game)"
              :disabled="!isLoggedIn || game.stock === 0"
              class="action-btn secondary"
              type="button"
            >
              Buy
            </button>
          </div>
        </article>
      </div>

      <section v-if="totalPages > 1" class="pagination-section">
        <button
          type="button"
          class="pagination-btn"
          :disabled="currentPage === 1"
          @click="goToPage(currentPage - 1)"
        >
          Previous
        </button>

        <div class="pagination-info">
          Page {{ currentPage }} of {{ totalPages }} ({{ totalGames }} total games)
        </div>

        <button
          type="button"
          class="pagination-btn"
          :disabled="currentPage === totalPages"
          @click="goToPage(currentPage + 1)"
        >
          Next
        </button>
      </section>
    </section>

    <section v-else class="list-section shadow-md">
      <div class="loading-card">Preparing game list...</div>
    </section>

    <div v-if="!isLoggedIn" class="login-required">
      <p>Please log in to rent or buy games</p>
      <router-link to="/" class="action-btn primary">Go to Home</router-link>
    </div>

    <div v-if="showBookingModal" class="modal">
      <div class="modal-content">
        <button class="close" type="button" @click="showBookingModal = false">&times;</button>
        <h2>Rent {{ selectedGame?.title }}</h2>
        <form @submit.prevent="handleBooking">
          <label>Return Date (default: 1 day):</label>
          <input v-model="bookingData.return_date" type="date" />
          <button type="submit" class="action-btn primary">Confirm Rental</button>
        </form>
      </div>
    </div>

    <div v-if="showOrderModal" class="modal">
      <div class="modal-content">
        <button class="close" type="button" @click="showOrderModal = false">&times;</button>
        <h2>Buy {{ selectedGame?.title }}</h2>
        <form @submit.prevent="handleOrder">
          <label>Quantity:</label>
          <input
            v-model.number="orderData.quantity"
            type="number"
            min="1"
            :max="selectedGame?.stock"
            required
          />
          <p class="total">
            Total: ${{ ((selectedGame?.price || 0) * (orderData.quantity || 1)).toFixed(2) }}
          </p>
          <button type="submit" class="action-btn secondary">Place Order</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import '@/assets/shared-controls.css'
import '@/assets/modal.css'
import '@/assets/gamelist.css'

import { computed, onMounted, ref, watch } from 'vue'
import { getToken } from '../api/auth'
import { createBooking } from '../api/bookings'
import type { BookingCreate } from '../api/bookings'
import { getGames, getTrendingGames, type Game } from '../api/games'
import { createOrder } from '../api/orders'
import TrendingCarousel from '../components/TrendingCarousel.vue'

const games = ref<Game[]>([])
const trendingGames = ref<Game[]>([])
const loading = ref(false)
const isLoggedIn = ref(!!getToken())
const searchQuery = ref('')
const sortBy = ref<'title' | 'rating' | 'price_asc' | 'price_desc' | 'stock'>('rating')
const currentTrendIndex = ref(0)
const gameListStorageKey = 'game-list-page-size'
const currentPage = ref(1)
const pageSize = ref<number | null>(null)
const totalGames = ref(0)
const totalPages = ref(1)

const showBookingModal = ref(false)
const showOrderModal = ref(false)
const selectedGame = ref<Game | null>(null)

const bookingData = ref<BookingCreate>({
  game_id: 0,
  return_date: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString().split('T')[0] ?? '', // default to 1 day later
})

const orderData = ref({
  game_id: 0,
  quantity: 1,
})

const isGameListReady = computed(() => pageSize.value !== null)
const resolvedPageSize = computed(() => pageSize.value ?? 12)

watch(trendingGames, (nextGames) => {
  if (nextGames.length === 0) {
    currentTrendIndex.value = 0
    return
  }

  if (currentTrendIndex.value >= nextGames.length) {
    currentTrendIndex.value = 0
  }
})

onMounted(async () => {
  pageSize.value = readStoredPageSize(12)
  await fetchGameData()
})

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

function openBookingModal(game: Game) {
  if (!isLoggedIn.value) return

  selectedGame.value = game
  bookingData.value = {
    game_id: game.id,
    return_date: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString().split('T')[0] ?? '',
  }
  showBookingModal.value = true
}

function openOrderModal(game: Game) {
  if (!isLoggedIn.value) return

  selectedGame.value = game
  orderData.value = {
    game_id: game.id,
    quantity: 1,
  }
  showOrderModal.value = true
}

async function handleBooking() {
  try {
    const today = new Date().toISOString().split('T')[0] ?? ''
    const returnDate = bookingData.value.return_date
    if (!returnDate || returnDate < today) {
      alert('Return date cannot be in the past')
      return
    }
    await createBooking(bookingData.value)
    await fetchGameData()
    showBookingModal.value = false
    alert('Booking created successfully!')
  } catch (error) {
    console.error('Failed to create booking:', error)
    alert('Failed to create booking')
  }
}

async function handleOrder() {
  try {
    await createOrder({
      game_id: orderData.value.game_id,
      quantity: orderData.value.quantity,
    })
    await fetchGameData()
    showOrderModal.value = false
    alert('Order placed successfully!')
  } catch (error) {
    console.error('Failed to place order:', error)
    alert('Failed to place order')
  }
}

function resetToFirstPage() {
  currentPage.value = 1
  fetchGameData()
}

function readStoredPageSize(defaultValue: number): number {
  const storedValue = window.localStorage.getItem(gameListStorageKey)
  const parsedValue = storedValue ? Number(storedValue) : Number.NaN

  return Number.isFinite(parsedValue) && parsedValue > 0 ? Math.floor(parsedValue) : defaultValue
}

function handlePageSizeChange(event: Event) {
  const target = event.target as HTMLSelectElement
  const parsedValue = Number(target.value)
  const nextPageSize = Number.isFinite(parsedValue) ? parsedValue : 12

  pageSize.value = nextPageSize
  window.localStorage.setItem(gameListStorageKey, String(nextPageSize))
  resetToFirstPage()
}

function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    fetchGameData()
  }
}

async function fetchGameData() {
  if (pageSize.value === null) {
    return
  }

  loading.value = true
  try {
    const skip = (currentPage.value - 1) * resolvedPageSize.value
    const [gameResponse, trendingList] = await Promise.all([
      getGames(
        skip,
        resolvedPageSize.value,
        false,
        searchQuery.value,
        -1,
        -1,
        sortBy.value,
      ),
      getTrendingGames(4),
    ])

    games.value = gameResponse.items
    totalGames.value = gameResponse.total
    totalPages.value = gameResponse.total_pages
    currentPage.value = gameResponse.page
    trendingGames.value = trendingList
  } catch (error) {
    console.error('Failed to fetch games:', error)
  } finally {
    loading.value = false
  }
}
</script>
