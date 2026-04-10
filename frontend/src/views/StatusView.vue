<template>
  <div class="status-container">
    <div class="status-card">
      <p class="eyebrow">Backend Monitor</p>
      <h1>System Status</h1>

      <div v-if="loading" class="loading">Checking backend health...</div>

      <div v-else-if="error" class="error">
        <p class="error-title">Unable to reach service</p>
        <p>{{ error }}</p>
      </div>

      <div v-else class="status">
        <div class="row">
          <span class="label">Health</span>
          <span class="status-badge" :class="healthStatus">{{ health.status }}</span>
        </div>
        <div v-if="health.timestamp" class="row">
          <span class="label">Last Updated</span>
          <span class="timestamp">{{ health.timestamp }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { getStatus } from '@/api/status'
import { ref, onMounted, defineComponent } from 'vue'

export default defineComponent({
  setup() {
    const health = ref({ status: 'unknown', timestamp: new Date().toLocaleString() })
    const loading = ref(true)
    const error = ref('')
    const healthStatus = ref('status-unknown')

    onMounted(async () => {
      try {
        const data = await getStatus()
        health.value = { status: data.status, timestamp: new Date().toLocaleString() }
        healthStatus.value = data.status === 'ok' ? 'status-up' : 'status-down'
      } catch (err) {
        error.value = 'Failed to fetch system status.'
        console.error(err)
        healthStatus.value = 'status-down'
      } finally {
        loading.value = false
      }
    })

    return { health, loading, error, healthStatus }
  },
})
</script>

<style scoped>
.status-container {
  width: 100%;
  height: 100%;
  margin: auto;
  align-items: center;
  justify-items: center;
}

.status-card {
  width: min(680px, 100%);
  border-radius: 1rem;
  border: 1px solid var(--color-cdarkslategray);
  background: var(--color-cgainsboro);
  padding: 1.4rem;
}

.eyebrow {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.11em;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--color-cdarkslategray);
}

h1 {
  margin: 0.4rem 0 1rem;
  color: var(--color-cblack);
  font-size: clamp(1.6rem, 2.8vw, 2.2rem);
}

.loading,
.error,
.status {
  border-radius: 0.85rem;
  border: 1px solid var(--color-cdarkslategray);
  padding: 0.95rem;
  background: var(--color-cgainsboro);
}

.loading {
  color: var(--color-cdarkslategray);
}

.error {
  border-color: var(--color-cdarksalmon);
  background: var(--color-red-200);
  color: var(--color-cindianred);
}

.error-title {
  margin: 0 0 0.25rem;
  font-weight: 700;
}

.error p {
  margin: 0;
}

.status {
  display: grid;
  gap: 0.75rem;
}

.row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
}

.label {
  color: var(--color-cdarkslategray);
  font-weight: 600;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 90px;
  border-radius: 999px;
  padding: 0.3rem 0.72rem;
  border: 1px solid transparent;
  text-transform: uppercase;
  font-size: 0.78rem;
  letter-spacing: 0.04em;
  font-weight: 700;
}

.timestamp {
  color: #2c2c2c;
}

.status-up {
  color: var(--color-green-900);
  background: var(--color-green-200);
  border-color: var(--color-green-300);
}

.status-down {
  color: var(--color-cindianred);
  background: var(--color-red-200);
  border-color: var(--color-red-300);
}

.status-unknown {
  color: var(--color-cdarkslategray);
  background: var(--color-cgainsboro);
  border-color: var(--color-cdarkslategray);
}

@media (max-width: 640px) {
  .status-card {
    padding: 1rem;
  }

  .row {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
