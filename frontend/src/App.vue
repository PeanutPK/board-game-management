<template>
  <div id="app">
    <header class="shrink-0">
      <Navbar />
    </header>

    <main class="grow overflow-y-auto">
      <RouterView />
    </main>

    <footer class="shrink-0">
      <PageFooter />
    </footer>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import PageFooter from './components/PageFooter.vue'
console.clear()
</script>
