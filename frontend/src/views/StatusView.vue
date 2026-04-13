<template>
  <div class="status-container">
    <div class="status-card p-6 shadow-md rounded-lg text-cblack">
      <p class="status-eyebrow">Backend Monitor</p>
      <h1 class="status-title text-3xl font-bold mb-4 border-b pb-2 text-cblack">System Status</h1>

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
import '@/assets/status.css'

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
