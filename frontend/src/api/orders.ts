/**
 * Orders API client
 */

import { getToken } from './auth'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export interface Order {
  id: number
  user_id: number
  game_id: number
  quantity: number
  total_price: number
  order_date: string
  status: 'pending' | 'completed' | 'cancelled'
}

export interface OrderCreate {
  game_id: number
}

function getHeaders() {
  const token = getToken()
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`
  }
}

export async function createOrder(order: OrderCreate): Promise<Order> {
  const response = await fetch(`${API_URL}/orders/`, {
    method: 'POST',
    headers: getHeaders(),
    body: JSON.stringify(order)
  })

  if (!response.ok) {
    throw new Error('Failed to create order')
  }

  return response.json()
}

export async function getMyOrders(): Promise<Order[]> {
  const response = await fetch(`${API_URL}/orders/`, {
    headers: getHeaders()
  })

  if (!response.ok) {
    throw new Error('Failed to fetch orders')
  }

  return response.json()
}

export async function cancelOrder(orderId: number): Promise<Order> {
  const response = await fetch(`${API_URL}/orders/${orderId}/cancel`, {
    method: 'POST',
    headers: getHeaders()
  })

  if (!response.ok) {
    throw new Error('Failed to cancel order')
  }

  return response.json()
}