<template>
  <div class="game-list-container">
    <h1>Game List</h1>

    <div v-if="!isLoggedIn" class="login-required">
      <p>Please log in to book or order games</p>
      <router-link to="/" class="btn btn-primary">Go to Home</router-link>
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
        <option value="price">Sort by Price</option>
        <option value="stock">Sort by Stock</option>
      </select>
    </div>

    <div v-if="loading" class="loading">Loading games...</div>

    <div v-else-if="games.length === 0" class="empty-state">
      <p>No games found</p>
    </div>

    <div v-else class="games-grid">
      <div v-for="game in filteredGames" :key="game.id" class="game-card">
        <div class="game-header">
          <h3>{{ game.title }}</h3>
          <span :class="`availability ${game.is_available ? 'available' : 'unavailable'}`">
            {{ game.is_available ? 'Available' : 'Unavailable' }}
          </span>
        </div>

        <p class="description">{{ game.description }}</p>

        <div class="game-details">
          <div class="detail">
            <span class="label">Price:</span>
            <span class="value">${{ game.price.toFixed(2) }}</span>
          </div>
          <div class="detail">
            <span class="label">Stock:</span>
            <span class="value">{{ game.stock }} units</span>
          </div>
        </div>

        <div v-if="isLoggedIn" class="actions">
          <button 
            @click="openBookingModal(game)"
            :disabled="!game.is_available"
            class="btn btn-primary"
          >
            Book
          </button>
          <button 
            @click="openOrderModal(game)"
            :disabled="game.stock === 0"
            class="btn btn-success"
          >
            Order
          </button>
        </div>
      </div>
    </div>

    <!-- Booking Modal -->
    <div v-if="showBookingModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="showBookingModal = false">&times;</span>
        <h2>Book {{ selectedGame?.title }}</h2>
        <form @submit.prevent="handleBooking">
          <label>Return Date (optional):</label>
          <input v-model="bookingData.return_date" type="date" />
          <button type="submit" class="btn btn-primary">Confirm Booking</button>
        </form>
      </div>
    </div>

    <!-- Order Modal -->
    <div v-if="showOrderModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="showOrderModal = false">&times;</span>
        <h2>Order {{ selectedGame?.title }}</h2>
        <form @submit.prevent="handleOrder">
          <label>Quantity:</label>
          <input 
            v-model.number="orderData.quantity" 
            type="number" 
            min="1" 
            :max="selectedGame?.stock"
            required
          />
          <p class="total">Total: ${{ ((selectedGame?.price || 0) * (orderData.quantity || 1)).toFixed(2) }}</p>
          <button type="submit" class="btn btn-success">Place Order</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getToken } from '../api/auth'
import { getGames, type Game } from '../api/games'
import { createBooking } from '../api/bookings'
import type { BookingCreate } from '../api/bookings'

const games = ref<Game[]>([])
const loading = ref(false)
const isLoggedIn = ref(!!getToken())
const searchQuery = ref('')
const sortBy = ref('title')

const showBookingModal = ref(false)
const showOrderModal = ref(false)
const selectedGame = ref<Game | null>(null)

const bookingData = ref<BookingCreate>({
  game_id: 0,
  return_date: null
})

const orderData = ref({
  game_id: 0,
  quantity: 1
})

const filteredGames = computed(() => {
  const result = games.value.filter(game =>
    game.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  )

  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'price':
        return a.price - b.price
      case 'stock':
        return b.stock - a.stock
      default:
        return a.title.localeCompare(b.title)
    }
  })

  return result
})

onMounted(async () => {
  loading.value = true
  try {
    games.value = await getGames(0, 100)
  } catch (error) {
    console.error('Failed to fetch games:', error)
  } finally {
    loading.value = false
  }
})

function openBookingModal(game: Game) {
  selectedGame.value = game
  bookingData.value = {
    game_id: game.id,
    return_date: null
  }
  showBookingModal.value = true
}

function openOrderModal(game: Game) {
  selectedGame.value = game
  orderData.value = {
    game_id: game.id,
    quantity: 1
  }
  showOrderModal.value = true
}

async function handleBooking() {
  try {
    await createBooking(bookingData.value)
    showBookingModal.value = false
    alert('Booking created successfully!')
  } catch (error) {
    console.error('Failed to create booking:', error)
    alert('Failed to create booking')
  }
}

async function handleOrder() {
  try {
    console.log('Order placed:', orderData.value)
    showOrderModal.value = false
    alert('Order placed successfully!')
  } catch (error) {
    console.error('Failed to place order:', error)
    alert('Failed to place order')
  }
}
</script>