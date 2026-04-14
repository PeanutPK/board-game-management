<template>
  <article :class="['review-form-card', sideClass, 'shadow-md']">
    <div v-if="usePanelHeader" class="panel-header">
      <div>
        <p class="eyebrow">Your review</p>
        <component :is="headingTag">{{ titleText }}</component>
      </div>
    </div>

    <template v-else>
      <p class="eyebrow">Your review</p>
      <component :is="headingTag">{{ titleText }}</component>
    </template>

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
            :required="textareaRequired"
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
</template>

<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { computed } from 'vue'
import type { Review, ReviewCreate } from '@/api/reviews'

const props = withDefaults(
  defineProps<{
    currentUserReview: Review | null
    isLoggedIn: boolean
    reviewForm: ReviewCreate
    submitting: boolean
    formMessage: string
    messageType: 'success' | 'error' | ''
    headingTag?: 'h2' | 'h3'
    sideClass?: string
    usePanelHeader?: boolean
    textareaRequired?: boolean
  }>(),
  {
    headingTag: 'h2',
    sideClass: '',
    usePanelHeader: false,
    textareaRequired: false,
  },
)

const emit = defineEmits<{
  (e: 'submit-review'): void
  (e: 'update:review-form', value: ReviewCreate): void
}>()

const titleText = computed(() =>
  props.currentUserReview ? 'Update your review' : 'Leave a review',
)

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
