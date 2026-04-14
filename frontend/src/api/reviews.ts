/**
 * Reviews API client
 */

import api from './axios'
import { getToken } from './auth'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export interface Review {
  id: number
  user_id: number
  game_id: number
  username: string
  rating: number
  comment: string
}

export interface ReviewCreate {
  rating: number
  comment: string
}

function getHeaders() {
  const token = getToken()
  return {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
  }
}

export async function getGameReviews(gameId: number): Promise<Review[]> {
  const response = await api
    .get(`${API_URL}/games/${gameId}/reviews`, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to fetch reviews', error)
    })

  return response.data
}

export async function createOrUpdateGameReview(
  gameId: number,
  review: ReviewCreate,
): Promise<Review> {
  const response = await api
    .post(`${API_URL}/games/${gameId}/reviews`, review, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to submit review', error)
    })

  return response.data
}
