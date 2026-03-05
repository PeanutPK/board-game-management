<template>
  <div class="game-card">
    <div class="game-header">
      <span class="genre-badge">{{ game.genre }}</span>
    </div>
    <h3>{{ game.title }}</h3>
    <p class="description">{{ game.description }}</p>
    <div class="meta">
      <span>👥 {{ game.min_players }}–{{ game.max_players }} players</span>
      <span :class="['copies', game.available_copies === 0 ? 'out' : 'in']">
        {{ game.available_copies }} available
      </span>
    </div>
    <div class="actions">
      <button @click="$emit('edit', game)">Edit</button>
      <button class="btn-danger" @click="$emit('delete', game)">Delete</button>
    </div>
  </div>
</template>

<script setup>
defineProps({ game: { type: Object, required: true } })
defineEmits(['edit', 'delete'])
</script>

<style scoped>
.game-card {
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 1.2rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.game-header {
  display: flex;
  justify-content: flex-end;
}

.genre-badge {
  background: #e8f5ee;
  color: #2e7d4f;
  padding: 0.2rem 0.6rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

h3 {
  margin: 0;
}

.description {
  color: #666;
  font-size: 0.88rem;
  flex: 1;
}

.meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
}

.copies.in {
  color: #27ae60;
}

.copies.out {
  color: #c0392b;
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
