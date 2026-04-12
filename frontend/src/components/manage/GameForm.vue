<template>
  <section class="manage-card">
    <h2 class="title">Add New Game</h2>

    <form class="form-grid" @submit.prevent="submitForm">
      <label class="field">
        <span>Title</span>
        <input v-model.trim="form.title" type="text" maxlength="100" required />
      </label>

      <label class="field field-full">
        <span>Description</span>
        <textarea v-model.trim="form.description" rows="3" maxlength="1000" required></textarea>
      </label>

      <label class="field">
        <span>Price</span>
        <input v-model.number="form.price" type="number" min="0" step="0.01" required />
      </label>

      <label class="field">
        <span>Initial Stock</span>
        <input v-model.number="form.stock" type="number" min="0" step="1" required />
      </label>

      <div class="actions field-full">
        <button type="submit" :disabled="submitting">{{ submitting ? 'Adding...' : 'Add Game' }}</button>
      </div>
    </form>
  </section>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import type { GameCreate } from '@/api/games'

defineProps<{
  submitting: boolean
}>()

const emit = defineEmits<{
  submit: [payload: GameCreate]
}>()

const form = reactive<GameCreate>({
  title: '',
  description: '',
  price: 0,
  stock: 0,
})

function submitForm() {
  if (form.price < 0 || form.stock < 0) {
    return
  }

  emit('submit', {
    title: form.title,
    description: form.description,
    price: form.price,
    stock: form.stock,
  })
}
</script>

<style scoped>
.manage-card {
  background: #f8f9fb;
  border: 1px solid #d9dde5;
  border-radius: 12px;
  padding: 1rem;
}

.title {
  margin: 0 0 0.75rem;
  font-size: 1.15rem;
  font-weight: 700;
}

.form-grid {
  display: grid;
  gap: 0.75rem;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.field-full {
  grid-column: 1 / -1;
}

input,
textarea,
button {
  font: inherit;
}

input,
textarea {
  border: 1px solid #c4cad6;
  border-radius: 8px;
  padding: 0.5rem 0.65rem;
}

.actions {
  display: flex;
  justify-content: flex-end;
}

button {
  border: 0;
  border-radius: 8px;
  padding: 0.55rem 0.95rem;
  background: #145c9e;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
