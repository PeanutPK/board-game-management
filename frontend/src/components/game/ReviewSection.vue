<template>
  <section class="review-layout">
    <ReviewFormCard
      side-class="left-card"
      :current-user-review="currentUserReview"
      :is-logged-in="isLoggedIn"
      :review-form="reviewForm"
      :submitting="submitting"
      :form-message="formMessage"
      :message-type="messageType"
      @submit-review="emit('submit-review')"
      @update:review-form="emit('update:review-form', $event)"
    />

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

    <ReviewFormCard
      side-class="right-card"
      heading-tag="h3"
      :use-panel-header="true"
      :textarea-required="true"
      :current-user-review="currentUserReview"
      :is-logged-in="isLoggedIn"
      :review-form="reviewForm"
      :submitting="submitting"
      :form-message="formMessage"
      :message-type="messageType"
      @submit-review="emit('submit-review')"
      @update:review-form="emit('update:review-form', $event)"
    />
  </section>
</template>

<script setup lang="ts">
import type { Review, ReviewCreate } from '@/api/reviews'
import ReviewCard from '@/components/game/ReviewCard.vue'
import ReviewFormCard from '@/components/game/ReviewFormCard.vue'

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
</script>
