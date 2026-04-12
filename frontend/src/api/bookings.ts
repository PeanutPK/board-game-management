/**
 * Bookings API client
 */
import api from './axios'
import { getToken } from './auth'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export interface Booking {
  id: number
  user_id: number
  game_id: number
  booking_date: string
  return_date: string | null
  is_active: boolean
}

export interface BookingCreate {
  game_id: number
  return_date?: string | null
}

function getHeaders() {
  const token = getToken()
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`
  }
}

export async function createBooking(booking: BookingCreate): Promise<Booking> {
  const response = await api.post(`${API_URL}/bookings/`, booking, {
    headers: getHeaders(),
  })
  .catch(function(error) {
    throw new Error('Failed to create booking')
  })

  return response.data
}

export async function getMyBookings(): Promise<Booking[]> {
  const response = await api.get(`${API_URL}/bookings/`, {
    headers: getHeaders()
  })
  .catch(function(error) {
    throw new Error('Failed to fetch bookings')
  })

  return response.data
}

export async function returnBooking(bookingId: number): Promise<Booking> {
  const response = await api.post(`${API_URL}/bookings/${bookingId}/return`, {}, {
    headers: getHeaders()
  })
  .catch(function(error) {
    throw new Error('Failed to return booking')
  })

  return response.data
}
