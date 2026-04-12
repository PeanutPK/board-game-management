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
  stock: number
  is_available: boolean
}

export interface GameCreate {
  title: string
  description: string
  price: number
  stock: number
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

  return response.data
}

export async function getGameStats(): Promise<{ total: number; available: number }> {
  const response = await api.get(`${API_URL}/games/stats`, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to fetch game stats', error)
    })

  return response.data
}

export async function getGame(id: number): Promise<Game> {
  const response = await api.get(`${API_URL}/games/${id}`, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to fetch game', error)
    })

  return response.data
}

export async function createGame(game: GameCreate): Promise<Game> {
  const response = await api.post(`${API_URL}/games/`, game, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to create game', error)
    })

  return response.data
}

export async function updateGame(id: number, game: Partial<GameCreate>): Promise<Game> {
  const response = await api.put(`${API_URL}/games/${id}`, game, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to update game', error)
    })

  return response.data
}

export async function deleteGame(id: number): Promise<void> {
  const response = await api.delete(`${API_URL}/games/${id}`, {
      headers: getHeaders(),
    })
    .catch(function (error) {
      throw new Error('Failed to delete game', error)
    })
}
