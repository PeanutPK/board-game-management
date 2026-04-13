/**
 * Games API client
 */

import api from './axios'
import { getToken } from './auth'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export interface Game {
  id: number
  title: string
  description: string
  price: number
  rent: number | null
  average_rating: number | null
  min_players: number | null
  max_players: number | null
  average_playtime: number | null
  recommended_age: number | null
  stock: number
  is_available: boolean
}

export interface GameCreate {
  title: string
  description: string
  price: number
  rent: number
  min_players: number
  max_players: number
  average_playtime: number
  recommended_age: number
  stock: number
}

export interface GameUpdatePayload {
  title?: string
  description?: string
  price?: number
  rent?: number
  min_players?: number
  max_players?: number
  average_playtime?: number
  recommended_age?: number
  stock?: number
  is_available?: boolean
}

function getHeaders() {
  const token = getToken()
  return {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
  }
}

export async function getGames(
  skip: number = 0,
  limit: number = 10,
  available_only: boolean = false,
): Promise<Game[]> {
  const response = await api
    .get(`${API_URL}/games/?skip=${skip}&limit=${limit}&available_only=${available_only}`, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to fetch games', error)
    })
  console.log(response.data[0])

  return response.data
}

export async function getGameStats(): Promise<{ total: number; available: number }> {
  const response = await api
    .get(`${API_URL}/games/stats`, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to fetch game stats', error)
    })

  return response.data
}

export async function getTrendingGames(limit: number = 4): Promise<Game[]> {
  const response = await api.get(`${API_URL}/games/trending?limit=${limit}`, {
    headers: getHeaders(),
  })

  return response.data
}

export async function getGame(id: number): Promise<Game> {
  const response = await api
    .get(`${API_URL}/games/${id}`, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to fetch game', error)
    })

  return response.data
}

export async function createGame(game: GameCreate): Promise<Game> {
  const response = await api
    .post(`${API_URL}/games/`, game, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to create game', error)
    })

  return response.data
}

export async function updateGame(id: number, game: GameUpdatePayload): Promise<Game> {
  const response = await api
    .put(`${API_URL}/games/${id}`, game, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to update game', error)
    })

  return response.data
}

export async function deleteGame(id: number): Promise<void> {
  await api
    .delete(`${API_URL}/games/${id}`, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to delete game', error)
    })
}
