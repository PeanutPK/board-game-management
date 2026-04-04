<template>
  <div class="customer-layout">
    <div class="content-wrapper">
      <slot />
    </div>
    <footer class="footer">
      <p>&copy; 2024 Board Game Management. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
// Customer specific logic can go here
</script>

<style scoped>
.customer-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content-wrapper {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 2rem;
  margin-top: 4rem;
  border-top: 1px solid #444;
}

.footer p {
  margin: 0;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 1rem;
  }

  .footer {
    padding: 1rem;
  }
}
</style>