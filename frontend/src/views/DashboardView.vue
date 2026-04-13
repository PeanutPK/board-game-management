<template>
  <div class="dashboard">
    <h1>My Dashboard</h1>

    <div v-if="!isLoggedIn" class="not-logged-in">
      <p>Please log in to view your dashboard</p>
      <router-link to="/" class="btn btn-primary">Go to Home</router-link>
    </div>

    <div v-else class="dashboard-content">
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <!-- Bookings Section -->
      <section class="bookings-section">
        <h2>My Active Bookings</h2>
        <div v-if="loading" class="empty-state">
          <p>Loading bookings...</p>
        </div>
        <div v-else-if="bookings.length === 0" class="empty-state">
          <p>You have no active bookings</p>
        </div>
        <div v-else class="bookings-list">
          <div v-for="booking in bookings" :key="booking.id" class="booking-item">
            <div>
              <h3>Booking #{{ booking.id }}</h3>
              <p>Game ID: {{ booking.game_id }}</p>
              <p>Booked on: {{ formatDate(booking.booking_date) }}</p>
              <p v-if="booking.return_date">Return by: {{ formatDate(booking.return_date) }}</p>
            </div>
            <button @click="handleReturnBooking(booking.id)" class="btn btn-danger">Return</button>
          </div>
        </div>
      </section>

      <!-- Orders Section -->
      <section class="orders-section">
        <h2>My Orders</h2>
        <div v-if="loading" class="empty-state">
          <p>Loading orders...</p>
        </div>
        <div v-else-if="orders.length === 0" class="empty-state">
          <p>You have no orders yet</p>
        </div>
        <div v-else class="orders-list">
          <div v-for="order in orders" :key="order.id" class="order-item">
            <div>
              <h3>Order #{{ order.id }}</h3>
              <p>Game ID: {{ order.game_id }}</p>
              <p>Quantity: {{ order.quantity }}</p>
              <p>Total: ${{ (order.total_price / 100).toFixed(2) }}</p>
              <p :class="`status status-${order.status}`">
                {{ order.status.toUpperCase() }}
              </p>
            </div>
            <button
              v-if="order.status === 'pending'"
              @click="handleCompleteOrder(order.id)"
              :disabled="isUpdatingOrder"
              class="btn btn-success"
            >
              Complete Payment
            </button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getToken } from '../api/auth'
import { getMyBookings, returnBooking } from '../api/bookings'
import type { Booking } from '../api/bookings'
import { completeOrder, getMyOrders, type Order } from '../api/orders'

const bookings = ref<Booking[]>([])
const orders = ref<Order[]>([])
const isLoggedIn = ref(!!getToken())
const loading = ref(false)
const isUpdatingOrder = ref(false)
const errorMessage = ref('')

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
    await returnBooking(bookingId)
    bookings.value = bookings.value.filter((b) => b.id !== bookingId)
  } catch (error) {
    console.error('Failed to return booking:', error)
    errorMessage.value = 'Failed to return booking.'
  }
}

async function handleCompleteOrder(orderId: number) {
  try {
    isUpdatingOrder.value = true
    const updatedOrder = await completeOrder(orderId)
    orders.value = orders.value.map((order) => (order.id === orderId ? updatedOrder : order))
  } catch (error) {
    console.error('Failed to complete order:', error)
    errorMessage.value = 'Failed to complete order.'
  } finally {
    isUpdatingOrder.value = false
  }
}
</script>
