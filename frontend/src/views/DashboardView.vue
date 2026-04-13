<template>
  <div class="dashboard page-container">
    <div class="dashboard-head">
      <div>
        <h1>My Dashboard</h1>
        <p class="subtitle">Track and manage your rentals and orders in one place.</p>
      </div>
      <button class="btn btn-primary" :disabled="loading" @click="fetchDashboardData">Refresh</button>
    </div>

    <div v-if="!isLoggedIn" class="not-logged-in">
      <p>Please log in to view your dashboard</p>
      <router-link to="/" class="btn btn-primary">Go to Home</router-link>
    </div>

    <div v-else class="dashboard-content">
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <section class="summary-grid">
        <article class="summary-card">
          <p class="label">Active Rentals</p>
          <p class="value">{{ bookings.length }}</p>
        </article>
        <article class="summary-card">
          <p class="label">Pending Orders</p>
          <p class="value">{{ pendingOrdersCount }}</p>
        </article>
        <article class="summary-card">
          <p class="label">Completed Orders</p>
          <p class="value">{{ completedOrdersCount }}</p>
        </article>
      </section>

      <!-- Bookings Section -->
      <section class="card-section">
        <div class="section-head">
          <h2>My Active Rentals</h2>
        </div>

        <div v-if="loading" class="empty-state">
          <p>Loading bookings...</p>
        </div>
        <div v-else-if="bookings.length === 0" class="empty-state">
          <p>You have no active rentals.</p>
        </div>
        <div v-else class="table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>Booking #</th>
                <th>Game ID</th>
                <th>Booked Date</th>
                <th>Return Date</th>
                <th class="actions-col">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="booking in bookings" :key="booking.id">
                <td>#{{ booking.id }}</td>
                <td>{{ booking.game_id }}</td>
                <td>{{ formatDate(booking.booking_date) }}</td>
                <td>{{ booking.return_date ? formatDate(booking.return_date) : '-' }}</td>
                <td class="actions-col">
                  <button
                    class="btn btn-danger"
                    :disabled="returningBookingId === booking.id"
                    @click="handleReturnBooking(booking.id)"
                  >
                    {{ returningBookingId === booking.id ? 'Returning...' : 'Return' }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Orders Section -->
      <section class="card-section">
        <div class="section-head">
          <h2>My Orders</h2>
        </div>

        <div v-if="loading" class="empty-state">
          <p>Loading orders...</p>
        </div>
        <div v-else-if="orders.length === 0" class="empty-state">
          <p>You have no orders yet.</p>
        </div>
        <div v-else class="table-wrap">
          <table class="data-table">
            <thead>
              <tr>
                <th>Order #</th>
                <th>Game ID</th>
                <th>Qty</th>
                <th>Total</th>
                <th>Date</th>
                <th>Status</th>
                <th class="actions-col">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in sortedOrders" :key="order.id">
                <td>#{{ order.id }}</td>
                <td>{{ order.game_id }}</td>
                <td>{{ order.quantity }}</td>
                <td>${{ (order.total_price / 100).toFixed(2) }}</td>
                <td>{{ formatDate(order.order_date) }}</td>
                <td>
                  <span :class="`status-badge status-${order.status}`">
                    {{ order.status.toUpperCase() }}
                  </span>
                </td>
                <td class="actions-col">
                  <button
                    v-if="order.status === 'pending'"
                    class="btn btn-success"
                    :disabled="completingOrderId === order.id"
                    @click="handleCompleteOrder(order.id)"
                  >
                    {{ completingOrderId === order.id ? 'Processing...' : 'Complete Payment' }}
                  </button>
                  <span v-else class="done-text">-</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { getToken } from '../api/auth'
import { getMyBookings, returnBooking } from '../api/bookings'
import type { Booking } from '../api/bookings'
import { completeOrder, getMyOrders, type Order } from '../api/orders'

const bookings = ref<Booking[]>([])
const orders = ref<Order[]>([])
const isLoggedIn = ref(!!getToken())
const loading = ref(false)
const errorMessage = ref('')
const completingOrderId = ref<number | null>(null)
const returningBookingId = ref<number | null>(null)

const pendingOrdersCount = computed(
  () => orders.value.filter((order) => order.status === 'pending').length,
)
const completedOrdersCount = computed(
  () => orders.value.filter((order) => order.status === 'completed').length,
)

const sortedOrders = computed(() => {
  return [...orders.value].sort(
    (a, b) => new Date(b.order_date).getTime() - new Date(a.order_date).getTime(),
  )
})

onMounted(async () => {
  if (!isLoggedIn.value) {
    return
  }

  await fetchDashboardData()
})

async function fetchDashboardData() {
  loading.value = true
  errorMessage.value = ''

  try {
    const [bookingList, orderList] = await Promise.all([getMyBookings(), getMyOrders()])
    bookings.value = bookingList
    orders.value = orderList
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
    errorMessage.value = 'Failed to load dashboard data. Please try again.'
  } finally {
    loading.value = false
  }
}

function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

async function handleReturnBooking(bookingId: number) {
  try {
    returningBookingId.value = bookingId
    await returnBooking(bookingId)
    bookings.value = bookings.value.filter((b) => b.id !== bookingId)
  } catch (error) {
    console.error('Failed to return booking:', error)
    errorMessage.value = 'Failed to return booking.'
  } finally {
    returningBookingId.value = null
  }
}

async function handleCompleteOrder(orderId: number) {
  try {
    completingOrderId.value = orderId
    const updatedOrder = await completeOrder(orderId)
    orders.value = orders.value.map((order) => (order.id === orderId ? updatedOrder : order))
  } catch (error) {
    console.error('Failed to complete order:', error)
    errorMessage.value = 'Failed to complete order.'
  } finally {
    completingOrderId.value = null
  }
}
</script>

<style scoped>
.page-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px;
}

.dashboard-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
}

.subtitle {
  margin-top: 6px;
  color: #667085;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

.summary-card {
  background: #fff;
  border: 1px solid #eaecf0;
  border-radius: 10px;
  padding: 12px 14px;
}

.summary-card .label {
  color: #667085;
  font-size: 13px;
  margin: 0;
}

.summary-card .value {
  margin: 4px 0 0;
  font-size: 24px;
  font-weight: 700;
}

.card-section {
  background: #fff;
  border: 1px solid #eaecf0;
  border-radius: 12px;
  padding: 14px;
  margin-bottom: 16px;
}

.section-head {
  margin-bottom: 10px;
}

.table-wrap {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  border-top: 1px solid #eaecf0;
  padding: 10px;
  text-align: left;
  white-space: nowrap;
}

.data-table thead th {
  border-top: none;
  color: #475467;
  font-size: 13px;
}

.actions-col {
  text-align: right;
}

.status-badge {
  display: inline-flex;
  padding: 2px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.status-pending {
  background: #fffaeb;
  color: #b54708;
}

.status-completed {
  background: #ecfdf3;
  color: #067647;
}

.status-cancelled {
  background: #fef3f2;
  color: #b42318;
}

.done-text {
  color: #98a2b3;
}

.error-message {
  color: #b42318;
  background: #fef3f2;
  border: 1px solid #fecdca;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.btn {
  border: none;
  border-radius: 8px;
  padding: 8px 12px;
  font-weight: 600;
  cursor: pointer;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: #5a42ee;
  color: #fff;
}

.btn-danger {
  background: #ef4444;
  color: #fff;
}

.btn-success {
  background: #16a34a;
  color: #fff;
}

.empty-state {
  color: #667085;
  padding: 14px;
  text-align: center;
}

@media (max-width: 768px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }

  .dashboard-head {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
