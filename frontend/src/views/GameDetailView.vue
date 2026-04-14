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
      <section class="view-hero shadow-md">
        <div>
          <div>
            <p class="eyebrow">Game detail</p>
            <h1>{{ game.title }}</h1>
            <p class="subtext">Explore the game and share your review with other players.</p>
          </div>

          <div class="detail-actions">
            <router-link to="/game" class="action-btn secondary">Back to Games</router-link>
          </div>
        </div>

        <div class="detail-meta">
          <span :class="`availability ${game.is_available ? 'available' : 'unavailable'}`">
            {{ game.is_available ? 'Available' : 'Unavailable' }}
          </span>
          <div class="flex gap-[0.7rem]">
            <span class="stat-pill">{{ reviewCount }} Reviews</span>
            <span class="stat-pill">Community Rating: {{ displayAverageRating }}</span>
          </div>
        </div>
      </section>

      <section class="game-summary shadow-md">
        <div class="panel-header">
          <div>
            <p class="eyebrow">Game detail</p>
            <h2>Game Summary</h2>
          </div>
          <p class="subtext">Explore the game and share your review with other players.</p>
        </div>
        <section class="detail-card">
          <div class="detail-grid">
            <div class="detail-item">
              <span>Price</span>
              <strong>${{ game.price.toFixed(2) }}</strong>
            </div>
            <div class="detail-item">
              <span>Rent</span>
              <strong>{{
                game.rent !== null ? `$${game.rent.toFixed(2)}` : 'Not available'
              }}</strong>
            </div>
            <div class="detail-item">
              <span>Stock</span>
              <strong>{{ game.stock }}</strong>
            </div>
            <div class="detail-item">
              <span>Players</span>
              <strong>{{ formatPlayers(game.min_players, game.max_players) }}</strong>
            </div>
          </div>

          <div class="detail-grid compact" style="margin-top: 1rem">
            <div class="detail-item">
              <span>Playtime</span>
              <strong>{{ formatPlaytime(game.average_playtime) }}</strong>
            </div>
            <div class="detail-item">
              <span>Age</span>
              <strong>{{ formatAge(game.recommended_age) }}</strong>
            </div>
            <div class="detail-item">
              <span>Catalog Rating</span>
              <strong>{{ formatRating(game.average_rating) }}</strong>
            </div>
          </div>

          <p class="description" style="margin-top: 1rem">{{ game.description }}</p>
        </section>
      </section>

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
    </template>
  </section>
</template>

<script setup lang="ts">
import '@/assets/gamelist.css'
import '@/assets/gamedetail.css'

import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getToken, getUsername } from '@/api/auth'
import { getGame, type Game } from '@/api/games'
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

  return formatRating(game.value?.average_rating ?? null)
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

function formatRating(rating: number | null): string {
  if (rating === null || rating === undefined) {
    return 'NR'
  }

  return rating.toFixed(1)
}

function formatPlayers(minPlayers: number | null, maxPlayers: number | null): string {
  if (!minPlayers && !maxPlayers) {
    return 'N/A'
  }

  if (!maxPlayers || minPlayers === maxPlayers) {
    return `${minPlayers ?? maxPlayers ?? 'N/A'} players`
  }

  return `${minPlayers ?? '?'}-${maxPlayers} players`
}

function formatPlaytime(playtime: number | null): string {
  if (!playtime) {
    return 'N/A'
  }

  return `${playtime} min`
}

function formatAge(age: number | null): string {
  if (!age) {
    return 'N/A'
  }

  return `${age}+`
}

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
</script>
