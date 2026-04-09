<template>
  <section class="hero">
    <div class="left-hero">
      <img :src="generatedLogo" alt="Board Game Management logo" class="hero-logo" />
    </div>
    <div class="right-hero">
      <h1 class="text-cblack">Welcome to Board Game Management</h1>
      <p class="hero-subtitle">Browse, book, and order your favorite board games in one place.</p>

      <div class="hero-stats">
        <div class="stat-pill">
          <span class="stat-label">Games Listed</span>
          <strong>{{ gameStats.total }}</strong>
        </div>
        <div class="stat-pill">
          <span class="stat-label">Available Now</span>
          <strong>{{ gameStats.available }}</strong>
        </div>
        <router-link to="/game" class="browse-link">Browse</router-link>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import generatedLogo from '../assets/generatedLogo.png'
import { ref, onMounted } from 'vue'
import { getGameStats } from '../api/games'

const gameStats = ref<{ total: number; available: number }>({ total: 0, available: 0 })

onMounted(async () => {
  try {
    gameStats.value = await getGameStats()
    console.log('Game stats fetched successfully:', gameStats.value)
  } catch (error) {
    console.error('Failed to fetch game stats:', error)
  }
})
</script>

<style scoped>
h1 {
  margin: 0.45rem 0 0.7rem;
  line-height: 1.12;
  font-size: clamp(1.9rem, 3.2vw, 2.9rem);
  font-weight: bolder;
}

.hero {
  display: grid;
  grid-template-columns: minmax(200px, 320px) minmax(280px, 1fr);
  align-items: center;
  gap: clamp(1rem, 2.5vw, 2rem);
  width: min(1080px, 100%);
  margin: 0 auto;
  padding: 0.75rem 1rem;
}

.left-hero {
  width: 100%;
  height: clamp(150px, 24vw, 240px);
  min-width: 0;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-logo {
  width: 100%;
  height: 100%;
  max-width: 320px;
  display: block;
  object-fit: contain;
  object-position: center;
}

.right-hero {
  flex: 1;
  width: 100%;
  min-width: 0;
}

.hero-subtitle {
  margin: 0;
  color: var(--color-cdarkslategray);
  max-width: 60ch;
  line-height: 1.6;
}

.hero-stats {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 0.7rem;
  margin-top: 1rem;
}

.stat-pill {
  padding: 0.5rem 0.8rem;
  border-radius: 0.75rem;
  border: 1px solid var(--color-cdarkslategray);
  background: var(--color-cgainsboro);
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
}

.stat-label {
  color: var(--color-cdarkslategray);
  font-size: 0.8rem;
}

.browse-link {
  color: var(--color-cdarkslategray);
  font-weight: 700;
  text-decoration: none;
  border-bottom: 2px solid transparent;
  margin-left: 0;
  align-self: center;
}

.browse-link:hover {
  border-color: var(--color-cdarkslategray);
}

.section-head {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.8rem;
}

.section-head h2 {
  margin: 0;
  color: var(--color-cblack);
}

@media (max-width: 900px) {
  .hero {
    grid-template-columns: minmax(180px, 260px) 1fr;
  }

  .hero-subtitle {
    max-width: 52ch;
  }
}

@media (max-width: 768px) {
  .hero {
    grid-template-columns: 1fr;
    justify-items: center;
    text-align: center;
    padding: 0.5rem 0.75rem;
  }

  .left-hero {
    height: clamp(120px, 38vw, 190px);
    margin-bottom: 0.5rem;
  }

  .hero-logo {
    max-width: 220px;
  }

  .right-hero {
    width: 100%;
  }

  .hero-subtitle {
    margin: 0 auto;
  }

  .hero-stats {
    justify-content: center;
  }

  .browse-link {
    margin: 0 auto;
  }
}

@media (max-width: 480px) {
  .stat-pill {
    width: 100%;
    justify-content: center;
  }
}
</style>
