<template>
  <div id="app">
    <header>
      <Navbar />
    </header>

    <main>
      <RouterView />
    </main>

    <footer>
      <PageFooter />
    </footer>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
import PageFooter from './components/PageFooter.vue'
</script>
