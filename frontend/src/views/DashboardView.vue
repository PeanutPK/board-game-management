<template>
  <div class="dashboard">
    <h1>My Dashboard</h1>

    <div v-if="!isLoggedIn" class="not-logged-in">
      <p>Please log in to view your dashboard</p>
      <router-link to="/" class="btn btn-primary">Go to Home</router-link>
    </div>

    <div v-else class="dashboard-content">
      <!-- Bookings Section -->
      <section class="bookings-section">
        <h2>My Active Bookings</h2>
        <div v-if="bookings.length === 0" class="empty-state">
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
        <div v-if="orders.length === 0" class="empty-state">
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
import type { Order } from '../api/orders'

const bookings = ref<Booking[]>([])
const orders = ref<Order[]>([])
const isLoggedIn = ref(!!getToken())

onMounted(async () => {
  if (!isLoggedIn.value) return

  try {
    bookings.value = await getMyBookings()
  } catch (error) {
    console.error('Failed to fetch bookings:', error)
  }
})

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
  }
}

async function handleCompleteOrder(orderId: number) {
  try {
    // Call complete order API
    console.log('Completing order:', orderId)
  } catch (error) {
    console.error('Failed to complete order:', error)
  }
}
</script>
