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

    <section class="list-section shadow-md">
      <div class="section-head list-head">
        <div>
          <p class="eyebrow">List</p>
          <h2>All Games</h2>
        </div>

        <div class="filters">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search games..."
            class="search-input"
          />
          <select v-model="sortBy" class="sort-select">
            <option value="title">Sort by Title</option>
            <option value="rating">Sort by Rating</option>
            <option value="price">Sort by Price</option>
            <option value="stock">Sort by Stock</option>
          </select>
        </div>
      </div>

      <div v-if="loading" class="loading-card">Loading games...</div>

      <div v-else-if="filteredGames.length === 0" class="empty-state">
        <p>No games found</p>
      </div>

      <div v-else class="games-grid">
        <article v-for="game in filteredGames" :key="game.id" class="game-card">
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
import { computed, onMounted, ref, watch } from 'vue'
import { getToken } from '../api/auth'
import { createBooking } from '../api/bookings'
import type { BookingCreate } from '../api/bookings'
import { getGames, getTrendingGames, type Game } from '../api/games'
import { createOrder } from '../api/orders'
import TrendingCarousel from '../components/TrendingCarousel.vue'

import '@/assets/gamelist.css'

const games = ref<Game[]>([])
const trendingGames = ref<Game[]>([])
const loading = ref(false)
const isLoggedIn = ref(!!getToken())
const searchQuery = ref('')
const sortBy = ref<'title' | 'rating' | 'price' | 'stock'>('rating')
const currentTrendIndex = ref(0)

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

const filteredGames = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  const result = games.value.filter((game) => game.title.toLowerCase().includes(query))

  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'price':
        return a.price - b.price
      case 'stock':
        return b.stock - a.stock
      case 'rating':
        return (b.average_rating ?? 0) - (a.average_rating ?? 0)
      default:
        return a.title.localeCompare(b.title)
    }
  })

  return result
})

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

async function fetchGameData() {
  loading.value = true
  try {
    const [gameList, trendingList] = await Promise.all([getGames(0, 20), getTrendingGames(4)])
    games.value = gameList
    trendingGames.value = trendingList
  } catch (error) {
    console.error('Failed to fetch games:', error)
  } finally {
    loading.value = false
  }
}
</script>
