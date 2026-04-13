<template>
  <div class="view">
    <section class="view-hero shadow-md">
      <div>
        <h1>My Dashboard</h1>
        <p class="subtext">Track and manage your rentals and orders in one place.</p>
      </div>
      <button class="action-btn secondary" :disabled="loading" @click="fetchDashboardData">
        Refresh
      </button>
    </section>

    <section class="stats-grid">
      <article class="stat-card shadow-md">
        <h3>Active Rentals</h3>
        <p>{{ bookings.length }}</p>
      </article>
      <article class="stat-card shadow-md">
        <h3>Pending Orders</h3>
        <p>{{ pendingOrdersCount }}</p>
      </article>
      <article class="stat-card shadow-md">
        <h3>Completed Orders</h3>
        <p>{{ completedOrdersCount }}</p>
      </article>
    </section>

    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <!-- Bookings Section -->
    <section class="card-section shadow-md">
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
                  class="action-btn danger"
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
    <section class="card-section shadow-md">
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
                  class="action-btn primary"
                  :disabled="completingOrderId === order.id"
                  @click="handleCompleteOrder(order.id)"
                >
                  {{ completingOrderId === order.id ? 'Processing...' : 'Pay Now' }}
                </button>
                <span v-else class="action-btn success">Done</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import '@/assets/dashboard.css'

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
