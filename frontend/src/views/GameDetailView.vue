<template>
  <section class="view detail-view">
    <div v-if="loading" class="detail-loading shadow-md">Loading game details...</div>

    <div v-else-if="errorMessage" class="detail-error shadow-md">
      <h1>Game not available</h1>
      <p>{{ errorMessage }}</p>
      <div class="detail-actions">
        <router-link to="/game" class="action-btn primary">Back to Games</router-link>
      </div>
    </div>

    <template v-else-if="game">
      <GameDetailHero
        :game="game"
        :is-logged-in="isLoggedIn"
        :review-count="reviewCount"
        :display-average-rating="displayAverageRating"
        @rent="openBookingModal"
        @buy="openOrderModal"
      />

      <GameSummaryCard :game="game" />

      <ReviewSection
        :reviews="reviews"
        :current-username="currentUsername"
        :current-user-review="currentUserReview"
        :is-logged-in="isLoggedIn"
        :review-form="reviewForm"
        :submitting="submitting"
        :form-message="formMessage"
        :message-type="messageType"
        @submit-review="handleSubmitReview"
        @update:review-form="reviewForm = $event"
      />

      <div v-if="showBookingModal" class="modal">
        <div class="modal-content">
          <button class="close" type="button" @click="showBookingModal = false">&times;</button>
          <h2>Rent {{ game.title }}</h2>
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
          <h2>Buy {{ game.title }}</h2>
          <form @submit.prevent="handleOrder">
            <label>Quantity:</label>
            <input
              v-model.number="orderData.quantity"
              type="number"
              min="1"
              :max="game.stock"
              required
            />
            <p class="total">Total: ${{ (game.price * (orderData.quantity || 1)).toFixed(2) }}</p>
            <button type="submit" class="action-btn secondary">Place Order</button>
          </form>
        </div>
      </div>
    </template>
  </section>
</template>

<script setup lang="ts">
import '@/assets/gamelist.css'
import '@/assets/gamedetail.css'

import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getToken, getUsername } from '@/api/auth'
import { createBooking } from '@/api/bookings'
import type { BookingCreate } from '@/api/bookings'
import { getGame, type Game } from '@/api/games'
import { createOrder } from '@/api/orders'
import GameDetailHero from '@/components/game/GameDetailHero.vue'
import GameSummaryCard from '@/components/game/GameSummaryCard.vue'
import ReviewSection from '@/components/game/ReviewSection.vue'
import {
  createOrUpdateGameReview,
  getGameReviews,
  type Review,
  type ReviewCreate,
} from '@/api/reviews'

const route = useRoute()

const game = ref<Game | null>(null)
const reviews = ref<Review[]>([])
const loading = ref(true)
const submitting = ref(false)
const errorMessage = ref('')
const formMessage = ref('')
const messageType = ref<'success' | 'error' | ''>('')
const showBookingModal = ref(false)
const showOrderModal = ref(false)

const bookingData = ref<BookingCreate>({
  game_id: 0,
  return_date: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString().split('T')[0] ?? '',
})

const orderData = ref({
  game_id: 0,
  quantity: 1,
})

const reviewForm = ref<ReviewCreate>({
  rating: 5,
  comment: '',
})

const currentUsername = getUsername() ?? ''
const isLoggedIn = computed(() => !!getToken())
const reviewCount = computed(() => reviews.value.length)
const currentUserReview = computed(() => {
  if (!currentUsername) {
    return null
  }

  return reviews.value.find((review) => review.username === currentUsername) ?? null
})
const displayAverageRating = computed(() => {
  if (reviews.value.length > 0) {
    const total = reviews.value.reduce((sum, review) => sum + review.rating, 0)
    return (total / reviews.value.length).toFixed(1)
  }

  const rating = game.value?.average_rating
  return rating === null || rating === undefined ? 'NR' : rating.toFixed(1)
})

watch(
  currentUserReview,
  (review) => {
    if (review) {
      reviewForm.value = {
        rating: review.rating,
        comment: review.comment,
      }
      return
    }

    reviewForm.value = {
      rating: 5,
      comment: '',
    }
  },
  { immediate: true },
)

onMounted(async () => {
  await loadGameDetail()
})

watch(
  () => route.params.gameId,
  async () => {
    await loadGameDetail()
  },
)

async function loadGameDetail() {
  loading.value = true
  errorMessage.value = ''

  try {
    const gameId = Number(route.params.gameId)
    if (!Number.isFinite(gameId) || gameId <= 0) {
      throw new Error('Invalid game id')
    }

    const [gameResponse, reviewResponse] = await Promise.all([
      getGame(gameId),
      getGameReviews(gameId),
    ])

    game.value = gameResponse
    reviews.value = reviewResponse
  } catch (error) {
    console.error('Failed to load game details:', error)
    game.value = null
    reviews.value = []
    errorMessage.value =
      'Unable to load the selected game. Please return to the game list and try again.'
  } finally {
    loading.value = false
  }
}

async function handleSubmitReview() {
  if (!game.value) {
    return
  }

  if (!isLoggedIn.value) {
    messageType.value = 'error'
    formMessage.value = 'Please log in to submit a review.'
    return
  }

  submitting.value = true
  formMessage.value = ''
  messageType.value = ''

  try {
    await createOrUpdateGameReview(game.value.id, {
      rating: reviewForm.value.rating,
      comment: reviewForm.value.comment.trim(),
    })
    reviews.value = await getGameReviews(game.value.id)
    messageType.value = 'success'
    formMessage.value = 'Your review has been saved.'
  } catch (error) {
    console.error('Failed to save review:', error)
    messageType.value = 'error'
    formMessage.value = 'Unable to save your review. Please try again.'
  } finally {
    submitting.value = false
  }
}

function openBookingModal() {
  if (!game.value || !isLoggedIn.value) {
    return
  }

  bookingData.value = {
    game_id: game.value.id,
    return_date: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString().split('T')[0] ?? '',
  }
  showBookingModal.value = true
}

function openOrderModal() {
  if (!game.value || !isLoggedIn.value) {
    return
  }

  orderData.value = {
    game_id: game.value.id,
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
    showBookingModal.value = false
    await loadGameDetail()
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
    showOrderModal.value = false
    await loadGameDetail()
    alert('Order placed successfully!')
  } catch (error) {
    console.error('Failed to place order:', error)
    alert('Failed to place order')
  }
}
</script>
