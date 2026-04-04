<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <nav>
        <router-link to="/dashboard" class="nav-item">Dashboard</router-link>
        <router-link to="/inventory" class="nav-item">Inventory</router-link>
      </nav>
    </aside>
    <main class="main-content">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
// Admin specific logic can go here
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 250px;
  background-color: #222;
  color: white;
  padding: 2rem 0;
  box-shadow: 2px 0 4px rgba(0, 0, 0, 0.1);
}

.sidebar nav {
  display: flex;
  flex-direction: column;
}

.nav-item {
  color: white;
  text-decoration: none;
  padding: 1rem 1.5rem;
  border-left: 3px solid transparent;
  transition: all 0.3s;
  display: block;
}

.nav-item:hover {
  background-color: #333;
  border-left-color: #4CAF50;
  color: #4CAF50;
}

.nav-item.router-link-active {
  background-color: #333;
  border-left-color: #4CAF50;
  color: #4CAF50;
}

.main-content {
  flex: 1;
  padding: 2rem;
  background-color: #f5f5f5;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .admin-layout {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
  }

  .sidebar nav {
    flex-direction: row;
    overflow-x: auto;
  }
}
</style>