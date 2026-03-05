<template>
  <div class="home">
    <h1>Board Game Management</h1>
    <p class="subtitle">Manage board game stock across all stores</p>
    <div class="cards">
      <div class="card" @click="$router.push('/games')">
        <span class="icon">🎲</span>
        <h2>Board Games</h2>
        <p>Browse and manage the full board game catalogue</p>
      </div>
      <div class="card" @click="$router.push('/stores')">
        <span class="icon">🏪</span>
        <h2>Stores</h2>
        <p>View and manage store locations and inventory</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  text-align: center;
  padding: 2rem;
}

.subtitle {
  color: #666;
  margin-bottom: 2rem;
}

.cards {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  flex-wrap: wrap;
}

.card {
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 2rem;
  width: 220px;
  cursor: pointer;
  transition: box-shadow 0.2s;
}

.card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.icon {
  font-size: 2.5rem;
}

.card h2 {
  margin: 0.5rem 0;
}

.card p {
  color: #555;
  font-size: 0.9rem;
}
</style>
