<template>
  <section class="review-layout">
    <article class="review-form-card left-card shadow-md">
      <p class="eyebrow">Your review</p>
      <h2>{{ currentUserReview ? 'Update your review' : 'Leave a review' }}</h2>

      <template v-if="isLoggedIn">
        <form class="review-form" @submit.prevent="emit('submit-review')">
          <label>
            Rating
            <div class="star-rating" role="radiogroup" aria-label="Choose a rating">
              <button
                v-for="value in [1, 2, 3, 4, 5]"
                :key="value"
                type="button"
                class="star-button"
                :class="{ active: selectedRating >= value }"
                :aria-pressed="selectedRating >= value"
                :aria-label="`${value} star${value === 1 ? '' : 's'}`"
                @click="selectedRating = value"
              >
                <Icon icon="iconoir:star-solid" class="star-icon" />
              </button>
            </div>
          </label>

          <label>
            Comment
            <textarea
              v-model.trim="commentText"
              placeholder="Share what you liked, what could be better, or who this game is for."
            />
          </label>

          <p class="helper-text" v-if="currentUserReview">
            You already reviewed this game. Submitting again will update your review.
          </p>

          <p v-if="formMessage" :class="['helper-text', messageType]">{{ formMessage }}</p>

          <button type="submit" class="action-btn primary" :disabled="submitting">
            {{ submitting ? 'Saving...' : 'Submit Review' }}
          </button>
        </form>
      </template>

      <template v-else>
        <p class="helper-text">Please log in to leave a review for this game.</p>
        <router-link to="/auth" class="action-btn primary">Go to Login</router-link>
      </template>
    </article>
    <article class="review-list-card shadow-md">
      <div class="panel-header">
        <div>
          <p class="eyebrow">Player feedback</p>
          <h2>Reviews</h2>
        </div>
      </div>

      <div v-if="reviews.length === 0" class="helper-text">
        No one has reviewed this game yet. Be the first.
      </div>

      <div v-else class="review-list">
        <ReviewCard
          v-for="review in reviews"
          :key="review.id"
          :review="review"
          :current-username="currentUsername"
        />
      </div>
    </article>

    <article class="review-form-card right-card shadow-md">
      <div class="panel-header">
        <div>
          <p class="eyebrow">Your review</p>
          <h3>{{ currentUserReview ? 'Update your review' : 'Leave a review' }}</h3>
        </div>
      </div>

      <template v-if="isLoggedIn">
        <form class="review-form" @submit.prevent="emit('submit-review')">
          <label>
            Rating
            <div class="star-rating" role="radiogroup" aria-label="Choose a rating">
              <button
                v-for="value in [1, 2, 3, 4, 5]"
                :key="value"
                type="button"
                class="star-button"
                :class="{ active: selectedRating >= value }"
                :aria-pressed="selectedRating >= value"
                :aria-label="`${value} star${value === 1 ? '' : 's'}`"
                @click="selectedRating = value"
              >
                <Icon icon="iconoir:star-solid" class="star-icon" />
              </button>
            </div>
          </label>

          <label>
            Comment
            <textarea
              v-model.trim="commentText"
              placeholder="Share what you liked, what could be better, or who this game is for."
              required
            />
          </label>

          <p class="helper-text" v-if="currentUserReview">
            You already reviewed this game. Submitting again will update your review.
          </p>

          <p v-if="formMessage" :class="['helper-text', messageType]">{{ formMessage }}</p>

          <button type="submit" class="action-btn primary" :disabled="submitting">
            {{ submitting ? 'Saving...' : 'Submit Review' }}
          </button>
        </form>
      </template>

      <template v-else>
        <p class="helper-text">Please log in to leave a review for this game.</p>
        <router-link to="/auth" class="action-btn primary">Go to Login</router-link>
      </template>
    </article>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Review, ReviewCreate } from '@/api/reviews'
import ReviewCard from '@/components/game/ReviewCard.vue'
import { Icon } from '@iconify/vue'

const props = defineProps<{
  reviews: Review[]
  currentUsername: string
  currentUserReview: Review | null
  isLoggedIn: boolean
  reviewForm: ReviewCreate
  submitting: boolean
  formMessage: string
  messageType: 'success' | 'error' | ''
}>()

const emit = defineEmits<{
  (e: 'submit-review'): void
  (e: 'update:review-form', value: ReviewCreate): void
}>()

const commentText = computed({
  get: () => props.reviewForm.comment,
  set: (value: string) =>
    emit('update:review-form', {
      ...props.reviewForm,
      comment: value,
    }),
})

const selectedRating = computed({
  get: () => props.reviewForm.rating,
  set: (value: number) =>
    emit('update:review-form', {
      ...props.reviewForm,
      rating: Number(value),
    }),
})
</script>
