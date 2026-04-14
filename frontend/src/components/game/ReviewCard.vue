<template>
  <section class="review-card">
    <div class="review-card-header">
      <div>
        <p class="review-author">{{ review.username }}</p>
        <span class="rating-badge">{{ review.rating }}/5</span>
      </div>
      <span v-if="currentUsername === review.username" class="stat-pill">Your review</span>
    </div>
    <p class="review-comment">{{ review.comment }}</p>
  </section>
</template>

<script setup lang="ts">
import type { Review } from '@/api/reviews'

defineProps<{
  review: Review
  currentUsername: string
}>()
</script>
