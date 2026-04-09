<template>
  <div class="footer-container">
    <div class="footer-menu">
      <router-link to="/status" class="footer-link">Status</router-link>
      <router-link to="/privacy" class="footer-link">Privacy Policy</router-link>
      <router-link to="/contact" class="footer-link">Contact</router-link>
    </div>
    <div class="footer-copyright">
      <p>&copy; 2026 Board Game Management. All rights reserved.</p>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.footer-container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: end;
  justify-content: space-between;
  padding: 1rem 0;
  min-height: 5rem;
  width: 100%;
}

.footer-menu {
  display: flex;
  gap: 1rem;
}

.footer-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.6rem;
  border: 1px solid transparent;
  color: var(--color-cgainsboro);
  text-decoration: none;
  font-weight: 600;
  transition:
    background-color 0.2s ease,
    border-color 0.2s ease,
    transform 0.2s ease;
}

.footer-link:hover {
  text-decoration: underline;
}

.footer-link:active {
  transform: translateY(1px);
}

.footer-copyright {
  display: flex;
  color: var(--color-cgainsboro);
  font-size: 0.8rem;
  align-items: end;
  border-radius: 0.6rem;
  border: 1px solid transparent;
}

@media (max-width: 640px) {
  .footer-container {
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }
}
</style>
