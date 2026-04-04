/**
 * Bookings API client
 */

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
  const response = await fetch(`${API_URL}/bookings/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(booking)
  })

  if (!response.ok) {
    throw new Error('Failed to create booking')
  }

  return response.json()
}

export async function getMyBookings(): Promise<Booking[]> {
  const response = await fetch(`${API_URL}/bookings/`, {
    headers: getHeaders()
  })

  if (!response.ok) {
    throw new Error('Failed to fetch bookings')
  }

  return response.json()
}

export async function returnBooking(bookingId: number): Promise<Booking> {
  const response = await fetch(`${API_URL}/bookings/${bookingId}/return`, {
    method: 'POST',
    headers: getHeaders()
  })

  if (!response.ok) {
    throw new Error('Failed to return booking')
  }

  return response.json()
}