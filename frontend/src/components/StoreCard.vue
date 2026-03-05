<template>
  <div class="store-card">
    <div class="store-icon">🏪</div>
    <h3>{{ store.name }}</h3>
    <p class="location">📍 {{ store.location }}</p>
    <p v-if="store.contact" class="contact">✉️ {{ store.contact }}</p>
    <div class="actions">
      <button @click="$emit('edit', store)">Edit</button>
      <button class="btn-danger" @click="$emit('delete', store)">Delete</button>
    </div>
  </div>
</template>

<script setup>
defineProps({ store: { type: Object, required: true } })
defineEmits(['edit', 'delete'])
</script>

<style scoped>
.store-card {
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 1.2rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.store-icon {
  font-size: 2rem;
}

h3 {
  margin: 0;
}

.location,
.contact {
  color: #555;
  font-size: 0.88rem;
  margin: 0;
}

.actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

.actions button {
  padding: 0.3rem 0.9rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  cursor: pointer;
  background: #fff;
  font-size: 0.88rem;
}

.actions button:hover {
  background: #f0f0f0;
}

.btn-danger {
  border-color: #e74c3c !important;
  color: #e74c3c;
}

.btn-danger:hover {
  background: #fdecea !important;
}
</style>
